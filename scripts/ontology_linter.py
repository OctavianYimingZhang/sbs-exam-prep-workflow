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
    "WorkflowPlan",
    "LectureModule",
    "KnowledgeWalkthroughPlan",
    "CourseSection",
    "LectureSession",
    "LectureConceptModule",
    "ExamEmphasisProfile",
    "ExamPrepNotesPlan",
    "QuestionTypeAddOn",
    "VisualAidSpec",
    "GeneratedVisualAid",
    "SourceDocument",
    "ExampleReviewLedger",
    "TransferableRuleSet",
    "NonTransferableContentBlocklist",
    "ExampleTransferQA",
    "SourceFragment",
    "FragmentPartition",
    "AssessmentRegime",
    "ExamBlueprint",
    "PastPaperQuestion",
    "KnowledgePoint",
    "AtomicKnowledgeLedger",
    "AtomicKnowledgeUnit",
    "SourceBaselineNotesPlan",
    "KnowledgeOnlyStudentView",
    "ExamOverlayPass",
    "PublicOutputPoint",
    "PublicPointBlock",
    "OutputLanguageProfile",
    "RouteDocxStyleProfile",
    "RenderDecision",
    "PointCoverageBinding",
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
    "EXAMPLE_REVIEW_USES_SOURCE",
    "RULE_SET_DERIVED_FROM_REVIEW",
    "BLOCKLIST_DERIVED_FROM_REVIEW",
    "EXAMPLE_QA_CHECKS_RULE_SET",
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
    "SUPPORTS_LECTURE_MODULE",
    "SUPPORTS_COURSE_SECTION",
    "MAPS_TO_LECTURE_SESSION",
    "HAS_LECTURE_CONCEPT_MODULE",
    "SUPPORTS_LECTURE_CONCEPT_MODULE",
    "MAPS_KP_TO_EXAM_EMPHASIS",
    "LEDGER_DECOMPOSES_FRAGMENT",
    "LEDGER_HAS_ATOMIC_UNIT",
    "LEDGER_BINDS_KP",
    "BASELINE_USES_ATOMIC_LEDGER",
    "BASELINE_COVERS_KP",
    "OVERLAY_USES_BASELINE",
    "OVERLAY_USES_EXAM_EMPHASIS",
    "VIEW_FILTERS_BASELINE",
    "VIEW_APPLIES_OVERLAY",
    "VIEW_SELECTS_PUBLIC_POINT",
    "PLAN_HAS_PUBLIC_POINT",
    "PUBLIC_POINT_HAS_BLOCK",
    "PUBLIC_POINT_COVERS_ATOMIC_UNIT",
    "PUBLIC_BLOCK_COVERS_ATOMIC_UNIT",
    "OUTPUT_VIEW_USES_LANGUAGE_PROFILE",
    "PREP_ARTIFACT_USES_DOCX_STYLE_PROFILE",
    "RENDER_DECISION_HIDES_INTERNAL_FIELD",
    "RENDER_DECISION_RENDERS_BLOCK",
    "POINT_COVERAGE_BINDS_PUBLIC_POINT",
    "PLAN_USES_EXAM_EMPHASIS",
    "VISUAL_AID_FOR_KP",
    "GENERATED_FROM_VISUAL_AID_SPEC",
    "GENERATED_FROM",
    "GENERATED_FROM_KP",
    "GENERATED_FROM_LECTURE_MODULE",
    "GENERATED_FROM_EXAM_PREP_NOTES_PLAN",
    "VISUAL_AID_ATTACHED_TO",
    "GENERATED_FROM_MCQ_POLICY",
    "GENERATED_FROM_SHORT_ANSWER_VARIANT",
    "GENERATED_FROM_ESSAY_COVERAGE_PLAN",
    "GENERATED_FROM_METHOD_BLOCK",
    "GENERATED_FROM_PRACTICAL_OPERATION",
    "BLOCKS",
    "HAS_MANIFEST",
    "EMITS_LINEAGE",
}

REQUIRED_ACTION_TYPES = {
    "ParseUserExamPrepRequest",
    "BuildSourceCoverageMap",
    "SelectOutputView",
    "RecordGateResult",
    "PlanWorkflow",
    "CreateSourceInventory",
    "ExtractFragments",
    "BuildFragmentIndex",
    "AnalyzeExamplesIntoTransferableRules",
    "SynthesizeTransferableRules",
    "RunRulePromotionGate",
    "LintExampleTransfer",
    "BuildLectureModules",
    "BuildKnowledgeWalkthroughPlan",
    "ReconstructCourseSections",
    "MapLectureSessions",
    "BuildLectureConceptModules",
    "BuildAtomicKnowledgeLedger",
    "BuildSourceBaselineNotesPlan",
    "RunBaselineCoverageFloorQA",
    "BuildExamEmphasisProfile",
    "ApplyExamOverlayPass",
    "RunOverlayCoverageQA",
    "BuildKnowledgeOnlyStudentView",
    "SelectOutputLanguageProfile",
    "SelectRouteDocxStyleProfile",
    "BuildPublicOutputPoints",
    "BindAtomicItemsToPublicPoints",
    "LintPublicOutputPoints",
    "LintOutputLanguageNeutrality",
    "BuildExamPrepNotesPlan",
    "BuildQuestionTypeAddOns",
    "PlanVisualAid",
    "GenerateVisualAid",
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
    "workflow_plan_precedes_execution",
    "student_facing_output_filter_applied",
    "exam_prep_notes_reconstruct_before_rewrite",
    "student_or_unknown_note_requires_verification_for_factual_claim",
    "question_type_addon_after_base_notes",
    "generated_visual_aid_is_not_evidence",
    "knowledge_walkthrough_docx_is_lecture_first",
    "question_type_reports_hide_internal_reasoning",
    "blocking_gap_asks_one_question_or_marks_blocked",
    "output_view_does_not_break_evidence_rules",
    "exact_future_question_wording_not_claimed",
    "short_answer_variants_require_slot_grammar",
    "mcq_official_answer_requires_answer_key",
    "external_reading_claim_requires_verified_source",
    "old_regime_evidence_cannot_raise_current_confidence_above_medium",
    "student_output_excludes_internal_helper_artifacts",
    "public_output_points_hide_internal_card_fields",
    "output_language_profile_required_for_public_output",
    "route_specific_docx_style_profile_required",
    "exam_prep_notes_compact_style_not_essay_style",
    "protected_atomic_item_bound_to_public_point",
    "ordinary_notes_hide_exam_use_trap_and_must_master_headings",
    "example_review_required_before_rule_promotion",
    "example_rules_must_strip_source_identity",
    "examples_cannot_support_target_facts_or_predictions",
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

    for template in [
        "source_coverage_card",
        "output_view_selection",
        "workflow_plan_preview",
        "student_output_filter",
        "exam_prep_notes_docx",
        "knowledge_walkthrough_docx",
        "essay_exam_prep",
        "mcq_exam_prep",
        "long_answer_project_scenario_prep",
        "extra_reading_insert",
    ]:
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
