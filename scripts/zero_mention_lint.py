#!/usr/bin/env python3
"""Lint rendered student-facing text for missing protected source mentions."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    from docx import Document  # type: ignore
except Exception:  # pragma: no cover
    Document = None  # type: ignore

PUBLIC_VISIBILITY = {"public_knowledge", "include_in_notes", "student_visible", "required"}
SKIP_VISIBILITY = {"internal_audit_only", "excluded_admin", "duplicate_bound_elsewhere", "exclude_admin"}
SKIP_STATUS = {"excluded_with_reason", "duplicate_covered_elsewhere", "audit_only", "unreadable", "unsupported"}


def normalise(value: str) -> str:
    value = value.casefold().replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", value).strip()


def read_text(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        if Document is None:
            raise RuntimeError("python-docx is required to lint DOCX files")
        doc = Document(path)
        return "\n".join(paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip())
    return path.read_text(encoding="utf-8", errors="ignore")


def collect_output_text(paths: list[Path]) -> str:
    parts: list[str] = []
    for path in paths:
        if path.is_file():
            parts.append(read_text(path))
        elif path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file() and child.suffix.lower() in {".docx", ".md", ".txt"}:
                    parts.append(read_text(child))
    return "\n".join(parts)


def load_units(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    for key in ["protected_units", "protected_source_units", "units", "slide_or_page_units"]:
        value = data.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    if isinstance(data.get("slide_atomic_ledger"), dict):
        return load_units_from_ledger(data["slide_atomic_ledger"])
    return []


def load_units_from_ledger(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    units: list[dict[str, Any]] = []
    for item in ledger.get("slide_or_page_units", []) or []:
        if isinstance(item, dict):
            units.append(item)
    return units


def expected_mentions(unit: dict[str, Any]) -> list[str]:
    value = unit.get("expected_public_mentions")
    if isinstance(value, str):
        mentions = [value]
    elif isinstance(value, list):
        mentions = [str(item) for item in value if str(item).strip()]
    else:
        mentions = []
    if not mentions:
        for key in ["mention_text", "raw_heading", "term", "name", "unit_id"]:
            if unit.get(key):
                mentions.append(str(unit[key]))
                break
    return [mention.strip() for mention in mentions if mention.strip()]


def should_check(unit: dict[str, Any]) -> bool:
    visibility = str(unit.get("required_visibility") or unit.get("student_visibility") or unit.get("protected_status") or "public_knowledge")
    status = str(unit.get("coverage_status") or "")
    if visibility in SKIP_VISIBILITY or status in SKIP_STATUS:
        return False
    return visibility in PUBLIC_VISIBILITY or bool(expected_mentions(unit))


def unit_present(unit: dict[str, Any], output_text_norm: str) -> bool:
    mentions = expected_mentions(unit)
    for mention in mentions:
        if normalise(mention) in output_text_norm:
            return True
    return False


def lint_units(units: list[dict[str, Any]], output_text: str) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    output_text_norm = normalise(output_text)
    for unit in units:
        if not should_check(unit):
            continue
        if not unit_present(unit, output_text_norm):
            failures.append(
                {
                    "type": "protected_unit_zero_visible_mention",
                    "unit_id": unit.get("unit_id"),
                    "locator": unit.get("locator"),
                    "expected_public_mentions": expected_mentions(unit),
                }
            )
    return failures


def lint(protected_items: Path, output_paths: list[Path]) -> dict[str, Any]:
    units = load_units(protected_items)
    output_text = collect_output_text(output_paths)
    failures: list[dict[str, Any]] = []
    if not units:
        failures.append({"type": "no_protected_units_loaded", "protected_items": str(protected_items)})
    if not output_text.strip():
        failures.append({"type": "no_output_text_loaded", "outputs": [str(path) for path in output_paths]})
    if units and output_text.strip():
        failures.extend(lint_units(units, output_text))
    return {"status": "pass" if not failures else "fail", "counts": {"protected_units": len(units)}, "failures": failures}


def self_test() -> dict[str, Any]:
    units = [
        {"unit_id": "u1", "required_visibility": "public_knowledge", "expected_public_mentions": ["Beer-Lambert"]},
        {"unit_id": "u2", "required_visibility": "public_knowledge", "expected_public_mentions": ["PCR-RFLP"]},
        {"unit_id": "u3", "required_visibility": "duplicate_bound_elsewhere", "expected_public_mentions": ["Hidden duplicate"]},
    ]
    good_text = "Beer-Lambert converts absorbance into concentration. PCR-RFLP converts SNP differences into fragment patterns."
    bad_text = "Absorbance and PCR diagnostics are important."
    good_failures = lint_units(units, good_text)
    bad_failures = lint_units(units, bad_text)
    failures: list[dict[str, Any]] = []
    if good_failures:
        failures.append({"type": "self_test_good_fixture_rejected", "failures": good_failures})
    if not any(item.get("unit_id") == "u1" for item in bad_failures) or not any(item.get("unit_id") == "u2" for item in bad_failures):
        failures.append({"type": "self_test_bad_fixture_not_rejected", "bad_failures": bad_failures})
    return {
        "status": "pass" if not failures else "fail",
        "good_fixture_failures": good_failures,
        "bad_fixture_failures": bad_failures,
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protected-items", type=Path)
    parser.add_argument("outputs", nargs="*", type=Path)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    elif args.protected_items and args.outputs:
        result = lint(args.protected_items, args.outputs)
    else:
        result = {"status": "fail", "failures": [{"type": "missing_protected_items_or_outputs"}]}
    text = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0 if result.get("status") == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
