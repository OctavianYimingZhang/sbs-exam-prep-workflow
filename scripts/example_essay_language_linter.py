#!/usr/bin/env python3
"""Lint complete Example Essay prose against the shared language contract."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    from docx import Document  # type: ignore
except Exception:  # pragma: no cover
    Document = None


WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?")
SENTENCE_RE = re.compile(r"[^.!?]+[.!?]?")
AUTHOR_YEAR_RE = re.compile(r"\([A-Z][A-Za-z'’-]+(?:\s+et\s+al\.|\s+and\s+[A-Z][A-Za-z'’-]+)?(?:,\s*|\s+)(?:19|20)\d{2}[a-z]?\)")

CLAIM_CONNECTORS = re.compile(
    r"\b(because|therefore|consequently|as a result|depends on|regulates|drives|converts|constrains|enables|explains|links|integrates|supports|limits|whereas|although|while|thereby|so)\b",
    re.I,
)

META_OPENERS = re.compile(
    r"^\s*(this essay will|in this essay|this paragraph will|the following (essay|section|paragraph)|i will|we will)\b",
    re.I,
)

SOURCE_TRACE = [
    ("page_trace", re.compile(r"\bPages?\s+\d+\b", re.I)),
    ("slide_trace", re.compile(r"\bSlides?\s+\d+\b", re.I)),
    ("lecture_sequence_narration", re.compile(r"\blecture sequence\b", re.I)),
    ("source_walkthrough", re.compile(r"\b(first establishes|then develops|then closes|later pages add|slide sequence)\b", re.I)),
    (
        "lecture_route_narration",
        re.compile(
            r"\b(?:the\s+)?(?:lecture|lectures|slides|source|chapter|section|module)\s+(?:\d+\s+)?"
            r"(?:establishes|establish|adds|add|introduces|introduce|covers|cover|moves from|move from|develops|develop|closes with|close with)\b",
            re.I,
        ),
    ),
]

HOW_TO_WRITE = [
    ("how_to_write", re.compile(r"\b(should be written as|write this as|use these pages|turn pages|in an essay answer)\b", re.I)),
    (
        "exam_guidance_sentence",
        re.compile(
            r"\b(final\s+exam\s+thesis\s+should\s+be|exam\s+thesis\s+should\s+be|"
            r"in\s+an\s+exam\s+answer|for\s+the\s+exam|the\s+answer\s+should\s+be|"
            r"the\s+correct\s+conclusion\s+is|should\s+frame\s+this\s+as)\b",
            re.I,
        ),
    ),
    (
        "mechanical_compression_trace",
        re.compile(
            r"\b(?:compressed|compress(?:ion|ing)?|reduce(?:d)?|cut)\s+(?:by|about|around|approximately)?\s*\d{1,3}%\b|"
            r"\b(?:target|safe|lossless)\s+word[-\s]?count\b|"
            r"\b(?:safe|lossless)\s+compression\s+(?:range|budget|limit)\b",
            re.I,
        ),
    ),
]

WEAK_OPENERS = re.compile(r"^\s*(background|introduction|firstly|secondly|thirdly|to begin with)\b[:,]?", re.I)
EXAMPLE_TERMS = re.compile(r"\b(for example|case study|case|firm|company|example)\b", re.I)
EXAMPLE_TO_ARGUMENT = re.compile(r"\b(shows|demonstrates|supports|indicates|suggests|therefore|consequently|implies|evidence|illustrates)\b", re.I)
NEGATIVE_FRAMING = re.compile(r"\b(not\s+(?:a|an|the|only|merely|simply)|rather than)\b", re.I)
BROAD_IMPORTANCE = re.compile(r"\b(this matters|this is important|this is critical|the important point)\b", re.I)
IMPORTANCE_WITH_CONSEQUENCE = re.compile(r"\b(because|therefore|consequently|as a result|so|means that|explains|limits|enables|constrains)\b", re.I)
SUPPORT_TO_CAUSE_OVERCLAIM = re.compile(
    r"\b(?:supports?|implicates?|suggests?|is consistent with|is associated with)\b[^.!?]{0,140}\b(?:the|a|single|sole)\s+cause\b",
    re.I,
)
CHANNEL_CATALOGUE_TERMS = re.compile(
    r"\b(?:persistent\s+Na\+?|persistent\s+sodium|low-threshold\s+Ca(?:2\+|\²\+)?|low-threshold\s+calcium|"
    r"NMDA(?:-dependent)?|HCN|Ca(?:2\+|\²\+)?-dependent\s+K\+?|calcium-dependent\s+potassium|"
    r"sodium\s+current|calcium\s+current|potassium\s+current|ionic\s+conductance|conductances?)\b",
    re.I,
)
SCOPE_COLLAPSE = re.compile(
    r"\b(?:sensory\s+(?:feedback|input|reafference)\s+(?:is\s+)?(?:unnecessary|dispensable|not\s+necessary)\s+for\s+locomotion|"
    r"feedback\s+(?:is\s+)?(?:unnecessary|dispensable)\s+for\s+movement)\b",
    re.I,
)
DESCRIPTIVE_START = re.compile(
    r"^\s*[A-Z][A-Za-z0-9βγα/+\-\s]{1,45}\s+"
    r"(?:is|are|mediates?|regulates?|controls?|provides?|encodes?|expresses?|contains?|projects?|activates?|inhibits?)\b",
    re.I,
)
ANALYTIC_SENTENCE_MARKERS = re.compile(
    r"\b(because|therefore|so|whereas|although|while|thereby|this\s+(?:means|shows|demonstrates|limits|explains)|"
    r"solves?|distinguish(?:es)?|rather than|in contrast|as a result|consequently|link(?:s|ed)?\s+to)\b",
    re.I,
)


@dataclass
class ParagraphRecord:
    source: str
    essay_id: str | None
    paragraph_id: str | None
    index: int
    function: str | None
    text: str
    has_lecture_anchor: bool | None = None
    is_conclusion: bool = False


def words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def first_sentence(text: str) -> str:
    for match in SENTENCE_RE.finditer(text.strip()):
        sentence = match.group(0).strip()
        if sentence:
            return sentence
    return text.strip()


def sentences(text: str) -> list[str]:
    return [match.group(0).strip() for match in SENTENCE_RE.finditer(text.strip()) if match.group(0).strip()]


def has_three_descriptive_sentences_without_analysis(items: list[str]) -> bool:
    streak = 0
    for sentence in items:
        if DESCRIPTIVE_START.search(sentence) and not ANALYTIC_SENTENCE_MARKERS.search(sentence):
            streak += 1
            if streak >= 3:
                return True
        else:
            streak = 0
    return False


def paragraph_text(paragraph: dict[str, Any]) -> str:
    if "text" in paragraph:
        return str(paragraph.get("text") or "")
    return "".join(str(run.get("text", "")) for run in paragraph.get("text_runs", []))


def is_body_paragraph(paragraph: dict[str, Any]) -> bool:
    return not (paragraph.get("is_title") or paragraph.get("is_subtitle") or paragraph.get("is_heading"))


def load_plan_records(path: Path) -> list[ParagraphRecord]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        essays = data
    elif isinstance(data.get("essays"), list):
        essays = data["essays"]
    else:
        essays = [data]

    records: list[ParagraphRecord] = []
    for essay in essays:
        body = [p for p in essay.get("paragraphs", []) if is_body_paragraph(p)]
        for idx, paragraph in enumerate(body, start=1):
            text = paragraph_text(paragraph)
            function = paragraph.get("function")
            records.append(
                ParagraphRecord(
                    source=str(path),
                    essay_id=essay.get("essay_id"),
                    paragraph_id=paragraph.get("paragraph_id"),
                    index=idx,
                    function=function,
                    text=text,
                    has_lecture_anchor=bool(paragraph.get("lecture_anchors")),
                    is_conclusion=bool(function and "conclusion" in str(function).lower()),
                )
            )
    return records


def load_text_records(path: Path) -> list[ParagraphRecord]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    parts = [part.strip() for part in re.split(r"\n\s*\n", raw) if part.strip()]
    return [
        ParagraphRecord(source=str(path), essay_id=None, paragraph_id=None, index=idx, function=None, text=part, is_conclusion=bool(re.match(r"^\s*conclusion\b", part, re.I)))
        for idx, part in enumerate(parts, start=1)
    ]


def source_map_for_docx(path: Path) -> dict[str, Any] | None:
    candidates = [
        path.with_name(path.stem.split("_")[0] + "_source_map.json"),
        path.with_name(path.stem + "_source_map.json"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return json.loads(candidate.read_text(encoding="utf-8"))
    return None


def load_docx_records(path: Path) -> list[ParagraphRecord]:
    if Document is None:
        raise RuntimeError("python-docx is required to lint .docx files")
    doc = Document(path)
    parts = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    source_map = source_map_for_docx(path)
    if source_map and len(source_map.get("paragraphs", [])) == len(parts):
        records = []
        body_index = 0
        for visible_index, (text, paragraph) in enumerate(zip(parts, source_map.get("paragraphs", [])), start=1):
            if paragraph.get("kind") != "body":
                continue
            body_index += 1
            function = paragraph.get("function")
            records.append(
                ParagraphRecord(
                    source=str(path),
                    essay_id=source_map.get("essay_id"),
                    paragraph_id=paragraph.get("paragraph_id"),
                    index=body_index,
                    function=function,
                    text=text,
                    has_lecture_anchor=bool(paragraph.get("lecture_anchors")),
                    is_conclusion=bool(function and "conclusion" in str(function).lower()),
                )
            )
        return records

    body = []
    for idx, paragraph in enumerate(parts, start=1):
        if idx == 1:
            continue
        if idx == 2 and re.match(r"^\s*(explain|discuss|compare|evaluate|describe|how|why|what)\b", paragraph, re.I):
            continue
        if re.match(r"^\d+(?:\.\d+)*\s+\S+", paragraph):
            continue
        body.append(paragraph)
    return [
        ParagraphRecord(source=str(path), essay_id=None, paragraph_id=None, index=idx, function=None, text=part, is_conclusion=bool(re.match(r"^\s*conclusion\b", part, re.I)))
        for idx, part in enumerate(body, start=1)
    ]


def load_fixture_records(path: Path) -> tuple[list[ParagraphRecord], dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    records: list[ParagraphRecord] = []
    expectations: dict[str, str] = {}
    for idx, case in enumerate(data.get("cases", []), start=1):
        case_id = case.get("id", f"case_{idx}")
        text = case.get("text", "")
        function = case.get("function")
        expectations[case_id] = str(case.get("expected", "")).lower()
        records.append(
            ParagraphRecord(
                source=str(path),
                essay_id=case_id,
                paragraph_id=case_id,
                index=idx,
                function=function,
                text=text,
                has_lecture_anchor=case.get("has_lecture_anchor"),
                is_conclusion=bool(function and "conclusion" in str(function).lower()),
            )
        )
    return records, expectations


def hit_patterns(text: str, patterns: Iterable[tuple[str, re.Pattern[str]]]) -> list[dict[str, str]]:
    hits = []
    for name, pattern in patterns:
        match = pattern.search(text)
        if match:
            hits.append({"type": name, "phrase": match.group(0)})
    return hits


def lint_paragraph(record: ParagraphRecord, min_words: int, max_words: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    failures: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    text = record.text.strip()
    count = len(words(text))
    first = first_sentence(text)

    for hit in hit_patterns(text, SOURCE_TRACE + HOW_TO_WRITE):
        failures.append({"type": hit["type"], "phrase": hit["phrase"]})
    if META_OPENERS.search(first):
        failures.append({"type": "generic_metacommentary_opener", "phrase": first[:120]})
    if record.has_lecture_anchor is False:
        failures.append({"type": "body_paragraph_missing_lecture_anchor"})
    if count < min_words:
        warnings.append({"type": "short_paragraph", "word_count": count})
    if count > max_words:
        warnings.append({"type": "overlong_paragraph", "word_count": count})
    if WEAK_OPENERS.search(first):
        warnings.append({"type": "weak_topic_label_opener", "phrase": first[:120]})
    if not CLAIM_CONNECTORS.search(text) and count >= min_words:
        warnings.append({"type": "no_visible_mechanism_or_inference_connector"})

    for sentence in sentences(text):
        if len(AUTHOR_YEAR_RE.findall(sentence)) >= 3:
            failures.append({"type": "citation_stack", "phrase": sentence[:180]})

    example_count = len(EXAMPLE_TERMS.findall(text))
    if example_count >= 3 and not EXAMPLE_TO_ARGUMENT.search(text):
        failures.append({"type": "example_overload_without_inference", "example_terms": example_count})
    if SUPPORT_TO_CAUSE_OVERCLAIM.search(text):
        failures.append({"type": "citation_strength_overclaim", "phrase": SUPPORT_TO_CAUSE_OVERCLAIM.search(text).group(0)[:180]})
    channel_terms = {match.group(0).lower() for match in CHANNEL_CATALOGUE_TERMS.finditer(text)}
    if len(channel_terms) >= 4:
        failures.append({"type": "unnecessary_channel_catalogue", "terms": sorted(channel_terms)[:8]})
    if SCOPE_COLLAPSE.search(text):
        failures.append({"type": "compression_changed_claim_scope", "phrase": SCOPE_COLLAPSE.search(text).group(0)})
    sentence_items = sentences(text)
    if has_three_descriptive_sentences_without_analysis(sentence_items):
        failures.append({"type": "descriptive_list_without_analysis"})
    if len(NEGATIVE_FRAMING.findall(text)) >= 4:
        warnings.append({"type": "repeated_negative_framing"})
    if BROAD_IMPORTANCE.search(text) and not IMPORTANCE_WITH_CONSEQUENCE.search(text):
        warnings.append({"type": "broad_importance_without_specific_consequence"})

    if record.is_conclusion:
        if AUTHOR_YEAR_RE.search(text):
            failures.append({"type": "conclusion_adds_citation_or_new_evidence"})
        if re.search(r"\b(for example|new evidence|another example)\b", text, re.I):
            failures.append({"type": "conclusion_adds_new_example"})

    return failures, warnings


def record_payload(record: ParagraphRecord, issues: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "source": record.source,
        "essay_id": record.essay_id,
        "paragraph_id": record.paragraph_id,
        "paragraph_index": record.index,
        "function": record.function,
        "issues": issues,
        "preview": record.text[:240].replace("\n", " "),
    }


def lint_records(records: list[ParagraphRecord], min_words: int = 35, max_words: int = 280) -> dict[str, Any]:
    failures = []
    warnings = []
    for record in records:
        record_failures, record_warnings = lint_paragraph(record, min_words=min_words, max_words=max_words)
        if record_failures:
            failures.append(record_payload(record, record_failures))
        if record_warnings:
            warnings.append(record_payload(record, record_warnings))
    return {
        "pass": not failures,
        "fail_reasons": sorted({issue["type"] for row in failures for issue in row["issues"]}),
        "counts": {
            "paragraphs": len(records),
            "failing_paragraphs": len(failures),
            "warning_paragraphs": len(warnings),
        },
        "failures": failures,
        "warnings": warnings[:100],
    }


def fixture_report(path: Path, min_words: int, max_words: int) -> dict[str, Any]:
    records, expectations = load_fixture_records(path)
    cases = []
    for record in records:
        result = lint_records([record], min_words=min_words, max_words=max_words)
        expected = expectations.get(record.paragraph_id or "", "")
        expected_pass = expected == "pass" if expected in {"pass", "fail"} else None
        matched = expected_pass is None or result["pass"] == expected_pass
        cases.append(
            {
                "case_id": record.paragraph_id,
                "expected": expected,
                "actual_pass": result["pass"],
                "matched": matched,
                "fail_reasons": result["fail_reasons"],
            }
        )
    return {
        "pass": all(case["matched"] for case in cases),
        "cases": cases,
        "counts": {
            "cases": len(cases),
            "matched": sum(1 for case in cases if case["matched"]),
            "mismatched": sum(1 for case in cases if not case["matched"]),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint complete Example Essay language quality.")
    parser.add_argument("--plan", action="append", type=Path, default=[])
    parser.add_argument("--text", action="append", type=Path, default=[])
    parser.add_argument("--docx", action="append", type=Path, default=[])
    parser.add_argument("--fixture", action="append", type=Path, default=[])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--min-words", type=int, default=35)
    parser.add_argument("--max-words", type=int, default=280)
    args = parser.parse_args()

    reports = []
    overall_pass = True

    for path in args.plan:
        try:
            report = lint_records(load_plan_records(path), args.min_words, args.max_words)
        except Exception as exc:
            report = {"pass": False, "fail_reasons": ["read_error"], "error": str(exc)}
        report.update({"type": "plan", "path": str(path)})
        reports.append(report)
        overall_pass = overall_pass and bool(report["pass"])

    for path in args.text:
        try:
            report = lint_records(load_text_records(path), args.min_words, args.max_words)
        except Exception as exc:
            report = {"pass": False, "fail_reasons": ["read_error"], "error": str(exc)}
        report.update({"type": "text", "path": str(path)})
        reports.append(report)
        overall_pass = overall_pass and bool(report["pass"])

    for path in args.docx:
        try:
            report = lint_records(load_docx_records(path), args.min_words, args.max_words)
        except Exception as exc:
            report = {"pass": False, "fail_reasons": ["read_error"], "error": str(exc)}
        report.update({"type": "docx", "path": str(path)})
        reports.append(report)
        overall_pass = overall_pass and bool(report["pass"])

    for path in args.fixture:
        try:
            report = fixture_report(path, args.min_words, args.max_words)
        except Exception as exc:
            report = {"pass": False, "fail_reasons": ["read_error"], "error": str(exc)}
        report.update({"type": "fixture", "path": str(path)})
        reports.append(report)
        overall_pass = overall_pass and bool(report["pass"])

    if not reports:
        reports.append({"type": "none", "pass": False, "fail_reasons": ["no_inputs"]})
        overall_pass = False

    result = {"pass": overall_pass, "reports": reports}
    text = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
