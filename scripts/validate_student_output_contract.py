#!/usr/bin/env python3
"""Validate student-facing output policy files and contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "references/student_facing_output_policy.md",
    "references/knowledge_walkthrough_docx_protocol.md",
    "schemas/student_output_contract.schema.json",
    "schemas/knowledge_walkthrough_plan.schema.json",
    "scripts/generate_knowledge_walkthrough_docx.py",
    "scripts/knowledge_walkthrough_linter.py",
]

REQUIRED_PRESET = "knowledge_walkthrough_docx"

FORBIDDEN_VISIBLE_FIELDS = {
    "source_anchor",
    "confidence",
    "evidence",
    "examiner_operation",
    "discriminator_axis",
    "practice_mcq",
    "answer_key",
    "contrast_table",
    "separate_trap_bank",
    "mark_producing_schema",
    "reference_expansion",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate(root: Path) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    for rel_path in REQUIRED_FILES:
        if not (root / rel_path).exists():
            failures.append({"type": "missing_required_file", "path": rel_path})

    skill_schema = load_json(root / "schemas/skill_config.schema.json")
    workflow_schema = load_json(root / "schemas/workflow_plan.schema.json")
    for schema_name, schema in [("skill_config", skill_schema), ("workflow_plan", workflow_schema)]:
        enum = set(schema.get("properties", {}).get("output_mode", {}).get("properties", {}).get("preset", {}).get("enum", []))
        if schema_name == "workflow_plan":
            enum = set(schema.get("properties", {}).get("selected_preset", {}).get("enum", []))
        if REQUIRED_PRESET not in enum:
            failures.append({"type": "missing_knowledge_walkthrough_preset", "schema": schema_name})

    plan_text = read(root / "scripts/plan_workflow.py")
    if REQUIRED_PRESET not in plan_text:
        failures.append({"type": "planner_missing_knowledge_walkthrough"})

    policy = read(root / "references/student_facing_output_policy.md")
    walkthrough = read(root / "references/knowledge_walkthrough_docx_protocol.md")
    combined = policy + "\n" + walkthrough
    for term in ["MCQStudentPointCard", "ShortAnswerPointCard", "Knowledge Walkthrough", "Lecture Recap"]:
        if term not in combined:
            failures.append({"type": "student_policy_missing_term", "term": term})
    for field in sorted(FORBIDDEN_VISIBLE_FIELDS):
        if field not in combined:
            failures.append({"type": "student_policy_missing_forbidden_field", "field": field})

    contract = load_json(root / "schemas/student_output_contract.schema.json")
    contract_text = json.dumps(contract)
    for field in sorted(FORBIDDEN_VISIBLE_FIELDS):
        if field not in contract_text:
            failures.append({"type": "student_output_schema_missing_forbidden_field", "field": field})

    return {
        "pass": not failures,
        "counts": {"required_files": len(REQUIRED_FILES), "forbidden_visible_fields": len(FORBIDDEN_VISIBLE_FIELDS)},
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = validate(args.root)
    except Exception as exc:
        result = {"pass": False, "failures": [{"type": "read_error", "error": str(exc)}]}
    text = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
