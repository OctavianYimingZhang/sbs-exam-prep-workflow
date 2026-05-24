#!/usr/bin/env python3
"""Validate the setup, planning, and readiness contract files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "agents/presets.yaml",
    "agents/prompt_cards.yaml",
    "agents/setup_wizard.yaml",
    "schemas/skill_config.schema.json",
    "schemas/workflow_action.schema.json",
    "schemas/workflow_plan.schema.json",
    "schemas/input_readiness_report.schema.json",
    "schemas/run_status.schema.json",
    "schemas/prompt_card.schema.json",
    "scripts/plan_workflow.py",
    "scripts/input_readiness_check.py",
    "scripts/render_workflow_plan.py",
    "scripts/run_status_report.py",
    "scripts/lineage_report.py",
    "references/interactive_setup_protocol.md",
    "references/best_usage_guide.md",
]

REQUIRED_PRESETS = {
    "source_inventory_only",
    "exam_format_diagnosis",
    "full_excel_workbook",
    "past_paper_prediction",
    "mcq_prep",
    "short_answer_prep",
    "practical_data_problem_prep",
    "project_scenario_long_answer",
    "essay_theme_plan",
    "example_essay_docx",
    "audit_lint_only",
    "github_ready_qa",
}

REQUIRED_LINKS = {
    "GENERATED_FROM_KP",
    "GENERATED_FROM_MCQ_POLICY",
    "GENERATED_FROM_SHORT_ANSWER_VARIANT",
    "GENERATED_FROM_ESSAY_COVERAGE_PLAN",
    "GENERATED_FROM_METHOD_BLOCK",
    "GENERATED_FROM_PRACTICAL_OPERATION",
}

REQUIRED_ID_FIELDS = {
    "MethodBlock": "method_block_id",
    "MCQScoringPolicy": "policy_id",
    "ShortAnswerVariant": "variant_id",
    "EssayCoveragePlan": "plan_id",
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

    ontology = load_json(root / "ontology/ontology.json")
    object_types = ontology.get("object_types", {})
    link_types = set(ontology.get("link_types", {}))
    action_types = set(ontology.get("action_types", {}))
    validation_rules = set(ontology.get("validation_rules", []))
    query_templates = set(ontology.get("query_templates", {}))

    if "WorkflowPlan" not in object_types:
        failures.append({"type": "missing_workflow_plan_object"})
    if "PlanWorkflow" not in action_types:
        failures.append({"type": "missing_plan_workflow_action"})
    for link in sorted(REQUIRED_LINKS - link_types):
        failures.append({"type": "missing_typed_generated_from_link", "link_type": link})
    for object_name, id_field in REQUIRED_ID_FIELDS.items():
        required = object_types.get(object_name, {}).get("required_properties", [])
        if id_field not in required:
            failures.append({"type": "missing_object_id_field", "object_type": object_name, "id_field": id_field})
    if "workflow_plan_precedes_execution" not in validation_rules:
        failures.append({"type": "missing_workflow_plan_validation_rule"})
    if "workflow_plan_preview" not in query_templates:
        failures.append({"type": "missing_workflow_plan_query_template"})

    workflow_schema = load_json(root / "schemas/workflow_plan.schema.json")
    workflow_required = set(workflow_schema.get("required", []))
    for field in {
        "plan_id",
        "request_scope",
        "selected_preset",
        "target_group_key",
        "source_inventory_required",
        "fragment_index_required",
        "actions",
        "skipped_modules",
        "blockers",
        "publish_gate",
    } - workflow_required:
        failures.append({"type": "workflow_plan_schema_missing_required_field", "field": field})
    actions_items = workflow_schema.get("properties", {}).get("actions", {}).get("items", {})
    if actions_items.get("$ref") != "workflow_action.schema.json":
        failures.append({"type": "workflow_plan_schema_missing_action_ref"})

    skill_schema = load_json(root / "schemas/skill_config.schema.json")
    enum = set(skill_schema.get("properties", {}).get("output_mode", {}).get("properties", {}).get("preset", {}).get("enum", []))
    missing_presets = sorted(REQUIRED_PRESETS - enum)
    if missing_presets:
        failures.append({"type": "skill_config_schema_missing_presets", "items": missing_presets})

    preset_text = read(root / "agents/presets.yaml")
    for preset in sorted(REQUIRED_PRESETS):
        if preset not in preset_text:
            failures.append({"type": "preset_missing_from_agents_file", "preset": preset})

    combined_docs = "\n".join(
        read(root / path)
        for path in [
            "SKILL.md",
            "README.md",
            "references/interactive_setup_protocol.md",
            "references/best_usage_guide.md",
        ]
        if (root / path).exists()
    )
    for term in ["SkillConfig", "WorkflowPlan", "InputReadinessReport", "Plan Preview"]:
        if term not in combined_docs:
            failures.append({"type": "planning_term_missing_from_docs", "term": term})

    return {
        "pass": not failures,
        "counts": {
            "required_files": len(REQUIRED_FILES),
            "required_presets": len(REQUIRED_PRESETS),
            "typed_generated_from_links": len(REQUIRED_LINKS),
        },
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
