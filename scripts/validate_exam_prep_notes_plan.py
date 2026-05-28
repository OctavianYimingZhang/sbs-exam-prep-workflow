#!/usr/bin/env python3
"""Validate ExamPrepNotesPlan coverage and student-visible knowledge cards."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = {
    "notes_plan_id",
    "target_group_key",
    "course_sections",
    "lecture_mapping",
    "knowledge_cards",
    "official_definition_records",
    "exam_emphasis_binding",
    "question_type_addons",
    "content_coverage_checks",
    "student_visible_structure",
    "forbidden_student_fields",
    "qa_flags",
    "qa_status",
}

REQUIRED_CARD_FIELDS = {
    "card_id",
    "kp_id",
    "section_id",
    "priority_label",
    "exam_function",
    "core_exam_claim",
    "exam_ready_synthesis",
    "source_anchors",
    "coverage_status",
    "student_visible",
}

ALLOWED_PRIORITY = {"必备", "重点", "补充"}
ALLOWED_COVERAGE = {"tested", "partially_tested", "fresh", "saturated", "unknown"}
ALLOWED_QA_STATUS = {"pass", "warn", "block"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def non_empty_list(value: Any) -> bool:
    return isinstance(value, list) and any(str(item).strip() for item in value)


def validate(plan: dict[str, Any]) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    for field in sorted(REQUIRED_TOP_LEVEL - set(plan)):
        failures.append({"type": "missing_top_level_field", "field": field})

    if plan.get("qa_status") not in ALLOWED_QA_STATUS:
        failures.append({"type": "invalid_qa_status", "qa_status": plan.get("qa_status")})

    if not isinstance(plan.get("course_sections"), list) or not plan.get("course_sections"):
        failures.append({"type": "course_sections_empty"})
    for section in plan.get("course_sections", []):
        if not isinstance(section, dict):
            failures.append({"type": "course_section_not_object"})
            continue
        if not non_empty_list(section.get("source_anchors")):
            failures.append({"type": "course_section_missing_source_anchors", "section_id": section.get("section_id")})

    if not isinstance(plan.get("lecture_mapping"), list) or not plan.get("lecture_mapping"):
        failures.append({"type": "lecture_mapping_empty"})
    for lecture in plan.get("lecture_mapping", []):
        if not isinstance(lecture, dict):
            failures.append({"type": "lecture_mapping_not_object"})
            continue
        if not non_empty_list(lecture.get("source_anchors")):
            failures.append({"type": "lecture_mapping_missing_source_anchors", "lecture_session_id": lecture.get("lecture_session_id")})

    cards = plan.get("knowledge_cards", [])
    if not isinstance(cards, list) or not cards:
        failures.append({"type": "knowledge_cards_empty"})
        cards = []
    for index, card in enumerate(cards, start=1):
        if not isinstance(card, dict):
            failures.append({"type": "knowledge_card_not_object", "index": index})
            continue
        for field in sorted(REQUIRED_CARD_FIELDS - set(card)):
            failures.append({"type": "knowledge_card_missing_field", "card_id": card.get("card_id"), "field": field})
        if card.get("student_visible") is True:
            if card.get("priority_label") not in ALLOWED_PRIORITY:
                failures.append({"type": "student_visible_card_invalid_priority", "card_id": card.get("card_id"), "priority_label": card.get("priority_label")})
            if not str(card.get("exam_function") or "").strip():
                failures.append({"type": "student_visible_card_missing_exam_function", "card_id": card.get("card_id")})
            if not non_empty_list(card.get("source_anchors")):
                failures.append({"type": "student_visible_card_missing_source_anchors", "card_id": card.get("card_id")})
            if card.get("coverage_status") not in ALLOWED_COVERAGE:
                failures.append({"type": "student_visible_card_invalid_coverage_status", "card_id": card.get("card_id"), "coverage_status": card.get("coverage_status")})

    emphasis = plan.get("exam_emphasis_binding", {})
    if not isinstance(emphasis, dict):
        failures.append({"type": "exam_emphasis_binding_not_object"})
    else:
        if "formal_papers_used" not in emphasis:
            failures.append({"type": "exam_emphasis_binding_missing_formal_papers_used"})
        if not isinstance(emphasis.get("compatible_question_types", []), list):
            failures.append({"type": "exam_emphasis_binding_question_types_not_list"})
        if not isinstance(emphasis.get("limitations", []), list):
            failures.append({"type": "exam_emphasis_binding_limitations_not_list"})

    checks = plan.get("content_coverage_checks", [])
    if not isinstance(checks, list) or not checks:
        failures.append({"type": "content_coverage_checks_empty"})
    for check in checks:
        if not isinstance(check, dict):
            failures.append({"type": "content_coverage_check_not_object"})
            continue
        if check.get("status") not in ALLOWED_QA_STATUS:
            failures.append({"type": "content_coverage_check_invalid_status", "check_id": check.get("check_id"), "status": check.get("status")})

    return {
        "pass": not failures,
        "counts": {
            "course_sections": len(plan.get("course_sections", [])) if isinstance(plan.get("course_sections"), list) else 0,
            "lecture_mapping": len(plan.get("lecture_mapping", [])) if isinstance(plan.get("lecture_mapping"), list) else 0,
            "knowledge_cards": len(cards),
            "content_coverage_checks": len(checks) if isinstance(checks, list) else 0,
        },
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = validate(load_json(args.plan))
    except Exception as exc:
        result = {"pass": False, "failures": [{"type": "read_error", "error": str(exc)}]}
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
