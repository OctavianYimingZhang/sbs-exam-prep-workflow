#!/usr/bin/env python3
"""Lint Knowledge Walkthrough DOCX files for formatting and student-output policy."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    from docx import Document  # type: ignore
    from docx.enum.text import WD_ALIGN_PARAGRAPH  # type: ignore
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"python-docx is required: {exc}")


FORBIDDEN_TEXT = {
    "source anchor",
    "confidence",
    "evidence score",
    "recurrence count",
    "examiner operation",
    "discriminator axis",
    "essay plan",
    "full example essay",
    "practice question",
    "answer key",
    "past paper year",
    "prediction score",
    "according to slide",
    "slides say",
    "ppt page",
}


def collect_docx(path: Path) -> list[Path]:
    if path.is_dir():
        return sorted(path.glob("*.docx"))
    return [path]


def lint_docx(path: Path) -> dict[str, Any]:
    doc = Document(path)
    failures: list[dict[str, Any]] = []
    text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
    lowered = text.lower()
    for phrase in sorted(FORBIDDEN_TEXT):
        if phrase in lowered:
            failures.append({"type": "forbidden_student_text", "phrase": phrase})

    required_terms = ["What This Lecture Is About", "Module Map", "Knowledge Walkthrough", "Key Logic", "Must Master", "Lecture Recap"]
    heading_terms = set(required_terms) | {"Core Logic", "What This Module Explains", "Common Confusions", "How To Use This Document"}
    for term in required_terms:
        if term not in text:
            failures.append({"type": "missing_required_section", "section": term})

    section = doc.sections[0]
    margins_cm = [section.top_margin.cm, section.bottom_margin.cm, section.left_margin.cm, section.right_margin.cm]
    if any(abs(value - 2.5) > 0.08 for value in margins_cm):
        failures.append({"type": "margins_not_2_5_cm", "margins_cm": margins_cm})

    visible_index = 0
    for paragraph in doc.paragraphs:
        if not paragraph.text.strip():
            continue
        visible_index += 1
        if paragraph.paragraph_format.line_spacing != 1.5:
            failures.append({"type": "line_spacing_not_1_5", "paragraph": visible_index})
        if visible_index == 1:
            if paragraph.alignment != WD_ALIGN_PARAGRAPH.CENTER:
                failures.append({"type": "title_not_centered"})
        elif paragraph.text in heading_terms or paragraph.text.startswith(("Lecture:", "Module:")):
            if paragraph.alignment != WD_ALIGN_PARAGRAPH.LEFT:
                failures.append({"type": "heading_not_left", "paragraph": visible_index, "text": paragraph.text[:80]})
        else:
            if paragraph.alignment != WD_ALIGN_PARAGRAPH.JUSTIFY:
                failures.append({"type": "body_not_justified", "paragraph": visible_index, "text": paragraph.text[:80]})
        for run_idx, run in enumerate([run for run in paragraph.runs if run.text], start=1):
            if run.font.name != "Arial":
                failures.append({"type": "run_font_not_arial", "paragraph": visible_index, "run": run_idx, "font": run.font.name})

    return {
        "docx": str(path),
        "status": "pass" if not failures else "fail",
        "failures": failures,
        "paragraph_count": len([p for p in doc.paragraphs if p.text.strip()]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    reports = []
    for path in args.paths:
        for docx in collect_docx(path):
            reports.append(lint_docx(docx))
    if not reports:
        reports.append({"status": "fail", "failures": [{"type": "no_docx_found"}]})
    result = {"status": "pass" if all(report["status"] == "pass" for report in reports) else "fail", "reports": reports}
    text = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
