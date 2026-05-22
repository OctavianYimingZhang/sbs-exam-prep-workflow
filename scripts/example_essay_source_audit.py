#!/usr/bin/env python3
"""Build source audit JSON for Example Essay DOCX outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def audit_from_source_map(path: Path) -> dict[str, Any]:
    data = load_json(path)
    lecture_sources: dict[tuple[str, str], set[str]] = {}
    citation_sources = []
    extra_sources = []
    lecture_logic_summary = []
    yellow_words = 0
    green_words = 0
    total_words = 0

    for paragraph in data.get("paragraphs", []):
        pid = paragraph.get("paragraph_id")
        if paragraph.get("function"):
            lecture_logic_summary.append({"paragraph": pid, "function": paragraph.get("function")})
        for anchor in paragraph.get("lecture_anchors", []):
            key = (anchor.get("file", ""), anchor.get("slide_or_page_range", ""))
            lecture_sources.setdefault(key, set()).add(pid)
        for run in paragraph.get("runs", []):
            total_words += int(run.get("word_count") or 0)
            if run.get("source_type") in {"citation_original_source", "classic_experiment_source"}:
                green_words += int(run.get("word_count") or 0)
                citation_sources.append(
                    {
                        "source_type": run.get("source_type"),
                        "raw_citation": run.get("in_text_citation"),
                        "slide_anchor": run.get("source_anchor"),
                        "resolved_to": run.get("source_anchor"),
                        "read_status": "read" if run.get("citation_original_read") else "not_read",
                        "used_in_essay": True,
                        "green_highlight_word_count": run.get("word_count", 0),
                    }
                )
            if run.get("source_type") == "extra_reading_book":
                yellow_words += int(run.get("word_count") or 0)
                extra_sources.append(
                    {
                        "file": run.get("source_anchor"),
                        "chapter": run.get("source_anchor"),
                        "section": run.get("source_anchor"),
                        "match_reason": "run_source_anchor",
                        "used_in_essay": True,
                        "yellow_highlight_word_count": run.get("word_count", 0),
                    }
                )

    lecture_slide_sources = [
        {
            "file": file,
            "slide_range": slide_range,
            "used_paragraphs": sorted(paragraphs),
        }
        for (file, slide_range), paragraphs in sorted(lecture_sources.items())
    ]
    total_body_words = data.get("word_counts", {}).get("total_body_words", total_words)
    audit_yellow_words = data.get("word_counts", {}).get("extra_reading_yellow_words", yellow_words)
    audit_green_words = data.get("word_counts", {}).get("citation_original_green_words", green_words)
    return {
        "essay_id": data.get("essay_id"),
        "question": data.get("question"),
        "docx_filename": data.get("docx_filename"),
        "lecture_slide_sources": lecture_slide_sources,
        "lecture_logic_summary": lecture_logic_summary,
        "citation_sources_detected": citation_sources,
        "extra_reading_books": extra_sources,
        "word_counts": {
            "total_body_words": total_body_words,
            "lecture_core_words": max(total_body_words - audit_yellow_words - audit_green_words, 0),
            "citation_original_green_words": audit_green_words,
            "extra_reading_yellow_words": audit_yellow_words,
            "extra_reading_ratio": data.get("word_counts", {}).get("extra_reading_ratio", (audit_yellow_words / total_body_words) if total_body_words else 0),
        },
        "qa_flags": data.get("qa_flags", []),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create Example Essay source audit JSON from source maps.")
    parser.add_argument("--source-map", action="append", type=Path, default=[])
    parser.add_argument("--dir", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    maps = list(args.source_map)
    if args.dir:
        maps.extend(sorted(args.dir.glob("EE*_source_map.json")))
    audits = [audit_from_source_map(path) for path in maps]
    result = {"essays": audits}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"status": "ok", "output": str(args.output), "essays": len(audits)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
