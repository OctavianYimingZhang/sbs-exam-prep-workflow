#!/usr/bin/env python3
"""Match uploaded Extra Reading Books to Example Essay questions and lecture terms."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    import fitz  # type: ignore
except Exception:  # pragma: no cover
    fitz = None


WORD = re.compile(r"[A-Za-z][A-Za-z0-9-]{2,}")
HEADING = re.compile(r"^(?:Chapter\s+\d+|CHAPTER\s+\d+|\d+(?:\.\d+)*\s+[A-Z][^\n]{3,}|[A-Z][A-Za-z0-9 ,:;()/-]{8,})$")


def extract_pdf_pages(path: Path) -> list[dict]:
    if fitz is None:
        return []
    doc = fitz.open(path)
    return [{"page": i + 1, "text": doc[i].get_text("text") or ""} for i in range(doc.page_count)]


def extract_text(path: Path) -> list[dict]:
    if path.suffix.lower() == ".pdf":
        return extract_pdf_pages(path)
    text = path.read_text(errors="ignore")
    return [{"page": 1, "text": text}]


def terms_from_inputs(question: str, keyword_files: list[Path]) -> set[str]:
    text = question + "\n" + "\n".join(path.read_text(errors="ignore") for path in keyword_files if path.exists())
    stop = {"the", "and", "for", "with", "that", "this", "from", "into", "essay", "explain", "discuss", "compare", "role"}
    return {word.lower() for word in WORD.findall(text) if word.lower() not in stop}


def find_headings(text: str) -> list[str]:
    headings = []
    for line in text.splitlines():
        line = line.strip()
        if 5 <= len(line) <= 120 and HEADING.match(line):
            headings.append(line)
    return headings[:20]


def rank_book(path: Path, terms: set[str]) -> dict:
    pages = extract_text(path)
    page_scores = []
    all_headings = []
    for page in pages:
        text = page["text"]
        tokens = {word.lower() for word in WORD.findall(text)}
        overlap = sorted(tokens & terms)
        score = len(overlap)
        if score:
            page_scores.append({"page": page["page"], "score": score, "matched_terms": overlap[:30], "preview": text[:500]})
        all_headings.extend(find_headings(text))
    page_scores.sort(key=lambda item: item["score"], reverse=True)
    return {
        "file": str(path),
        "candidate_headings": all_headings[:50],
        "top_pages": page_scores[:10],
        "chapter_found": bool(page_scores),
        "selected_anchor": f"page {page_scores[0]['page']}" if page_scores else None,
        "match_reason": "keyword_overlap" if page_scores else "no_relevant_overlap",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Match Extra Reading Books to essay questions and lecture keywords.")
    parser.add_argument("--question", required=True)
    parser.add_argument("--book", action="append", type=Path, default=[])
    parser.add_argument("--keyword-file", action="append", type=Path, default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    terms = terms_from_inputs(args.question, args.keyword_file)
    matches = [rank_book(path, terms) for path in args.book]
    result = {
        "question": args.question,
        "terms_used": sorted(terms),
        "matches": matches,
        "qa_flags": [] if any(match["chapter_found"] for match in matches) else ["extra_reading_chapter_not_found"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"status": "ok", "output": str(args.output), "matches": len(matches)}, indent=2))
    return 0 if any(match["chapter_found"] for match in matches) or not args.book else 1


if __name__ == "__main__":
    raise SystemExit(main())
