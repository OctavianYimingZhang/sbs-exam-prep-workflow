#!/usr/bin/env python3
"""Lint Academic Exam-Ready Notes for protected baseline coverage."""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from html import unescape
from pathlib import Path
from typing import Any

from knowledge_only_rendering_rules import forbidden_advisory_heading_hits, forbidden_advisory_phrase_hits


OLD_VISIBLE_STRINGS = [
    "Priority: 必备",
    "Priority: 重点",
    "Priority: 补充",
    "Evidence / Example Function",
]

FORBIDDEN_PUBLIC_PHRASES = [
    "Course-Level Exam Map",
    "assessment includes",
    "summative examination",
    "Section A asks",
    "Section B is",
    "Coverage note:",
    "no mark scheme",
    "historical papers",
    "older papers",
    "current regime",
    "ELM should be checked",
    "source coverage",
    "extraction quality",
]

FORBIDDEN_INTERNAL_HEADINGS = [
    "Exam Specificity",
    "Core Exam Claim",
    "Exam Use",
    "Common Error / Trap",
    "Must Master",
    "How To Answer This Exam",
]

PROTECTED_ITEM_TYPE_REQUIREMENTS = {
    "definition": "must appear under Definitions or as a standalone definition module",
    "contrast_pair": "must compare both sides in the explanation before any question-type add-on",
    "criteria_list": "must appear under Criteria as a list",
    "why_x_block": "must appear under Example or as a standalone Why-X module",
    "named_example": "must appear under Example or a named-example module",
    "assay_or_method": "must include method principle, readout, interpretation, and limitation when those terms are required by the fixture",
    "calculation_rule": "must include formula, units, substitution logic, and interpretation when those terms are required by the fixture",
    "graph_readout": "must include axis, trend, parameter extraction, and conclusion when those terms are required by the fixture",
    "workflow": "must preserve ordered steps when the source provides a workflow",
}

MODULE_HEADING_RE = re.compile(r"^(?:#{1,6}\s*)?Module\s*:\s*(.+?)\s*$", re.IGNORECASE)
STAR_HEADING_RE = re.compile(r"^(?:#{1,6}\s*)?(★★★|★★|★)\s+(.+?)\s*$")
PRIORITY_RE = re.compile(r"^Priority:\s*(★★★|★★|★)\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^(?:#{1,6}\s*)?[A-Z][A-Za-z /-]+:\s*$", re.MULTILINE)


def read_docx(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        chunks: list[str] = []
        for name in archive.namelist():
            if name.startswith("word/") and name.endswith(".xml"):
                raw = archive.read(name).decode("utf-8", errors="ignore")
                raw = re.sub(r"<[^>]+>", " ", raw)
                chunks.append(unescape(raw))
        return "\n".join(chunks)


def read_text_path(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        return read_docx(path)
    return path.read_text(encoding="utf-8", errors="ignore")


def collect_text(path: Path) -> str:
    if path.is_file():
        return read_text_path(path)
    chunks: list[str] = []
    for child in sorted(path.rglob("*")):
        if child.is_file() and child.suffix.lower() in {".txt", ".md", ".json", ".docx"}:
            chunks.append(read_text_path(child))
    return "\n\n".join(chunks)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold().replace("–", "-").replace("—", "-")).strip()


def parse_modules(text: str) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    offset = 0
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        module_match = MODULE_HEADING_RE.match(stripped)
        star_match = STAR_HEADING_RE.match(stripped)
        if module_match:
            matches.append({"start": offset, "title": module_match.group(1).strip(), "inline_priority": None})
        elif star_match:
            matches.append({"start": offset, "title": star_match.group(2).strip(), "inline_priority": star_match.group(1)})
        offset += len(line)
    modules: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        start = match["start"]
        end = matches[index + 1]["start"] if index + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        priority = match.get("inline_priority")
        priority_match = PRIORITY_RE.search(body)
        if priority_match:
            priority = priority_match.group(1)
        modules.append({"title": match["title"], "body": body, "priority": priority})
    return modules


def find_module(modules: list[dict[str, Any]], required_terms: list[str]) -> dict[str, Any] | None:
    for module in modules:
        title = normalize(module["title"])
        if all(term in title for term in required_terms):
            return module
    return None


def terms_from_config(value: Any) -> list[str]:
    if isinstance(value, list):
        return [normalize(str(item)) for item in value if normalize(str(item))]
    if isinstance(value, str) and normalize(value):
        return [normalize(value)]
    return []


def term_present(text: str, term: str) -> bool:
    return normalize(term) in normalize(text)


def load_protected_items(path: Path | None) -> dict[str, Any] | None:
    if not path:
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def section_after(body: str, heading: str) -> str:
    pattern = re.compile(rf"^{re.escape(heading)}:\s*$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(body)
    if not match:
        return ""
    next_heading = HEADING_RE.search(body, match.end())
    return body[match.end() : next_heading.start() if next_heading else len(body)]


def bullet_count(text: str) -> int:
    return len(re.findall(r"^\s*(?:[-*]|\d+[.)])\s+\S+", text, re.MULTILINE))


def priority_value(priority: str | None) -> int:
    return {"★★★": 3, "★★": 2, "★": 1}.get(priority or "", 0)


def internal_heading_present(text: str, heading: str) -> bool:
    return re.search(rf"(?im)^\s*(?:#+\s*)?{re.escape(heading)}\s*:?\s*$", text) is not None


def load_ledger(path: Path | None) -> dict[str, Any] | None:
    if not path:
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def significant_terms(text: str) -> list[str]:
    return [term for term in re.findall(r"[a-z0-9]+", normalize(text)) if len(term) > 2]


def lint_atomic_coverage(text: str, ledger: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not ledger:
        return []
    failures: list[dict[str, Any]] = []
    normalized_text = normalize(text)
    units = ledger.get("units", ledger if isinstance(ledger, list) else [])
    if not isinstance(units, list):
        return [{"type": "atomic_ledger_units_not_list"}]
    allowed_status = {"covered", "grouped_but_named"}
    for atom in units:
        if not isinstance(atom, dict):
            continue
        if atom.get("student_visibility") != "include_in_notes":
            continue
        if atom.get("coverage_status") not in allowed_status:
            failures.append({
                "type": "atomic_knowledge_unit_missing",
                "unit_id": atom.get("unit_id"),
                "raw_heading": atom.get("raw_heading"),
            })
            continue
        terms = significant_terms(str(atom.get("raw_heading", "")))
        if terms and not all(term in normalized_text for term in terms[:4]):
            failures.append({
                "type": "atomic_knowledge_unit_not_named_in_output",
                "unit_id": atom.get("unit_id"),
                "raw_heading": atom.get("raw_heading"),
            })
    return failures


def lint_protected_item(module: dict[str, Any], item: dict[str, Any]) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    item_id = item.get("item_id")
    item_type = item.get("item_type")
    if item_type not in PROTECTED_ITEM_TYPE_REQUIREMENTS:
        failures.append({"type": "unknown_protected_item_type", "item_id": item_id, "item_type": item_type})
        return failures

    body = module["body"]
    for term in terms_from_config(item.get("required_terms")):
        if not term_present(body, term):
            failures.append({"type": "protected_item_required_term_missing", "item_id": item_id, "term": term})

    for term in terms_from_config(item.get("body_terms")):
        if not term_present(body, term):
            failures.append({"type": "protected_item_body_term_missing", "item_id": item_id, "term": term})

    required_section = str(item.get("required_section") or "").strip()
    section_text = section_after(body, required_section) if required_section else ""
    if required_section and not section_text:
        failures.append({"type": "protected_item_required_section_missing", "item_id": item_id, "section": required_section})
    for term in terms_from_config(item.get("section_terms")):
        if not term_present(section_text, term):
            failures.append({"type": "protected_item_section_term_missing", "item_id": item_id, "section": required_section, "term": term})
    min_bullets = item.get("min_section_bullets")
    if isinstance(min_bullets, int) and bullet_count(section_text) < min_bullets:
        failures.append({
            "type": "protected_item_list_collapsed_into_prose",
            "item_id": item_id,
            "section": required_section,
            "bullets": bullet_count(section_text),
            "minimum": min_bullets,
        })

    pre_trap_terms = terms_from_config(item.get("pre_trap_terms"))
    if pre_trap_terms:
        before_trap = body.split("Common Error / Trap:", 1)[0].split("Must Master:", 1)[0]
        for term in pre_trap_terms:
            if not term_present(before_trap, term):
                failures.append({"type": "protected_item_only_in_trap_or_must_master", "item_id": item_id, "term": term})

    if item_type == "definition" and not (
        section_after(body, required_section or "Definitions")
        or section_after(body, "Key Definitions")
        or "definition" in normalize(module["title"])
    ):
        failures.append({"type": "definition_not_visible_as_definition", "item_id": item_id})
    if item_type == "criteria_list" and bullet_count(section_after(body, required_section or "Criteria")) < int(min_bullets or 1):
        failures.append({"type": "criteria_list_not_preserved_as_list", "item_id": item_id})
    if item_type in {"why_x_block", "named_example"} and not (
        section_after(body, required_section or "Example")
        or section_after(body, "Canonical Example")
        or normalize(module["title"]).startswith("why ")
    ):
        failures.append({"type": "named_example_or_why_block_not_visible", "item_id": item_id})

    return failures


def lint_protected_items(modules: list[dict[str, Any]], protected_config: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not protected_config:
        return []
    failures: list[dict[str, Any]] = []
    items = protected_config.get("protected_items", [])
    if not isinstance(items, list):
        return [{"type": "protected_items_not_list"}]

    found: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            failures.append({"type": "protected_item_not_object"})
            continue
        item_id = str(item.get("item_id") or "")
        title_terms = terms_from_config(item.get("title_terms") or item.get("module_title_terms"))
        module = find_module(modules, title_terms) if title_terms else None
        if not module:
            failures.append({"type": "missing_protected_standalone_module", "item_id": item_id, "title_terms": title_terms})
            continue
        found[item_id] = module
        failures.extend(lint_protected_item(module, item))

    core_item_ids = {str(item_id) for item_id in protected_config.get("core_item_ids", [])}
    core_modules = [module for item_id, module in found.items() if item_id in core_item_ids]
    if core_modules:
        max_core_priority = max(priority_value(module.get("priority")) for module in core_modules)
        max_core_length = max(len(normalize(module["body"]).split()) for module in core_modules)
        for background in protected_config.get("background_modules", []):
            terms = terms_from_config(background.get("title_terms") if isinstance(background, dict) else background)
            if not terms:
                continue
            for module in modules:
                if all(term in normalize(module["title"]) for term in terms):
                    if priority_value(module.get("priority")) > max_core_priority:
                        failures.append({"type": "background_module_priority_exceeds_protected_core", "module_title": module["title"]})
                    allow_longer_if = normalize(str(background.get("allow_longer_if", ""))) if isinstance(background, dict) else ""
                    if len(normalize(module["body"]).split()) > max_core_length and (not allow_longer_if or allow_longer_if not in normalize(module["body"])):
                        failures.append({"type": "background_module_longer_than_protected_core", "module_title": module["title"]})

    return failures


def lint(
    text: str,
    *,
    ledger: dict[str, Any] | None = None,
    protected_config: dict[str, Any] | None = None,
    min_modules: int | None = None,
    require_module_terms: list[str] | None = None,
) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    for old in OLD_VISIBLE_STRINGS:
        if old in text:
            failures.append({"type": "legacy_visible_template_string", "string": old})
    for phrase in FORBIDDEN_PUBLIC_PHRASES:
        if phrase.lower() in text.lower():
            failures.append({"type": "forbidden_public_phrase", "phrase": phrase})
    for heading in FORBIDDEN_INTERNAL_HEADINGS:
        if internal_heading_present(text, heading):
            failures.append({"type": "forbidden_internal_heading", "heading": heading})
    for phrase in forbidden_advisory_phrase_hits(text):
        failures.append({"type": "forbidden_advisory_phrase", "phrase": phrase})
    for heading in forbidden_advisory_heading_hits(text):
        failures.append({"type": "forbidden_advisory_heading", "heading": heading})

    modules = parse_modules(text)
    if not modules:
        failures.append({"type": "no_modules_detected"})
    if modules and any(module.get("priority") is None for module in modules):
        failures.append({"type": "module_missing_star_priority"})
    if min_modules is not None and len(modules) < min_modules:
        failures.append({"type": "module_density_below_floor", "modules": len(modules), "minimum": min_modules})
    for required in require_module_terms or []:
        terms = [term for term in re.split(r"[\s,+/]+", normalize(required)) if term]
        if not any(all(term in normalize(module["title"]) for term in terms) for module in modules):
            failures.append({"type": "missing_required_module_term", "term": required})

    failures.extend(lint_atomic_coverage(text, ledger))
    failures.extend(lint_protected_items(modules, protected_config))

    return {
        "pass": not failures,
        "counts": {
            "modules": len(modules),
            "legacy_strings_checked": len(OLD_VISIBLE_STRINGS),
            "forbidden_public_phrases_checked": len(FORBIDDEN_PUBLIC_PHRASES),
            "atomic_units_checked": len((ledger or {}).get("units", [])) if isinstance(ledger, dict) else 0,
            "protected_items_checked": len((protected_config or {}).get("protected_items", [])) if isinstance(protected_config, dict) else 0,
        },
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--ledger", type=Path, help="Optional AtomicKnowledgeLedger JSON for generic coverage linting.")
    parser.add_argument("--protected-items", type=Path, help="Optional protected-item fixture JSON for generic source-feature coverage linting.")
    parser.add_argument("--min-modules", type=int, help="Fail if fewer modules are detected.")
    parser.add_argument("--require-module-term", action="append", default=[], help="Fail unless a module title contains all terms.")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        result = lint(
            collect_text(args.path),
            ledger=load_ledger(args.ledger),
            protected_config=load_protected_items(args.protected_items),
            min_modules=args.min_modules,
            require_module_terms=args.require_module_term,
        )
    except Exception as exc:
        result = {"pass": False, "failures": [{"type": "read_error", "error": str(exc)}]}

    text = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
