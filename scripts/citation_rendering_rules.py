"""Shared public citation rendering rules for essay-style outputs."""

from __future__ import annotations

import re
from typing import Any


AUTHOR_YEAR_PARENTHETICAL_RE = re.compile(
    r"\([A-Z][A-Za-z'’-]+(?:\s+et\s+al\.|\s+and\s+[A-Z][A-Za-z'’-]+)?(?:,\s*|\s+)(?:19|20)\d{2}[a-z]?\)"
)

AUTHOR_VERB_PATTERN = (
    r"(?:argu(?:ed|es)|associate(?:d|s)|claim(?:ed|s)|demonstrat(?:ed|es)|describ(?:ed|es)|"
    r"discover(?:ed|s)|establish(?:ed|es)|find(?:s)?|found|identif(?:ied|ies)|implicat(?:ed|es)|"
    r"link(?:ed|s)?|propos(?:ed|es)|report(?:ed|s)|show(?:ed|s)?|suggest(?:ed|s)?)"
)

EXPLICIT_AUTHOR_LED_CITATION_RE = re.compile(
    r"\b[A-Z][A-Za-z'’-]+"
    r"(?:\s+et\s+al\.|\s+and\s+[A-Z][A-Za-z'’-]+|\s+\((?:19|20)\d{2}[a-z]?\))"
    r"\s+"
    + AUTHOR_VERB_PATTERN
    + r"\b"
)

SINGLE_AUTHOR_LED_WITH_CITATION_RE = re.compile(
    r"\b(?P<subject>[A-Z][A-Za-z'’-]+)\s+"
    + AUTHOR_VERB_PATTERN
    + r"\b(?=[^.!?]{0,180}\([A-Z][A-Za-z'’-]+(?:,\s*|\s+)(?:19|20)\d{2}[a-z]?\))"
)

NON_AUTHOR_SUBJECTS = {
    "A",
    "An",
    "Evidence",
    "Experiment",
    "It",
    "Review",
    "Study",
    "That",
    "The",
    "These",
    "They",
    "This",
    "Those",
}


def normalized_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("–", "-").replace("—", "-")).strip()


def author_led_citation_hits(text: str) -> list[str]:
    normalized = normalized_text(text)
    hits = [match.group(0) for match in EXPLICIT_AUTHOR_LED_CITATION_RE.finditer(normalized)]
    for match in SINGLE_AUTHOR_LED_WITH_CITATION_RE.finditer(normalized):
        if match.group("subject") not in NON_AUTHOR_SUBJECTS:
            hits.append(match.group(0))
    return sorted(set(hits))


def parenthetical_author_year_hits(text: str) -> list[str]:
    return [match.group(0) for match in AUTHOR_YEAR_PARENTHETICAL_RE.finditer(str(text or ""))]


def is_parenthetical_author_year(value: Any) -> bool:
    text = str(value or "").strip()
    return bool(AUTHOR_YEAR_PARENTHETICAL_RE.fullmatch(text))
