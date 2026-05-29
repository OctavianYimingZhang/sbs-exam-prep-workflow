#!/usr/bin/env python3
"""Validate the setup, planning, and readiness contract files."""

from __future__ import annotations

import argparse
import importlib.util
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
    "schemas/knowledge_walkthrough_plan.schema.json",
    "schemas/exam_prep_notes_plan.schema.json",
    "schemas/atomic_knowledge_ledger.schema.json",
    "schemas/example_review_ledger.schema.json",
    "schemas/exam_emphasis_profile.schema.json",
    "schemas/question_type_addon.schema.json",
    "schemas/visual_aid_spec.schema.json",
    "schemas/run_status.schema.json",
    "schemas/student_output_contract.schema.json",
    "schemas/prompt_card.schema.json",
    "scripts/plan_workflow.py",
    "scripts/input_readiness_check.py",
    "scripts/validate_exam_prep_notes_plan.py",
    "scripts/exam_prep_notes_linter.py",
    "scripts/example_transfer_linter.py",
    "scripts/exam_prep_docx_style_linter.py",
    "scripts/generate_exam_prep_notes_docx.py",
    "scripts/generate_knowledge_walkthrough_docx.py",
    "scripts/knowledge_walkthrough_linter.py",
    "scripts/render_workflow_plan.py",
    "scripts/run_status_report.py",
    "scripts/lineage_report.py",
    "references/interactive_setup_protocol.md",
    "references/best_usage_guide.md",
    "references/student_facing_output_policy.md",
    "references/exam_prep_notes_protocol.md",
    "references/essay_tutor_workflow_protocol.md",
    "references/visual_aid_generation_protocol.md",
    "references/knowledge_walkthrough_docx_protocol.md",
]

REQUIRED_PRESETS = {
    "source_inventory_only",
    "exam_format_diagnosis",
    "exam_prep_notes_docx",
    "knowledge_walkthrough_docx",
    "mcq_exam_prep",
    "short_answer_exam_prep",
    "long_answer_project_scenario_prep",
    "essay_exam_prep",
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


def load_planner_module(root: Path):
    planner_path = root / "scripts/plan_workflow.py"
    spec = importlib.util.spec_from_file_location("plan_workflow_contract_check", planner_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load plan_workflow.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
    for action in [
        "AnalyzeExamplesIntoTransferableRules",
        "SynthesizeTransferableRules",
        "RunRulePromotionGate",
        "LintExampleTransfer",
    ]:
        if action not in action_types:
            failures.append({"type": "missing_example_learning_action", "action_type": action})
    for action in [
        "BuildAtomicKnowledgeLedger",
        "BuildSourceBaselineNotesPlan",
        "RunBaselineCoverageFloorQA",
        "ApplyExamOverlayPass",
        "RunOverlayCoverageQA",
        "BuildKnowledgeOnlyStudentView",
        "SelectOutputLanguageProfile",
        "SelectRouteDocxStyleProfile",
        "BuildPublicOutputPoints",
        "BindAtomicItemsToPublicPoints",
        "LintPublicOutputPoints",
        "LintOutputLanguageNeutrality",
        "GenerateExamPrepNotesDocx",
        "LintExamPrepDocxStyle",
        "LintExamPrepNotes",
    ]:
        if action not in action_types:
            failures.append({"type": "missing_baseline_overlay_action", "action_type": action})
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

    plan_text = read(root / "scripts/plan_workflow.py")
    for optional_module in [
        "past_paper_questions",
        "question_archetypes",
        "examiner_operations",
        "example_learning",
        "transferable_rule_synthesis",
        "rule_promotion_gate",
        "example_transfer_linter",
    ]:
        if optional_module not in plan_text:
            failures.append({"type": "planner_missing_optional_module", "module": optional_module})
    for baseline_module in [
        "atomic_knowledge_ledger",
        "source_baseline_notes_plan",
        "baseline_coverage_floor_qa",
        "exam_overlay_pass",
        "overlay_did_not_damage_coverage_qa",
        "knowledge_only_student_view_filter",
        "output_language_profile",
        "route_docx_style_profile",
        "public_output_point_build",
        "point_coverage_binding",
        "public_output_point_linter",
        "output_language_neutrality_linter",
        "exam_prep_docx_style_linter",
        "exam_prep_notes_linter",
    ]:
        if baseline_module not in plan_text:
            failures.append({"type": "planner_missing_baseline_overlay_module", "module": baseline_module})
    try:
        planner = load_planner_module(root)
        available = {"any_source", "readable_course_notes", "formal_past_papers"}
        config = {"source_inputs": {"course_notes": ["fixture"], "formal_past_papers": ["fixture"]}}
        modules = planner.modules_for_preset("exam_prep_notes_docx", available, config)
        order = {module: index for index, module in enumerate(modules)}
        for module in ["exam_regime", "past_paper_questions", "question_archetypes", "examiner_operations"]:
            if order.get("baseline_coverage_floor_qa", 999) > order.get(module, -1):
                failures.append({"type": "past_paper_module_before_baseline_floor", "module": module})
            if order.get(module, 999) > order.get("exam_emphasis_profile", -1):
                failures.append({"type": "past_paper_module_after_exam_emphasis", "module": module})
        example_available = {"any_source", "readable_course_notes", "style_or_example_evidence"}
        example_config = {"source_inputs": {"course_notes": ["fixture"], "exemplars_or_feedback": ["fixture"]}}
        example_modules = planner.modules_for_preset("exam_prep_notes_docx", example_available, example_config)
        example_order = {module: index for index, module in enumerate(example_modules)}
        expected_chain = ["fragment_index", "example_learning", "transferable_rule_synthesis", "rule_promotion_gate", "example_transfer_linter", "course_section_reconstruction"]
        for left, right in zip(expected_chain, expected_chain[1:]):
            if example_order.get(left, 999) > example_order.get(right, -1):
                failures.append({"type": "example_learning_chain_order_invalid", "left": left, "right": right})
    except Exception as exc:
        failures.append({"type": "planner_order_check_error", "error": str(exc)})

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
    for term in ["SkillConfig", "WorkflowPlan", "InputReadinessReport", "Plan Preview", "knowledge_walkthrough_docx"]:
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
