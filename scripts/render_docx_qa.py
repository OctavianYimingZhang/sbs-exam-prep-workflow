#!/usr/bin/env python3
"""Render or structurally inspect DOCX files for Example Essay QA."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import zipfile
from pathlib import Path


def structural_ooxml_check(path: Path) -> dict:
    try:
        with zipfile.ZipFile(path) as zf:
            names = set(zf.namelist())
            document_xml = zf.read("word/document.xml")
        return {
            "docx": str(path),
            "render_status": "render_unavailable_structural_ooxml_only",
            "structural_ooxml_pass": "word/document.xml" in names and len(document_xml) > 100,
            "qa_flags": ["render_unavailable_structural_ooxml_only"],
        }
    except Exception as exc:
        return {"docx": str(path), "render_status": "fail", "structural_ooxml_pass": False, "qa_flags": ["docx_ooxml_unreadable"], "error": str(exc)}


def render_with_libreoffice(path: Path, out_dir: Path) -> dict:
    binary = shutil.which("soffice") or shutil.which("libreoffice")
    if not binary:
        return structural_ooxml_check(path)
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            [binary, "--headless", "--convert-to", "pdf", "--outdir", str(out_dir), str(path)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
        )
        pdf = out_dir / f"{path.stem}.pdf"
        return {
            "docx": str(path),
            "render_status": "pass" if pdf.exists() and pdf.stat().st_size > 1000 else "fail",
            "pdf": str(pdf),
            "qa_flags": [] if pdf.exists() and pdf.stat().st_size > 1000 else ["docx_render_pdf_missing_or_blank"],
        }
    except Exception as exc:
        fallback = structural_ooxml_check(path)
        fallback["libreoffice_error"] = str(exc)
        return fallback


def collect(path: Path) -> list[Path]:
    if path.is_dir():
        return sorted(path.glob("*.docx"))
    return [path]


def main() -> int:
    parser = argparse.ArgumentParser(description="Render DOCX to PDF for visual QA, or perform structural OOXML fallback.")
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    reports = []
    for path in args.paths:
        for docx in collect(path):
            reports.append(render_with_libreoffice(docx, args.output_dir))
    status = "pass" if all(report.get("render_status") in {"pass", "render_unavailable_structural_ooxml_only"} and report.get("qa_flags") != ["docx_ooxml_unreadable"] for report in reports) else "fail"
    result = {"status": status, "reports": reports}
    text = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
