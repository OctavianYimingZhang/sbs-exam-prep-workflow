#!/usr/bin/env python3
"""Normalize target group keys and split papers into exam regimes.

This helper is intentionally conservative. It groups only by filename/course
signals and emits review flags instead of forcing uncertain files into a
prediction pool.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


NOISE = re.compile(
    r"\b(20\d{2}|19\d{2}|mock|practice|with answers?|answers? only|"
    r"answer key|guide answers?|solutions?|modified|syllabus|cadmus|pp[12]|"
    r"essay|problem|case studies|case study|numerical assessment|may \d+|"
    r"combined|copy|final|canvas|blackboard|minus seats|seat|pre-seat|"
    r"paper|exam|questions?)\b",
    re.IGNORECASE,
)
COURSE_CODE_RE = re.compile(r"\b([A-Z]{4}\d{5}[A-Z]?)\b", re.IGNORECASE)
COURSE_CODE_FULL_RE = re.compile(r"[A-Z]{4}\d{5}[A-Z]?", re.IGNORECASE)


def detect_course_code(*values: str | None) -> str | None:
    for value in values:
        if not value:
            continue
        match = COURSE_CODE_RE.search(value)
        if match:
            return match.group(1).upper()
    return None


def clean_target_label(value: str | None) -> str | None:
    if not value:
        return None
    label = COURSE_CODE_RE.sub(" ", value)
    label = label.replace("_", " ").replace("-", " ")
    label = re.sub(r"\s+", " ", label).strip()
    if not label or COURSE_CODE_FULL_RE.fullmatch(label):
        return None
    return label


def normalize_target_group_key(
    name: str,
    text: str = "",
    *,
    target_code: str | None = None,
    target_name: str | None = None,
    target_hint: str | None = None,
    target_label: str | None = None,
    required_target_code: str | None = None,
) -> str:
    record_code = detect_course_code(target_code, target_name)
    if record_code:
        return record_code
    record_name = clean_target_label(target_name)
    if record_name:
        return record_name
    detected_code = detect_course_code(f"{name}\n{text[:5000]}")
    if detected_code:
        return detected_code
    hint_code = detect_course_code(required_target_code, target_hint, target_label)
    if hint_code:
        return hint_code
    hint_name = clean_target_label(target_label) or clean_target_label(target_hint)
    if hint_name:
        return hint_name
    stem = Path(name).stem
    stem = stem.replace("&", " and ")
    stem = stem.replace("_", " ").replace("-", " ")
    stem = re.sub(r"\([^)]*\)", " ", stem)
    stem = NOISE.sub(" ", stem)
    stem = re.sub(r"\s+", " ", stem).strip()
    return stem or Path(name).stem


def group_metadata(target_group_key: str) -> dict:
    code_match = COURSE_CODE_FULL_RE.fullmatch(target_group_key)
    return {
        "target_code": target_group_key if code_match else None,
        "target_name": None if code_match else target_group_key,
        "confidence": "medium" if target_group_key else "low",
        "grouping_evidence": ["course code, user-provided hint, title text, or filename normalization"],
        "possible_conflicts": [],
    }


def detect_year(name: str) -> int | None:
    match = re.search(r"(?<!\d)(20\d{2}|19\d{2})(?!\d)", name)
    return int(match.group(1)) if match else None


def infer_regime(text: str, name: str = "") -> str:
    lower = f"{name}\n{text}".lower()
    if "problem paper" in lower or "case stud" in lower or "numerical assessment" in lower:
        return "problem_or_data"
    if "essay paper" in lower:
        return "essay"
    if "example paper" in lower or "mock paper" in lower:
        return "example_or_mock"
    if "section a" in lower and "section b" in lower:
        if "answer one" in lower and ("project" in lower or "scenario" in lower):
            return "section-a-plus-section-b mixed_project_or_long_answer"
        if any(term in lower for term in ("problem", "data", "graph", "figure")):
            return "section-a-plus-section-b problem_or_data"
        if "answer all" in lower and ("answer one" in lower or "answer 1" in lower):
            return "section-a-answer-all plus section-b-answer-one"
        return "section-a-plus-section-b"
    if "answer one" in lower and ("project" in lower or "scenario" in lower):
        return "answer-one long-answer_project"
    if "answer one" in lower or "answer 1" in lower:
        if "essay" in lower:
            return "answer-one essay"
        return "answer-one mixed"
    if "answer all" in lower:
        if "multiple choice" in lower or "mcq" in lower:
            return "answer-all mcq_or_mixed"
        return "answer-all short-answer_or_problem"
    if "case stud" in lower:
        return "case-study"
    if "multiple choice" in lower or "mcq" in lower:
        return "mcq"
    return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_scan", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    scan = json.loads(args.source_scan.read_text())
    groups: dict[str, dict] = {}
    flags = []
    for record in scan.get("files", []):
        text = ""
        text_path = record.get("text_path")
        if text_path and Path(text_path).exists():
            text = Path(text_path).read_text(errors="ignore")[:20000]
        target_group_key = normalize_target_group_key(
            record.get("name", ""),
            text,
            target_code=record.get("target_code"),
            target_name=record.get("target_name"),
            target_hint=scan.get("target_hint"),
            target_label=scan.get("target_label"),
            required_target_code=scan.get("target_code"),
        )
        year = record.get("year") or detect_year(record.get("name", ""))
        regime = infer_regime(text, record.get("name", ""))
        item = {
            "file": record.get("path"),
            "name": record.get("name"),
            "role": record.get("role"),
            "year": year,
            "exam_regime": regime,
        }
        group = groups.setdefault(
            target_group_key,
            {
                "target_group_key": target_group_key,
                **group_metadata(target_group_key),
                "files": [],
                "regimes": {},
            },
        )
        group["files"].append(item)
        group["regimes"].setdefault(regime, []).append(item["name"])
        if regime == "unknown" and record.get("role") == "formal_past_paper":
            flags.append({"file": item["name"], "flag": "unknown_exam_regime"})

    args.output.write_text(json.dumps({"groups": list(groups.values()), "qa_flags": flags}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
