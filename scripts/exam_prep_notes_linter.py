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

REQUIRED_CLINICAL_MODULES = {
    "drug_target_definition": ["drug target definition"],
    "on_target_vs_off_target": ["on-target", "off-target"],
    "good_drug_target_criteria": ["good drug target criteria"],
    "why_gpcrs_are_good_targets": ["why gpcr"],
    "target_validation": ["target validation"],
    "assay_vs_screen": ["assay", "screen"],
}

SECTION_RE = re.compile(r"^(?:#{1,6}\s*)?(?:Module\s*:|###\s*Module\s*:)\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
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
    matches = list(SECTION_RE.finditer(text))
    modules: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        priority = None
        priority_match = PRIORITY_RE.search(body)
        if priority_match:
            priority = priority_match.group(1)
        modules.append({"title": match.group(1).strip(), "body": body, "priority": priority})
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


def lint(text: str, *, clinical_target_discovery: bool) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    for old in OLD_VISIBLE_STRINGS:
        if old in text:
            failures.append({"type": "legacy_visible_template_string", "string": old})

    modules = parse_modules(text)
    if modules and any(module.get("priority") is None for module in modules):
        failures.append({"type": "module_missing_star_priority"})

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
        },
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--clinical-target-discovery", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        result = lint(collect_text(args.path), clinical_target_discovery=args.clinical_target_discovery)
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
