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

REQUIRED_CLINICAL_MODULES = {
    "drug_target_definition": ["drug target definition"],
    "on_target_vs_off_target": ["on-target", "off-target"],
    "good_drug_target_criteria": ["good drug target criteria"],
    "why_gpcrs_are_good_targets": ["why gpcr"],
    "target_validation": ["target validation"],
    "assay_vs_screen": ["assay", "screen"],
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


def lint(
    text: str,
    *,
    clinical_target_discovery: bool,
    ledger: dict[str, Any] | None = None,
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

    if clinical_target_discovery:
        found: dict[str, dict[str, Any]] = {}
        for module_id, required_terms in REQUIRED_CLINICAL_MODULES.items():
            module = find_module(modules, required_terms)
            if not module:
                failures.append({"type": "missing_standalone_module", "module": module_id})
            else:
                found[module_id] = module

        criteria = found.get("good_drug_target_criteria")
        if criteria:
            criteria_section = section_after(criteria["body"], "Criteria / Components / Steps")
            if bullet_count(criteria_section) < 3:
                failures.append({"type": "good_target_criteria_collapsed_into_prose"})

        gpcr = found.get("why_gpcrs_are_good_targets")
        if gpcr:
            gpcr_text = normalize(gpcr["body"])
            for term in ["physiolog", "access", "modulat", "divers"]:
                if term not in gpcr_text:
                    failures.append({"type": "gpcr_rationale_missing_component", "component": term})

        on_off = found.get("on_target_vs_off_target")
        if on_off:
            body = on_off["body"]
            before_trap = body.split("Common Error / Trap:", 1)[0].split("Must Master:", 1)[0]
            if "on-target" not in normalize(before_trap) or "off-target" not in normalize(before_trap):
                failures.append({"type": "on_off_target_only_in_trap_or_must_master"})

        target_priorities = [priority_value(module.get("priority")) for module in found.values()]
        max_target_priority = max(target_priorities) if target_priorities else 0
        target_lengths = [len(normalize(module["body"]).split()) for module in found.values()]
        max_target_length = max(target_lengths) if target_lengths else 0
        for module in modules:
            title = normalize(module["title"])
            if any(term in title for term in ["pipeline", "stakeholder", "background"]):
                if priority_value(module.get("priority")) > max_target_priority:
                    failures.append({"type": "background_module_priority_exceeds_target_core", "module_title": module["title"]})
                if len(normalize(module["body"]).split()) > max_target_length and "direct exam-operation justification" not in normalize(module["body"]):
                    failures.append({"type": "background_module_longer_than_target_core", "module_title": module["title"]})

    return {
        "pass": not failures,
        "counts": {
            "modules": len(modules),
            "legacy_strings_checked": len(OLD_VISIBLE_STRINGS),
            "forbidden_public_phrases_checked": len(FORBIDDEN_PUBLIC_PHRASES),
            "atomic_units_checked": len((ledger or {}).get("units", [])) if isinstance(ledger, dict) else 0,
        },
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--clinical-target-discovery", action="store_true")
    parser.add_argument("--ledger", type=Path, help="Optional AtomicKnowledgeLedger JSON for generic coverage linting.")
    parser.add_argument("--min-modules", type=int, help="Fail if fewer modules are detected.")
    parser.add_argument("--require-module-term", action="append", default=[], help="Fail unless a module title contains all terms.")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        result = lint(
            collect_text(args.path),
            clinical_target_discovery=args.clinical_target_discovery,
            ledger=load_ledger(args.ledger),
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
