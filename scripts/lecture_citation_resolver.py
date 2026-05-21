#!/usr/bin/env python3
"""Detect lecture-slide citations and conservatively resolve uploaded originals."""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    import fitz  # type: ignore
except Exception:  # pragma: no cover
    fitz = None


AUTHOR_YEAR = re.compile(r"\b([A-Z][A-Za-z'’-]+(?:\s+et\s+al\.|\s+and\s+[A-Z][A-Za-z'’-]+)?)[,\s]+((?:19|20)\d{2}[a-z]?)\b")
DOI = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]+\b")
PMID = re.compile(r"\bPMID[:\s]*(\d{6,9})\b", re.I)


def extract_text(path: Path, max_chars: int = 50000) -> str:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md", ".json"}:
        return path.read_text(errors="ignore")[:max_chars]
    if suffix == ".pdf" and fitz is not None:
        doc = fitz.open(path)
        return "\n".join(page.get_text("text") for page in doc)[:max_chars]
    if suffix == ".pptx":
        texts: list[str] = []
        with zipfile.ZipFile(path) as zf:
            names = sorted(
                [name for name in zf.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", name)],
                key=lambda item: int(re.search(r"slide(\d+)\.xml", item).group(1)),
            )
            for name in names:
                root = ET.fromstring(zf.read(name))
                slide_no = re.search(r"slide(\d+)\.xml", name).group(1)
                for node in root.iter():
                    if node.tag.endswith("}t") and node.text:
                        texts.append(f"[slide {slide_no}] {node.text}")
        return "\n".join(texts)[:max_chars]
    return ""


def detect_citations(text: str) -> list[dict]:
    candidates = []
    seen = set()
    for match in AUTHOR_YEAR.finditer(text):
        raw = match.group(0)
        key = ("author_year", raw)
        if key not in seen:
            seen.add(key)
            candidates.append({"type": "author_year", "raw_citation": raw, "author": match.group(1), "year": match.group(2)})
    for pattern_type, pattern in [("doi", DOI), ("pmid", PMID)]:
        for match in pattern.finditer(text):
            raw = match.group(0)
            key = (pattern_type, raw)
            if key not in seen:
                seen.add(key)
                candidates.append({"type": pattern_type, "raw_citation": raw})
    return candidates


def resolve_against_uploads(candidate: dict, uploads: list[Path]) -> dict:
    raw = candidate.get("raw_citation", "")
    author = str(candidate.get("author", "")).lower()
    year = str(candidate.get("year", ""))
    for path in uploads:
        haystack = f"{path.name}\n{extract_text(path, max_chars=20000)}".lower()
        if raw.lower() in haystack or (author and year and author in haystack and year in haystack):
            return {
                "raw_citation": raw,
                "resolved_to": str(path),
                "read_status": "read",
                "resolution_method": "uploaded_file_text_match",
                "notes": extract_text(path, max_chars=3000),
            }
    return {
        "raw_citation": raw,
        "resolved_to": None,
        "read_status": "unresolved",
        "resolution_method": "not_found_in_uploaded_files",
        "notes": "",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect citations from lecture slide text and resolve uploaded originals.")
    parser.add_argument("--input", action="append", type=Path, default=[], help="Lecture slide/text/PDF/PPTX input.")
    parser.add_argument("--uploaded-source", action="append", type=Path, default=[], help="Candidate original source file already supplied by the user.")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    combined_text = "\n".join(extract_text(path) for path in args.input)
    candidates = detect_citations(combined_text)
    resolutions = [resolve_against_uploads(candidate, args.uploaded_source) for candidate in candidates]

    candidates_path = args.output_dir / "citation_candidates.json"
    log_path = args.output_dir / "citation_resolution_log.json"
    notes_path = args.output_dir / "citation_source_notes.json"
    candidates_path.write_text(json.dumps({"candidates": candidates}, indent=2), encoding="utf-8")
    log_path.write_text(json.dumps({"resolutions": resolutions}, indent=2), encoding="utf-8")
    notes_path.write_text(
        json.dumps(
            {
                "notes": [
                    {
                        "raw_citation": item["raw_citation"],
                        "source": item["resolved_to"],
                        "read_status": item["read_status"],
                        "notes": item.get("notes", ""),
                    }
                    for item in resolutions
                ]
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(json.dumps({"candidates": len(candidates), "resolved": sum(1 for item in resolutions if item["read_status"] == "read"), "output_dir": str(args.output_dir)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
