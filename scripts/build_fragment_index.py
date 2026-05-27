#!/usr/bin/env python3
"""Build request-prunable fragment partitions from source inventory metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


QUESTION_TYPE_FEATURES = {
    "mcq_or_single_best": "mcq",
    "short_answer": "short_answer",
    "essay_question": "essay",
    "problem_data_case": "data_problem",
    "practical_protocol": "practical_protocol",
}

ROLE_CONCEPT_TYPES = {
    "lecture_slide": "course_mechanism",
    "lecture_note": "course_mechanism",
    "annotated_lecture_slide": "course_mechanism",
    "student_typed_note": "student_note_hint",
    "student_handwritten_note": "student_note_hint",
    "structured_revision_note": "student_note_hint",
    "ai_generated_note": "unsupported_note",
    "formal_past_paper": "exam_question",
    "formal_past_paper_with_answers": "exam_question",
    "practical_protocol": "method_operation",
    "reading_list": "extra_reading",
    "marking_criteria": "assessment_rule",
    "essay_guidance": "assessment_rule",
    "exemplar_answer": "style_example",
    "exemplar_image": "style_example",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + ("\n" if rows else ""), encoding="utf-8")


def stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()


def source_hash(row: dict[str, Any]) -> str:
    path = Path(str(row.get("path") or ""))
    if path.exists() and path.is_file():
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(65536), b""):
                digest.update(chunk)
        return digest.hexdigest()
    payload = json.dumps(
        {
            "path": row.get("path"),
            "name": row.get("name"),
            "role": row.get("role"),
            "status": row.get("status"),
            "char_count": row.get("char_count"),
            "preview": row.get("preview"),
        },
        sort_keys=True,
        ensure_ascii=False,
    )
    return stable_hash(payload)


def allowed_evidence_use(row: dict[str, Any]) -> list[str]:
    uses = []
    if row.get("allowed_factual_use"):
        uses.append("factual_course_content")
    if row.get("allowed_prediction_use"):
        uses.append("current_prediction_evidence")
    if row.get("allowed_style_use"):
        uses.append("style_evidence")
    if row.get("allowed_layout_use"):
        uses.append("layout_evidence")
    if row.get("allowed_transferable_example_use"):
        uses.append("transferable_workflow_rule")
    if row.get("evidence_use") and row.get("evidence_use") not in uses:
        uses.append(str(row["evidence_use"]))
    return uses


def question_type_from_features(features: list[str], role: str) -> str | None:
    if role in {"formal_past_paper", "formal_past_paper_with_answers", "practice_paper", "mock_exam"}:
        for feature, qtype in QUESTION_TYPE_FEATURES.items():
            if feature in features:
                return qtype
        return "mixed_or_unknown"
    if role == "practical_protocol":
        return "practical_protocol"
    if role == "essay_guidance":
        return "essay"
    return None


def confidence_from_status(status: str) -> str:
    if status == "ok":
        return "High"
    if status == "partial":
        return "Medium"
    return "Low"


def source_document(row: dict[str, Any], index: int, digest: str) -> dict[str, Any]:
    source_id = row.get("source_id") or f"SRC{index:04d}"
    return {
        "object_type": "SourceDocument",
        "source_id": source_id,
        "path": row.get("path"),
        "file_role": row.get("role"),
        "trust_level": row.get("source_trust_level"),
        "analysis_context": row.get("analysis_context"),
        "allowed_evidence_use": allowed_evidence_use(row),
        "extraction_status": row.get("status"),
        "source_hash": digest,
        "text_path": row.get("text_path"),
        "target_group_key": row.get("target_code") or row.get("target_name"),
    }


def source_partition(row: dict[str, Any], source_id: str, index: int, digest: str) -> dict[str, Any]:
    features = row.get("source_features") or []
    role = str(row.get("role") or "unknown")
    return {
        "object_type": "FragmentPartition",
        "partition_id": f"PART{index:04d}",
        "source_id": source_id,
        "fragment_ids": [f"{source_id}:full_text"] if row.get("char_count", 0) else [],
        "source_role": role,
        "analysis_context": row.get("analysis_context"),
        "target_group_key": row.get("target_code") or row.get("target_name"),
        "exam_regime": row.get("analysis_context") if "regime" in str(row.get("analysis_context")) else None,
        "year": row.get("year"),
        "lecture_or_module": row.get("target_name"),
        "question_type": question_type_from_features(features, role),
        "concept_type": ROLE_CONCEPT_TYPES.get(role, "unknown"),
        "command_verbs": [],
        "input_format": None,
        "image_count": row.get("image_count"),
        "extraction_confidence": confidence_from_status(str(row.get("status") or "")),
        "allowed_evidence_use": allowed_evidence_use(row),
        "source_hash": digest,
    }


def question_partitions(path: Path, start_index: int) -> list[dict[str, Any]]:
    if not path:
        return []
    data = load_json(path)
    if isinstance(data, dict):
        rows = data.get("questions", [])
    elif isinstance(data, list):
        rows = data
    else:
        rows = []
    partitions = []
    for offset, question in enumerate(rows, start=start_index):
        source_file = question.get("source_file") or "unknown"
        source_id = "SRCQ" + stable_hash(source_file)[:12]
        question_id = question.get("question_id") or f"{source_id}:Q{question.get('question_no', offset)}"
        partitions.append(
            {
                "object_type": "FragmentPartition",
                "partition_id": f"PART{offset:04d}",
                "source_id": source_id,
                "fragment_ids": [question_id],
                "source_role": "formal_past_paper_question",
                "analysis_context": "target_current_regime",
                "target_group_key": question.get("target_group_key"),
                "exam_regime": question.get("current_regime_key"),
                "year": question.get("year"),
                "lecture_or_module": None,
                "question_type": question.get("question_type"),
                "concept_type": "exam_question",
                "command_verbs": question.get("command_verbs") or [],
                "input_format": question.get("input_format"),
                "image_count": None,
                "extraction_confidence": question.get("extracted_confidence") or "Medium",
                "allowed_evidence_use": ["current_prediction_evidence"],
                "source_hash": stable_hash(json.dumps(question, sort_keys=True)),
            }
        )
    return partitions


def build(source_scan: Path, output_dir: Path, past_paper_questions: Path | None = None) -> dict[str, Any]:
    scan = load_json(source_scan)
    files = scan.get("files", [])
    source_documents = []
    partitions = []
    links = []
    for index, row in enumerate(files, start=1):
        digest = source_hash(row)
        doc = source_document(row, index, digest)
        partition = source_partition(row, doc["source_id"], index, digest)
        source_documents.append(doc)
        partitions.append(partition)
        links.append(
            {
                "link_id": f"LINK{index:04d}",
                "link_type": "PARTITIONED_AS",
                "from_id": doc["source_id"],
                "to_id": partition["partition_id"],
                "created_by_action": "BuildFragmentIndex",
            }
        )
    if past_paper_questions:
        partitions.extend(question_partitions(past_paper_questions, len(partitions) + 1))

    output_dir.mkdir(parents=True, exist_ok=True)
    object_dir = output_dir / "ontology_objects"
    link_dir = output_dir / "ontology_links"
    write_jsonl(object_dir / "source_documents.jsonl", source_documents)
    write_jsonl(object_dir / "fragment_partitions.jsonl", partitions)
    write_jsonl(link_dir / "links.jsonl", links)
    summary = {
        "status": "ok" if partitions else "empty",
        "source_scan": str(source_scan),
        "counts": {
            "source_documents": len(source_documents),
            "fragment_partitions": len(partitions),
            "links": len(links),
        },
        "partitions": partitions,
    }
    (output_dir / "fragment_partitions.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-scan", type=Path, required=True)
    parser.add_argument("--past-paper-questions", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result = build(args.source_scan, args.output_dir, args.past_paper_questions)
    print(json.dumps({"status": result["status"], **result["counts"], "output": str(args.output_dir)}, indent=2))
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
