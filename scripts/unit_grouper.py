#!/usr/bin/env python3
"""Normalize unit keys and split papers into exam regimes.

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
    r"\b(20\d{2}|19\d{2}|mock|practice|with answers?|answer key|may \d+|"
    r"combined|copy|final|canvas|blackboard|minus seats|seat|pre-seat|"
    r"paper|exam|questions?)\b",
    re.IGNORECASE,
)

# These aliases support regression examples and filename normalization only.
# They must not limit the Skill to these Units or control question-type routing,
# prediction, or output-mode decisions.
UNIT_ALIASES = [
    ("Motor Systems", ["biol21332", "biol22332", "motor system", "motor systems"]),
    ("Genome Maintenance and Regulation", ["biol21101", "genome maintenance", "genome maintenance and regulation"]),
    ("Proteins", ["biol21111", "proteins"]),
    ("Principles of Developmental Biology", ["biol21172", "biol21172t", "principles of developmental biology"]),
    ("Plants for the Future", ["biol21202", "biol21202t", "plants for the future"]),
    ("Immunology", ["biol21242", "biol21242t", "immunology"]),
]


def normalize_unit_key(name: str, text: str = "") -> str:
    haystack = f"{name}\n{text[:5000]}".lower()
    for canonical, aliases in UNIT_ALIASES:
        if any(alias in haystack for alias in aliases):
            return canonical
    code_match = re.search(r"\b([A-Z]{4}\d{5}[A-Z]?)\b", f"{name}\n{text[:5000]}", flags=re.IGNORECASE)
    if code_match:
        return code_match.group(1).upper()
    stem = Path(name).stem
    stem = stem.replace("_", " ").replace("-", " ")
    stem = re.sub(r"\([^)]*\)", " ", stem)
    stem = NOISE.sub(" ", stem)
    stem = re.sub(r"\s+", " ", stem).strip()
    return stem or Path(name).stem


def unit_metadata(unit_key: str) -> dict:
    code_match = re.fullmatch(r"[A-Z]{4}\d{5}[A-Z]?", unit_key)
    return {
        "unit_code": unit_key if code_match else None,
        "unit_name": None if code_match else unit_key,
        "confidence": "medium" if unit_key else "low",
        "grouping_evidence": ["unit code, known alias, title text, or filename normalization"],
        "possible_conflicts": [],
    }


def detect_year(name: str) -> int | None:
    match = re.search(r"\b(20\d{2}|19\d{2})\b", name)
    return int(match.group(1)) if match else None


def infer_regime(text: str) -> str:
    lower = text.lower()
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
        unit_key = normalize_unit_key(record.get("name", ""), text)
        year = record.get("year") or detect_year(record.get("name", ""))
        regime = infer_regime(text)
        item = {
            "file": record.get("path"),
            "name": record.get("name"),
            "role": record.get("role"),
            "year": year,
            "exam_regime": regime,
        }
        group = groups.setdefault(
            unit_key,
            {
                "unit_key": unit_key,
                **unit_metadata(unit_key),
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
