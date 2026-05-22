#!/usr/bin/env python3
"""Extract transferable language deltas from external example material."""

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


TEXT_EXTS = {".txt", ".md", ".markdown", ".json"}
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?")
PAGE_TRACE = re.compile(r"\b(Pages?|Slides?)\s+\d+\b", re.I)
META = re.compile(r"\b(this essay will|in this essay|in an essay answer|should be written as|use these pages|turn pages)\b", re.I)
CITATION_STACK = re.compile(r"(?:\([A-Z][A-Za-z'’-]+(?:\s+et\s+al\.)?(?:,\s*|\s+)(?:19|20)\d{2}[a-z]?\).*){3,}")
EXAMPLE_WITHOUT_INFERENCE = re.compile(r"\b(for example|case study|case|firm|company|example)\b", re.I)
INFERENCE = re.compile(r"\b(shows|demonstrates|supports|suggests|therefore|implies|illustrates|evidence)\b", re.I)


def read_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in TEXT_EXTS:
        return path.read_text(encoding="utf-8", errors="replace")
    if suffix == ".docx":
        if Document is None:
            raise RuntimeError("python-docx is required to read .docx examples")
        doc = Document(path)
        return "\n\n".join(paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip())
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
        }
    if not text.strip():
        return {
            "source_id": source_id,
            "path": str(path),
            "status": "unreadable",
            "qa_flags": ["example_unreadable"],
            "language_deltas": [],
            "example_contributions": [],
        }
    deltas = []
    for paragraph in paragraphs(text):
        deltas.extend(analyse_paragraph(source_id, paragraph))
    contribution = {
        "source_id": source_id,
        "source_role": "external_example",
        "observed_source_pattern": "example material inspected for transferable language and workflow patterns",
        "structural_trigger": "matching future source evidence shows the same prose or workflow problem",
        "transferable_rule": "Convert example observations into generic language deltas and validation checks before updating production behaviour.",
        "non_transferable_content": ["all factual claims, citations, names, dates, topics, and recurrence details from the example"],
        "affected_workflows": ["example_essay_mode", "kp_synthesis", "qa", "cross_subject_regression"],
        "validation_checks": sorted({delta["validation_check"] for delta in deltas}) or ["manual_review_required"],
    }
    return {
        "source_id": source_id,
        "path": str(path),
        "status": "read",
        "qa_flags": [],
        "language_deltas": deltas,
        "example_contributions": [contribution],
        "paragraphs_read": len(paragraphs(text)),
        "word_count": len(WORD_RE.findall(text)),
    }


def iter_inputs(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(item for item in path.rglob("*") if item.is_file())
        else:
            files.append(path)
    return sorted(files, key=lambda item: str(item).lower())


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyse external examples into transferable language deltas.")
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    reports = [analyse_file(path) for path in iter_inputs(args.inputs)]
    result = {
        "examples_read": sum(1 for report in reports if report["status"] == "read"),
        "examples_unreadable": sum(1 for report in reports if report["status"] != "read"),
        "language_deltas": [delta for report in reports for delta in report["language_deltas"]],
        "example_contributions": [item for report in reports for item in report["example_contributions"]],
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
