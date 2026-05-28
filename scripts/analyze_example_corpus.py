#!/usr/bin/env python3
"""Extract language deltas and ExampleReviewLedger records from external examples."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

try:
    from docx import Document  # type: ignore
except Exception:  # pragma: no cover
    Document = None

try:
    from extract_sources import SUPPORTED_EXTS as SOURCE_SUPPORTED_EXTS
    from extract_sources import detect_role, detect_source_features, extract_text
except Exception:  # pragma: no cover
    SOURCE_SUPPORTED_EXTS = set()
    detect_role = None
    detect_source_features = None
    extract_text = None


TEXT_EXTS = {".txt", ".md", ".markdown", ".json", ".yml", ".yaml"}
READABLE_EXTS = TEXT_EXTS | {".docx"} | set(SOURCE_SUPPORTED_EXTS)
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?")
PAGE_TRACE = re.compile(r"\b(Pages?|Slides?)\s+\d+\b", re.I)
META = re.compile(
    r"\b(this essay will|in this essay|in an essay answer|should be written as|use these pages|turn pages|"
    r"final\s+exam\s+thesis\s+should\s+be|the\s+answer\s+should\s+be|the\s+correct\s+conclusion\s+is)\b",
    re.I,
)
CITATION_STACK = re.compile(r"(?:\([A-Z][A-Za-z'’-]+(?:\s+et\s+al\.)?(?:,\s*|\s+)(?:19|20)\d{2}[a-z]?\).*){3,}")
EXAMPLE_WITHOUT_INFERENCE = re.compile(r"\b(for example|case study|case|firm|company|example)\b", re.I)
INFERENCE = re.compile(r"\b(shows|demonstrates|supports|suggests|therefore|implies|illustrates|evidence)\b", re.I)
LECTURE_ROUTE = re.compile(
    r"\b(?:the\s+)?(?:lecture|lectures|slides|source|chapter|section|module)\s+(?:\d+\s+)?"
    r"(?:establishes|establish|adds|add|introduces|introduce|covers|cover|moves from|move from|develops|develop|closes with|close with)\b",
    re.I,
)
SUPPORT_TO_CAUSE_OVERCLAIM = re.compile(
    r"\b(?:supports?|implicates?|suggests?|is consistent with|is associated with)\b[^.!?]{0,140}\b(?:the|a|single|sole)\s+cause\b",
    re.I,
)
LANGUAGE_DELTA_EXCLUDED_ROLES = {
    "formal_past_paper",
    "formal_past_paper_with_answers",
    "practical_protocol",
    "lecture_slide",
    "lecture_note",
    "annotated_lecture_slide",
    "reading_list",
    "marking_criteria",
}


def read_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in TEXT_EXTS:
        return path.read_text(encoding="utf-8", errors="replace")
    if suffix == ".docx":
        if Document is None:
            raise RuntimeError("python-docx is required to read .docx examples")
        doc = Document(path)
        return "\n\n".join(paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip())
    if extract_text is not None and suffix in SOURCE_SUPPORTED_EXTS:
        text, _method, _extra, _limitations = extract_text(path)
        return text
    return ""


def paragraphs(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]


def delta_id(source_id: str, problem: str, paragraph: str) -> str:
    digest = hashlib.sha1(f"{source_id}:{problem}:{paragraph[:120]}".encode("utf-8")).hexdigest()[:10]
    return f"delta_{digest}"


def make_delta(source_id: str, problem: str, better_pattern: str, rule: str, validation: str, severity: str, paragraph: str) -> dict[str, Any]:
    return {
        "delta_id": delta_id(source_id, problem, paragraph),
        "source_id": source_id,
        "observed_problem": problem,
        "better_pattern": better_pattern,
        "transferable_rule": rule,
        "applies_to": ["kp_synthesis", "example_essay"],
        "non_transferable_content": ["all example-specific factual claims, names, citations, dates, and recurrence details"],
        "validation_check": validation,
        "severity": severity,
    }


def analyse_paragraph(source_id: str, paragraph: str) -> list[dict[str, Any]]:
    deltas = []
    example_terms = len(EXAMPLE_WITHOUT_INFERENCE.findall(paragraph))
    if PAGE_TRACE.search(paragraph):
        deltas.append(
            make_delta(
                source_id,
                "slide_or_page_trace_used_as_student_prose",
                "Replace source tracing with direct claim -> mechanism/process/evidence -> consequence prose.",
                "Do not preserve coverage by narrating pages or slides inside answer prose.",
                "essay_style_linter page/slide trace patterns",
                "high",
                paragraph,
            )
        )
    if META.search(paragraph):
        deltas.append(
            make_delta(
                source_id,
                "how_to_write_or_metacommentary_inside_answer",
                "Write the answer paragraph itself, starting with the claim or problem.",
                "Student-facing prose must not tell the student how to write the answer.",
                "essay_style_linter how-to-write patterns",
                "high",
                paragraph,
            )
        )
    if LECTURE_ROUTE.search(paragraph):
        deltas.append(
            make_delta(
                source_id,
                "lecture_or_source_route_narration_inside_answer",
                "Rewrite source-route narration as direct claim -> mechanism/evidence -> interpretation prose.",
                "Final essay prose must answer the question rather than narrating how a lecture, source, or section was taught.",
                "example_essay_language_linter lecture_route_narration",
                "high",
                paragraph,
            )
        )
    if CITATION_STACK.search(paragraph):
        deltas.append(
            make_delta(
                source_id,
                "citation_stacking",
                "Keep only the most directly relevant citation or citations for the claim.",
                "Citations must be minimal and sufficient, not stacked to create authority.",
                "example_essay_language_linter citation_stack",
                "medium",
                paragraph,
            )
        )
    if SUPPORT_TO_CAUSE_OVERCLAIM.search(paragraph):
        deltas.append(
            make_delta(
                source_id,
                "citation_support_overstated_as_single_cause",
                "Use calibrated source-strength verbs such as supports, implicates, contributes to, or is consistent with unless direct causality is verified.",
                "Citation-derived claims must not turn support, association, or plausibility into sole-cause proof.",
                "example_essay_language_linter citation_strength_overclaim",
                "high",
                paragraph,
            )
        )
    if example_terms >= 3 and not INFERENCE.search(paragraph):
        deltas.append(
            make_delta(
                source_id,
                "examples_listed_without_wider_inference",
                "Convert examples into evidence for a broader mechanism or system claim.",
                "Examples should prove a wider argument rather than become disconnected mini-case detail.",
                "example_essay_language_linter example_overload_without_inference",
                "medium",
                paragraph,
            )
        )
    return deltas


def analyse_file(path: Path) -> dict[str, Any]:
    source_id = path.stem
    if path.suffix.lower() not in READABLE_EXTS:
        return {
            "source_id": source_id,
            "path": str(path),
            "status": "skipped",
            "qa_flags": [f"unsupported_extension:{path.suffix.lower() or '[none]'}"],
            "language_deltas": [],
            "example_contributions": [],
            "example_review_records": [],
        }
    try:
        text = read_text(path)
    except Exception as exc:
        return {
            "source_id": source_id,
            "path": str(path),
            "status": "unreadable",
            "qa_flags": [f"example_unreadable:{type(exc).__name__}"],
            "language_deltas": [],
            "example_contributions": [],
            "example_review_records": [],
        }
    if not text.strip():
        return {
            "source_id": source_id,
            "path": str(path),
            "status": "unreadable",
            "qa_flags": ["example_unreadable"],
            "language_deltas": [],
            "example_contributions": [],
            "example_review_records": [],
        }
    features = detect_source_features(path, text) if detect_source_features is not None else []
    detected_role = detect_role(path, text, source_features=features) if detect_role is not None else "external_example"
    deltas = []
    language_delta_scan = "skipped_source_role" if detected_role in LANGUAGE_DELTA_EXCLUDED_ROLES else "scanned"
    if language_delta_scan == "scanned":
        for paragraph in paragraphs(text):
            deltas.extend(analyse_paragraph(source_id, paragraph))
    contribution = {
        "source_id": source_id,
        "source_role": detected_role,
        "observed_source_pattern": "example material inspected for transferable language and workflow patterns",
        "structural_trigger": "matching future source evidence shows the same prose or workflow problem",
        "transferable_rule": "Convert example observations into generic language deltas and validation checks before updating production behaviour.",
        "non_transferable_content": ["all factual claims, citations, names, dates, topics, and recurrence details from the example"],
        "affected_workflows": ["example_essay_mode", "kp_synthesis", "qa", "cross_subject_regression"],
        "validation_checks": sorted({delta["validation_check"] for delta in deltas}) or ["manual_review_required"],
    }
    review_record = {
        "example_id": source_id,
        "source_role": "style_exemplar" if detected_role in {"exemplar_answer", "essay_guidance"} else "other_example",
        "example_scope": "external example inspected for transferable language and workflow behaviour",
        "what_worked": [
            "The example can expose reusable prose, structure, density, or QA behaviour without becoming target evidence."
        ],
        "why_it_worked": [
            "The reusable part is the condition detected by language deltas or workflow review, not the example's factual content."
        ],
        "what_failed": [delta["observed_problem"] for delta in deltas] or ["no failure observed"],
        "why_it_failed": [
            "Detected paragraph patterns matched a known student-output risk."
        ] if deltas else ["not applicable because no failure was observed"],
        "transferable_principle": (
            "Promote only generic condition-based language, structure, density, or QA rules after stripping example identity."
        ),
        "non_transferable_content": [
            "factual claims, citations, names, dates, topics, recurrence details, and exact headings from this example"
        ],
        "anti_overfit_rule": "Do not branch production behaviour on this example identity or copy its topic sequence.",
        "affected_protocols": ["references/example_analysis_protocol.md"],
        "affected_scripts": ["scripts/example_transfer_linter.py"],
        "validation_check": "scripts/example_transfer_linter.py must pass on the ExampleReviewLedger before rule promotion.",
        "regression_fixture": "tests/fixtures/example_learning",
        "promotion_status": "candidate",
        "confidence": "medium",
    }
    return {
        "source_id": source_id,
        "path": str(path),
        "status": "read",
        "qa_flags": [],
        "source_role": detected_role,
        "source_features": features,
        "language_delta_scan": language_delta_scan,
        "language_deltas": deltas,
        "example_contributions": [contribution],
        "example_review_records": [review_record],
        "paragraphs_read": len(paragraphs(text)),
        "word_count": len(WORD_RE.findall(text)),
    }


def iter_inputs(paths: list[Path], extensions: set[str] | None, max_files: int | None) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(item for item in path.rglob("*") if item.is_file())
        else:
            files.append(path)
    if extensions:
        files = [path for path in files if path.suffix.lower() in extensions]
    files = sorted(files, key=lambda item: str(item).lower())
    if max_files is not None and max_files > 0:
        files = files[:max_files]
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyse external examples into transferable language deltas.")
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--extensions", help="Comma-separated extension allow-list, e.g. .pdf,.pptx,.docx")
    parser.add_argument("--max-files", type=int, default=None, help="Optional cap for broad corpus scans.")
    args = parser.parse_args()

    extensions = {item.strip().lower() for item in args.extensions.split(",") if item.strip()} if args.extensions else None
    reports = [analyse_file(path) for path in iter_inputs(args.inputs, extensions=extensions, max_files=args.max_files)]
    result = {
        "status": "ok",
        "examples_read": sum(1 for report in reports if report["status"] == "read"),
        "examples_unreadable": sum(1 for report in reports if report["status"] != "read"),
        "source_role_counts": {
            role: sum(1 for report in reports if report.get("source_role") == role)
            for role in sorted({report.get("source_role") for report in reports if report.get("source_role")})
        },
        "language_deltas": [delta for report in reports for delta in report["language_deltas"]],
        "example_contributions": [item for report in reports for item in report["example_contributions"]],
        "example_review_ledger": {
            "object_type": "ExampleReviewLedger",
            "ledger_id": "ledger_external_example_corpus",
            "target_group_key": "external_example_learning",
            "records": [item for report in reports for item in report.get("example_review_records", [])],
            "non_transferable_content": sorted({
                item
                for report in reports
                for record in report.get("example_review_records", [])
                for item in record.get("non_transferable_content", [])
            }),
            "promotion_summary": {
                "accepted_count": 0,
                "candidate_count": sum(1 for report in reports for item in report.get("example_review_records", []) if item.get("promotion_status") == "candidate"),
                "rejected_count": 0,
                "blocked_count": 0,
            },
            "qa_status": "warning",
        },
        "non_transferable_content": sorted({item for report in reports for contribution in report["example_contributions"] for item in contribution["non_transferable_content"]}),
        "qa_flags": [flag for report in reports for flag in report["qa_flags"]],
        "sources": reports,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"status": "ok", "output": str(args.output), "language_deltas": len(result["language_deltas"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
