"""Shared knowledge-only public rendering rules for ordinary notes routes."""

from __future__ import annotations

import re
from typing import Any


FORBIDDEN_ADVISORY_PHRASES = [
    "a strong answer should",
    "answer logic",
    "exam strategy",
    "generic exam advice",
    "how to answer",
    "integrated practical reasoning",
    "integrated reasoning",
    "not driven by question type",
    "not reliable by question type",
    "question-type dependent",
    "recommended approach",
    "recommended output route",
    "use this module",
]

FORBIDDEN_ADVISORY_HEADINGS = [
    "Answer Logic",
    "Exam Strategy",
    "How To Answer This Exam",
    "How To Use This Document",
    "Integrated Practical Reasoning",
    "Integrated Reasoning",
    "Must Master",
    "Recommended Approach",
]


def normalized_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").casefold().replace("–", "-").replace("—", "-")).strip()


def forbidden_advisory_phrase_hits(text: str) -> list[str]:
    normalized = normalized_text(text)
    return [phrase for phrase in FORBIDDEN_ADVISORY_PHRASES if normalized_text(phrase) in normalized]


def forbidden_advisory_heading_hits(text: str) -> list[str]:
    hits: list[str] = []
    for heading in FORBIDDEN_ADVISORY_HEADINGS:
        if re.search(rf"(?im)^\s*(?:#+\s*)?{re.escape(heading)}\s*:?\s*$", text):
            hits.append(heading)
    return hits

