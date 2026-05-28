#!/usr/bin/env python3
"""Validate runtime ontology objects, links, and publish gates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ID_FIELDS = {
    "UserExamPrepRequest": "request_id",
    "UserConstraint": "constraint_id",
    "SourceCoverageMap": "coverage_id",
    "GateResult": "gate_result_id",
    "OutputView": "view_id",
    "WorkflowPlan": "plan_id",
    "LectureModule": "module_id",
    "KnowledgeWalkthroughPlan": "walkthrough_id",
    "SourceDocument": "source_id",
    "ExampleReviewLedger": "ledger_id",
    "TransferableRuleSet": "rule_set_id",
    "NonTransferableContentBlocklist": "blocklist_id",
    "ExampleTransferQA": "qa_id",
    "SourceFragment": "fragment_id",
    "FragmentPartition": "partition_id",
    "AssessmentRegime": "regime_id",
    "ExamBlueprint": "blueprint_id",
    "PastPaperQuestion": "question_id",
    "KnowledgePoint": "kp_id",
    "ExaminerOperation": "operation_id",
    "QuestionArchetype": "archetype_id",
    "SlotGrammar": "slot_grammar_id",
    "EvidenceClaim": "claim_id",
    "ReadingSource": "reading_id",
    "PracticalOperation": "operation_id",
    "MethodBlock": "method_block_id",
    "MCQScoringPolicy": "policy_id",
    "ShortAnswerVariant": "variant_id",
    "EssayCoveragePlan": "plan_id",
    "PrepArtifact": "artifact_id",
    "QAFlag": "flag_id",
    "WorkflowRun": "run_id",
    "RunManifest": "run_id",
    "LineageEvent": "event_id",
}

FILE_TYPE_HINTS = {
    "user_exam_prep_requests": "UserExamPrepRequest",
    "user_constraints": "UserConstraint",
    "source_coverage_maps": "SourceCoverageMap",
    "gate_results": "GateResult",
    "output_views": "OutputView",
    "workflow_plans": "WorkflowPlan",
    "lecture_modules": "LectureModule",
    "knowledge_walkthrough_plans": "KnowledgeWalkthroughPlan",
    "source_documents": "SourceDocument",
    "example_review_ledgers": "ExampleReviewLedger",
    "transferable_rule_sets": "TransferableRuleSet",
    "non_transferable_content_blocklists": "NonTransferableContentBlocklist",
    "example_transfer_qas": "ExampleTransferQA",
    "source_fragments": "SourceFragment",
    "fragment_partitions": "FragmentPartition",
    "assessment_regimes": "AssessmentRegime",
    "exam_blueprints": "ExamBlueprint",
    "past_paper_questions": "PastPaperQuestion",
    "knowledge_points": "KnowledgePoint",
    "examiner_operations": "ExaminerOperation",
    "question_archetypes": "QuestionArchetype",
    "slot_grammars": "SlotGrammar",
    "evidence_claims": "EvidenceClaim",
    "reading_sources": "ReadingSource",
    "practical_operations": "PracticalOperation",
    "method_blocks": "MethodBlock",
    "mcq_scoring_policies": "MCQScoringPolicy",
    "short_answer_variants": "ShortAnswerVariant",
    "essay_coverage_plans": "EssayCoveragePlan",
    "prep_artifacts": "PrepArtifact",
    "qa_flags": "QAFlag",
    "run_manifests": "RunManifest",
    "lineage_events": "LineageEvent",
}

PUBLIC_HELPER_PATTERNS = (
    "internal_qa",
    "ontology_objects",
    "ontology_links",
    "source_map",
    "run_manifest",
    "example_essay_manifest",
    "lineage_events",
    "lineage_report",
    "source_audit",
)

GENERATED_FROM_LINK_TYPES = {
    "GENERATED_FROM",
    "GENERATED_FROM_KP",
    "GENERATED_FROM_LECTURE_MODULE",
    "GENERATED_FROM_MCQ_POLICY",
    "GENERATED_FROM_SHORT_ANSWER_VARIANT",
    "GENERATED_FROM_ESSAY_COVERAGE_PLAN",
    "GENERATED_FROM_METHOD_BLOCK",
    "GENERATED_FROM_PRACTICAL_OPERATION",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.strip():
            row = json.loads(line)
            row["_source_file"] = str(path)
            row["_line_no"] = line_no
            rows.append(row)
    return rows


def infer_type(path: Path, row: dict[str, Any]) -> str | None:
    if row.get("object_type"):
        return str(row["object_type"])
    stem = path.stem
    for key, object_type in FILE_TYPE_HINTS.items():
        if key in stem:
            return object_type
    return None


def collect_objects(objects_dir: Path) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    objects: dict[str, dict[str, Any]] = {}
    failures: list[dict[str, Any]] = []
    if not objects_dir.exists():
        return objects, [{"type": "objects_dir_missing", "path": str(objects_dir)}]
    for path in sorted(objects_dir.rglob("*")):
        if not path.is_file() or path.suffix not in {".json", ".jsonl"}:
            continue
        rows = read_jsonl(path) if path.suffix == ".jsonl" else normalize_json_objects(path, load_json(path))
        for row in rows:
            object_type = infer_type(path, row)
            if not object_type:
                failures.append({"type": "object_type_unknown", "path": str(path), "row": row.get("_line_no")})
                continue
            row["object_type"] = object_type
            id_field = ID_FIELDS.get(object_type)
            object_id = row.get(id_field) if id_field else None
            if not object_id:
                failures.append({"type": "object_id_missing", "object_type": object_type, "id_field": id_field, "path": str(path)})
                continue
            if str(object_id) in objects:
                failures.append({"type": "duplicate_object_id", "object_id": str(object_id), "path": str(path)})
                continue
            objects[str(object_id)] = row
    return objects, failures


def normalize_json_objects(path: Path, data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        rows = data
    elif isinstance(data, dict):
        for key in ("objects", "partitions", "questions", "archetypes", "artifacts", "qa_flags"):
            if isinstance(data.get(key), list):
                rows = data[key]
                break
        else:
            rows = [data]
    else:
        rows = []
    normalized = []
    for row in rows:
        if isinstance(row, dict):
            row = dict(row)
            row["_source_file"] = str(path)
            normalized.append(row)
    return normalized


def collect_links(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if not path.exists():
        return [], [{"type": "links_file_missing", "path": str(path)}]
    rows = read_jsonl(path) if path.suffix == ".jsonl" else normalize_json_objects(path, load_json(path))
    return rows, []


def load_contract(path: Path) -> dict[str, Any]:
    return load_json(path)


def required_property_failures(objects: dict[str, dict[str, Any]], contract: dict[str, Any]) -> list[dict[str, Any]]:
    failures = []
    object_types = contract.get("object_types", {})
    for object_id, row in objects.items():
        object_type = row["object_type"]
        required = object_types.get(object_type, {}).get("required_properties", [])
        missing = [key for key in required if key not in row]
        if missing:
            failures.append({"type": "object_missing_required_properties", "object_id": object_id, "object_type": object_type, "missing": missing})
    return failures


def context_for_object(object_id: str, objects: dict[str, dict[str, Any]]) -> dict[str, Any]:
    row = objects.get(object_id, {})
    if row.get("object_type") == "SourceFragment" and row.get("source_id") in objects:
        return objects[str(row["source_id"])]
    return row


def link_failures(links: list[dict[str, Any]], objects: dict[str, dict[str, Any]], contract: dict[str, Any]) -> list[dict[str, Any]]:
    failures = []
    link_types = contract.get("link_types", {})
    for link in links:
        link_type = link.get("link_type")
        from_id = str(link.get("from_id"))
        to_id = str(link.get("to_id"))
        if not link.get("link_id"):
            failures.append({"type": "link_id_missing", "link": link})
        if link_type not in link_types:
            failures.append({"type": "link_type_unknown", "link_id": link.get("link_id"), "link_type": link_type})
            continue
        from_object = objects.get(from_id)
        to_object = objects.get(to_id)
        if from_object is None:
            failures.append({"type": "link_from_object_missing", "link_id": link.get("link_id"), "from_id": from_id})
            continue
        if to_object is None:
            failures.append({"type": "link_to_object_missing", "link_id": link.get("link_id"), "to_id": to_id})
            continue
        expected = link_types[link_type]
        if from_object.get("object_type") != expected.get("from"):
            failures.append({"type": "link_from_type_mismatch", "link_id": link.get("link_id"), "expected": expected.get("from"), "actual": from_object.get("object_type")})
        if to_object.get("object_type") != expected.get("to"):
            failures.append({"type": "link_to_type_mismatch", "link_id": link.get("link_id"), "expected": expected.get("to"), "actual": to_object.get("object_type")})

        source_context = context_for_object(from_id, objects)
        if source_context.get("analysis_context") in {"cross_target_example", "benchmark_fixture"} and link_type in {"SUPPORTS_KP", "SUPPORTS_CLAIM", *GENERATED_FROM_LINK_TYPES}:
            failures.append({"type": "cross_target_or_benchmark_support_link", "link_id": link.get("link_id"), "link_type": link_type})
        if source_context.get("analysis_context") == "target_old_or_different_regime" and link_type == "DEFINES_BLUEPRINT":
            failures.append({"type": "old_regime_defines_current_blueprint", "link_id": link.get("link_id")})
        if source_context.get("extraction_status") == "unreadable" and link_type == "SUPPORTS_KP":
            failures.append({"type": "unreadable_source_supports_kp", "link_id": link.get("link_id")})
        if source_context.get("verification_status") in {"candidate", "unverified", "not_verified"} and link_type == "SUPPORTS_CLAIM":
            failures.append({"type": "unverified_source_supports_claim", "link_id": link.get("link_id")})
    return failures


def publish_gate_failures(objects: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    failures = []
    blocking_flags = {
        object_id: row
        for object_id, row in objects.items()
        if row.get("object_type") == "QAFlag"
        and row.get("severity") == "blocking"
        and row.get("resolution_status") not in {"resolved", "waived_with_reason"}
    }
    for object_id, row in objects.items():
        if row.get("object_type") != "PrepArtifact" or not row.get("student_visible"):
            continue
        if not row.get("source_links"):
            failures.append({"type": "student_visible_artifact_without_source_links", "artifact_id": object_id})
        if row.get("qa_status") != "pass":
            failures.append({"type": "student_visible_artifact_without_passed_qa", "artifact_id": object_id, "qa_status": row.get("qa_status")})
        artifact_path = str(row.get("path") or row.get("artifact_path") or "")
        if any(pattern in artifact_path for pattern in PUBLIC_HELPER_PATTERNS):
            failures.append({"type": "student_visible_artifact_points_to_helper_file", "artifact_id": object_id, "path": artifact_path})
        for flag_id, flag in blocking_flags.items():
            if flag.get("blocked_object") in {object_id, row.get("artifact_id")}:
                failures.append({"type": "blocking_flag_blocks_artifact", "artifact_id": object_id, "flag_id": flag_id})
    return failures


def validate(objects_dir: Path, links_path: Path, ontology_path: Path) -> dict[str, Any]:
    contract = load_contract(ontology_path)
    objects, failures = collect_objects(objects_dir)
    links, link_read_failures = collect_links(links_path)
    failures.extend(link_read_failures)
    failures.extend(required_property_failures(objects, contract))
    failures.extend(link_failures(links, objects, contract))
    failures.extend(publish_gate_failures(objects))
    return {
        "pass": not failures,
        "counts": {
            "objects": len(objects),
            "links": len(links),
        },
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--objects-dir", type=Path, required=True)
    parser.add_argument("--links", type=Path, required=True)
    parser.add_argument("--ontology", type=Path, default=Path("ontology/ontology.json"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = validate(args.objects_dir, args.links, args.ontology)
    except Exception as exc:
        result = {"pass": False, "failures": [{"type": "validator_error", "error": str(exc)}]}
    text = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
