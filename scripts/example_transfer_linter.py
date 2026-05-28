#!/usr/bin/env python3
"""Lint ExampleReviewLedger files before example-derived rules are promoted."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


DIRECT_COPY_PATTERNS = [
    re.compile(r"\bcopy\s+this\b", re.I),
    re.compile(r"\bmake\s+future\s+output\s+like\s+this\b", re.I),
    re.compile(r"\buse\s+the\s+same\s+module\s+list\b", re.I),
    re.compile(r"\bkeep\s+the\s+exact\s+heading\b", re.I),
    re.compile(r"\btransfer\s+the\s+topic\s+content\b", re.I),
]

ACCEPTED_STATUSES = {"accepted"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def as_non_empty_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold()).strip()


def contains_blocked_content(text: str, blocked_items: list[str]) -> str | None:
    normalized_text = normalize(text)
    for item in blocked_items:
        normalized_item = normalize(item)
        if normalized_item and normalized_item in normalized_text:
            return item
    return None


def has_direct_copy_language(text: str) -> bool:
    return any(pattern.search(text) for pattern in DIRECT_COPY_PATTERNS)


def lint_record(record: dict[str, Any], ledger_blocklist: list[str]) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    example_id = record.get("example_id")
    required_fields = [
        "example_id",
        "source_role",
        "example_scope",
        "what_worked",
        "why_it_worked",
        "what_failed",
        "why_it_failed",
        "transferable_principle",
        "non_transferable_content",
        "anti_overfit_rule",
        "validation_check",
        "regression_fixture",
        "promotion_status",
        "confidence",
    ]
    for field in required_fields:
        value = record.get(field)
        if isinstance(value, list):
            missing = not as_non_empty_list(value)
        else:
            missing = value in ("", None)
        if missing:
            failures.append({"type": "example_review_record_missing_field", "example_id": example_id, "field": field})

    for field in ["what_worked", "why_it_worked", "what_failed", "why_it_failed"]:
        if not as_non_empty_list(record.get(field)):
            failures.append({"type": "example_review_record_missing_analysis", "example_id": example_id, "field": field})

    record_blocklist = as_non_empty_list(record.get("non_transferable_content"))
    if not record_blocklist:
        failures.append({"type": "example_review_record_missing_blocklist", "example_id": example_id})

    principle = str(record.get("transferable_principle") or "")
    if has_direct_copy_language(principle):
        failures.append({"type": "direct_example_to_skill_language", "example_id": example_id})

    full_blocklist = [*ledger_blocklist, *record_blocklist]
    blocked_hit = contains_blocked_content(principle, full_blocklist)
    if blocked_hit:
        failures.append({"type": "blocked_content_in_transferable_principle", "example_id": example_id, "blocked_item": blocked_hit})

    promotion_status = str(record.get("promotion_status") or "")
    if promotion_status in ACCEPTED_STATUSES:
        destinations = [
            *as_non_empty_list(record.get("affected_protocols")),
            *as_non_empty_list(record.get("affected_scripts")),
        ]
        if not destinations:
            failures.append({"type": "accepted_rule_missing_destination", "example_id": example_id})
        for field in ["validation_check", "regression_fixture", "anti_overfit_rule"]:
            if not str(record.get(field) or "").strip():
                failures.append({"type": "accepted_rule_missing_gate_field", "example_id": example_id, "field": field})
        for field in ["validation_check", "regression_fixture"]:
            blocked_hit = contains_blocked_content(str(record.get(field) or ""), full_blocklist)
            if blocked_hit:
                failures.append({"type": "blocked_content_in_promotion_gate", "example_id": example_id, "field": field, "blocked_item": blocked_hit})

    return failures


def lint_ledger(ledger: dict[str, Any]) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    if ledger.get("object_type") != "ExampleReviewLedger":
        failures.append({"type": "wrong_object_type", "object_type": ledger.get("object_type")})
    records = ledger.get("records")
    if not isinstance(records, list) or not records:
        failures.append({"type": "example_review_ledger_missing_records"})
        records = []

    ledger_blocklist = as_non_empty_list(ledger.get("non_transferable_content"))
    seen: set[str] = set()
    for record in records:
        if not isinstance(record, dict):
            failures.append({"type": "example_review_record_not_object"})
            continue
        example_id = str(record.get("example_id") or "")
        if example_id in seen:
            failures.append({"type": "duplicate_example_review_record", "example_id": example_id})
        seen.add(example_id)
        failures.extend(lint_record(record, ledger_blocklist))

    summary = ledger.get("promotion_summary")
    if not isinstance(summary, dict):
        failures.append({"type": "promotion_summary_missing"})
    elif summary.get("accepted_count", 0) > 0 and not any(
        isinstance(record, dict) and record.get("promotion_status") == "accepted" for record in records
    ):
        failures.append({"type": "promotion_summary_acceptance_mismatch"})

    if ledger.get("qa_status") not in {"pass", "warning", "fail"}:
        failures.append({"type": "invalid_qa_status", "qa_status": ledger.get("qa_status")})

    return {
        "pass": not failures,
        "counts": {
            "records": len(records),
            "ledger_blocklist_items": len(ledger_blocklist),
            "accepted_records": sum(1 for record in records if isinstance(record, dict) and record.get("promotion_status") == "accepted"),
        },
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = lint_ledger(load_json(args.ledger))
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
