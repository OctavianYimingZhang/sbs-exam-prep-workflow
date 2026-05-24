#!/usr/bin/env python3
"""Validate the operational ontology contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_OBJECT_TYPES = {
    "UserExamPrepRequest",
    "UserConstraint",
    "SourceCoverageMap",
    "GateResult",
    "OutputView",
    "SourceDocument",
    "SourceFragment",
    "FragmentPartition",
    "AssessmentRegime",
    "ExamBlueprint",
    "PastPaperQuestion",
    "KnowledgePoint",
    "ExaminerOperation",
    "QuestionArchetype",
    "SlotGrammar",
    "EvidenceClaim",
    "ReadingSource",
    "PracticalOperation",
    "MethodBlock",
    "MCQScoringPolicy",
    "ShortAnswerVariant",
    "EssayCoveragePlan",
    "PrepArtifact",
    "QAFlag",
    "WorkflowRun",
    "RunManifest",
    "LineageEvent",
}

REQUIRED_LINK_TYPES = {
    "CONTAINS",
    "PARTITIONED_AS",
    "GROUPS_FRAGMENT",
    "SUPPORTS_KP",
    "SUPPORTS_CLAIM",
    "INSTANTIATES",
    "USES_OPERATION",
    "HAS_SLOT_GRAMMAR",
    "COMPATIBLE_WITH",
    "DEFINES_BLUEPRINT",
    "ENRICHES_KP",
    "TESTS_KP",
    "GENERATED_FROM",
    "BLOCKS",
    "HAS_MANIFEST",
    "EMITS_LINEAGE",
}

REQUIRED_ACTION_TYPES = {
    "ParseUserExamPrepRequest",
    "BuildSourceCoverageMap",
    "SelectOutputView",
    "RecordGateResult",
    "CreateSourceInventory",
    "ExtractFragments",
    "BuildFragmentIndex",
    "NormalizeTargetGroup",
    "SplitExamRegime",
    "ExtractPastPaperQuestions",
    "ClassifyQuestionType",
    "InferQuestionArchetype",
    "SegmentKnowledgePoints",
    "BuildPracticalOperations",
    "BuildMethodBlocks",
    "BuildMCQScoringPolicy",
    "GenerateShortAnswerVariants",
    "BuildEssayCoveragePlan",
    "MapKPToArchetype",
    "VerifyReadingSource",
    "GeneratePrepArtifact",
    "CreateWorkflowRun",
    "ValidateOntologyRuntime",
    "WriteRunManifest",
    "RunDeliverableQA",
    "ApproveStudentOutput",
}

REQUIRED_VALIDATION_RULES = {
    "every_non_root_object_has_writer_action",
    "user_request_mode_selected_or_defaulted",
    "source_coverage_visible_before_generation",
    "blocking_gap_asks_one_question_or_marks_blocked",
    "output_view_does_not_break_evidence_rules",
    "exact_future_question_wording_not_claimed",
    "short_answer_variants_require_slot_grammar",
    "mcq_official_answer_requires_answer_key",
    "external_reading_claim_requires_verified_source",
    "old_regime_evidence_cannot_raise_current_confidence_above_medium",
    "student_output_excludes_internal_helper_artifacts",
    "lineage_required_for_publish",
    "blocking_qa_flag_blocks_publish",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_ontology(data: dict[str, Any]) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    object_types = data.get("object_types", {})
    link_types = data.get("link_types", {})
    action_types = data.get("action_types", {})
    validation_rules = set(data.get("validation_rules", []))

    missing_objects = sorted(REQUIRED_OBJECT_TYPES - set(object_types))
    if missing_objects:
        failures.append({"type": "missing_object_types", "items": missing_objects})

    for name, payload in object_types.items():
        required = payload.get("required_properties", [])
        if not isinstance(required, list) or not required:
            failures.append({"type": "object_missing_required_properties", "object_type": name})
        if name.endswith("Question") and "question_type" not in required:
            failures.append({"type": "question_object_missing_question_type", "object_type": name})

    missing_links = sorted(REQUIRED_LINK_TYPES - set(link_types))
    if missing_links:
        failures.append({"type": "missing_link_types", "items": missing_links})

    for name, payload in link_types.items():
        source = payload.get("from")
        target = payload.get("to")
        if source not in object_types:
            failures.append({"type": "link_source_unknown", "link_type": name, "source": source})
        if target not in object_types:
            failures.append({"type": "link_target_unknown", "link_type": name, "target": target})

    missing_actions = sorted(REQUIRED_ACTION_TYPES - set(action_types))
    if missing_actions:
        failures.append({"type": "missing_action_types", "items": missing_actions})

    object_names = set(object_types)
    link_names = set(link_types)
    writer_coverage: dict[str, list[str]] = {name: [] for name in object_names}
    for action_name, outputs in action_types.items():
        if not isinstance(outputs, list) or not outputs:
            failures.append({"type": "action_missing_outputs", "action_type": action_name})
            continue
        for output in outputs:
            if output in object_names:
                writer_coverage[output].append(action_name)
            elif output not in link_names:
                failures.append({"type": "action_writes_unknown_type", "action_type": action_name, "output": output})
    missing_writers = sorted(name for name, writers in writer_coverage.items() if not writers)
    if missing_writers:
        failures.append({"type": "object_without_writer_action", "items": missing_writers})

    forbidden_ids = {item.get("id") for item in data.get("forbidden_links", []) if isinstance(item, dict)}
    for required_id in {"no_cross_target_factual_claim", "old_regime_no_current_blueprint", "unverified_source_no_claim_support"}:
        if required_id not in forbidden_ids:
            failures.append({"type": "missing_forbidden_link_rule", "id": required_id})

    missing_rules = sorted(REQUIRED_VALIDATION_RULES - validation_rules)
    if missing_rules:
        failures.append({"type": "missing_validation_rules", "items": missing_rules})

    for template in ["source_coverage_card", "output_view_selection", "essay_theme", "mcq_prep", "data_problem_prep", "extra_reading_insert"]:
        if template not in data.get("query_templates", {}):
            failures.append({"type": "missing_query_template", "template": template})

    return {
        "pass": not failures,
        "counts": {
            "object_types": len(object_types),
            "link_types": len(link_types),
            "action_types": len(action_types),
            "validation_rules": len(validation_rules),
        },
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate ontology/ontology.json.")
    parser.add_argument("--ontology", type=Path, default=Path("ontology/ontology.json"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        result = validate_ontology(load_json(args.ontology))
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
