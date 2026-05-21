#!/usr/bin/env python3
"""Lightweight benchmark checker for cross-subject regression examples.

The checker is deliberately conservative. It verifies file availability,
unit-key separation, rough exam-regime signals, lecture-source extractability,
and benchmark expectation wiring. It does not make content predictions.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    import fitz  # type: ignore
except Exception:  # pragma: no cover
    fitz = None

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover
    PdfReader = None

try:
    from essay_style_linter import lint_records, workbook_records
except Exception:  # pragma: no cover
    sys.path.append(str(Path(__file__).resolve().parent))
    try:
        from essay_style_linter import lint_records, workbook_records
    except Exception:  # pragma: no cover
        lint_records = None
        workbook_records = None

try:
    from docx_format_linter import lint_docx
except Exception:  # pragma: no cover
    sys.path.append(str(Path(__file__).resolve().parent))
    try:
        from docx_format_linter import lint_docx
    except Exception:  # pragma: no cover
        lint_docx = None


DEFAULT_SUITE = Path(__file__).resolve().parents[1] / "benchmarks" / "cross_subject_regression_suite.json"

REQUIRED_CONTRIBUTION_FIELDS = {
    "generic_contribution": "missing_generic_contribution",
    "transferable_rules": "missing_transferable_rules",
    "future_unit_diagnostic_questions": "missing_future_unit_diagnostic_questions",
    "non_transferable_content": "missing_non_transferable_content",
    "workflow_steps_tested": "missing_workflow_steps_tested",
    "anti_patterns_guarded_against": "missing_anti_patterns_guarded_against",
}


def normalise_benchmark_units(suite: dict) -> list[dict]:
    """Return a uniform list of benchmark unit records.

    Cross-subject fixtures use a `units` array. Single-unit fixtures, such as
    the BIOL21111 long-answer suite, store benchmark metadata at the root.
    """
    if isinstance(suite.get("units"), list):
        return suite["units"]

    if "unit_key" not in suite:
        return []

    source_examples = suite.get("source_examples", {})
    lecture_folder = source_examples.get("lecture_folder")
    return [
        {
            "unit_key": suite.get("unit_key"),
            "unit_code": suite.get("unit_code"),
            "lecture_source_examples": source_examples.get("lecture_sources", []),
            "source_folder_examples": [lecture_folder] if lecture_folder else [],
            "past_paper_paths": source_examples.get("formal_papers", []),
            "expected_regimes": suite.get("expected_regimes", []),
            "required_archetypes": suite.get("required_archetypes", []),
            "must_not": suite.get("hard_rules", []),
            "generic_contribution": suite.get("generic_contribution"),
            "transferable_rules": suite.get("transferable_rules", []),
            "future_unit_diagnostic_questions": suite.get("future_unit_diagnostic_questions", []),
            "non_transferable_content": suite.get("non_transferable_content", []),
            "workflow_steps_tested": suite.get("workflow_steps_tested", []),
            "anti_patterns_guarded_against": suite.get("anti_patterns_guarded_against", []),
        }
    ]


def pptx_text_and_slide_count(path: Path, max_chars: int = 20000) -> tuple[int, str]:
    texts: list[str] = []
    slides = 0
    with zipfile.ZipFile(path) as zf:
        names = sorted(
            [name for name in zf.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", name)],
            key=lambda n: int(re.search(r"slide(\d+)\.xml", n).group(1)),
        )
        slides = len(names)
        for name in names:
            xml = zf.read(name)
            root = ET.fromstring(xml)
            for node in root.iter():
                if node.tag.endswith("}t") and node.text:
                    texts.append(node.text)
            if sum(len(t) for t in texts) >= max_chars:
                break
    return slides, "\n".join(texts)[:max_chars]


def pdf_text(path: Path, max_pages: int = 3, max_chars: int = 12000) -> str:
    if fitz is not None:
        try:
            doc = fitz.open(path)
            return "\n".join(doc[i].get_text("text") for i in range(min(max_pages, doc.page_count)))[:max_chars]
        except Exception:
            pass
    if PdfReader is None:
        return ""
    try:
        reader = PdfReader(str(path))
        chunks = []
        for page in reader.pages[:max_pages]:
            chunks.append(page.extract_text() or "")
        return "\n".join(chunks)[:max_chars]
    except Exception:
        return ""


def year_from_name(name: str) -> str | None:
    match = re.search(r"\b(20\d{2}|19\d{2})\b", name)
    return match.group(1) if match else None


def infer_regime(text: str) -> list[str]:
    lower = text.lower()
    signals = []
    if "section a" in lower:
        signals.append("section_a")
    if "section b" in lower:
        signals.append("section_b")
    if "answer all" in lower:
        signals.append("answer_all")
    if "answer one" in lower or "answer 1" in lower:
        signals.append("answer_one")
    if "short answer" in lower or "concise" in lower:
        signals.append("short_answer")
    if "essay" in lower:
        signals.append("essay")
    if "problem" in lower or "data" in lower or "figure" in lower or "graph" in lower:
        signals.append("problem_data")
    return signals or ["unknown"]


def metadata_only_result(suite: dict, benchmark_units: list[dict], suite_name: str) -> dict:
    result = {
        "suite": suite.get("suite_name", suite_name),
        "hard_rule": suite.get("hard_rule") or "; ".join(suite.get("hard_rules", [])),
        "units": [],
        "generic_contribution_results": [],
        "workbook_lint_results": [],
        "example_essay_docx_results": [],
        "global_failures": [],
        "pass": True,
        "mode": "metadata_only",
    }
    if not benchmark_units:
        result["pass"] = False
        result["global_failures"].append({"type": "no_benchmark_units"})
        return result

    seen_unit_keys = set()
    for unit in benchmark_units:
        unit_key = unit["unit_key"]
        generic_contribution_failures = []
        qa_flags = []
        for field, flag in REQUIRED_CONTRIBUTION_FIELDS.items():
            if not unit.get(field):
                generic_contribution_failures.append(flag)
                qa_flags.append({"type": flag})
        if unit_key in seen_unit_keys:
            qa_flags.append({"type": "duplicate_unit_key"})
        seen_unit_keys.add(unit_key)

        status = "pass" if not qa_flags else "fail"
        if status != "pass":
            result["pass"] = False
        result["units"].append(
            {
                "unit_key": unit_key,
                "unit_key_unique": not any(flag["type"] == "duplicate_unit_key" for flag in qa_flags),
                "expected_regimes": unit.get("expected_regimes", []),
                "required_archetypes": unit.get("required_archetypes", []),
                "must_not": unit.get("must_not", []),
                "generic_contribution": unit.get("generic_contribution"),
                "transferable_rules": unit.get("transferable_rules", []),
                "future_unit_diagnostic_questions": unit.get("future_unit_diagnostic_questions", []),
                "non_transferable_content": unit.get("non_transferable_content", []),
                "workflow_steps_tested": unit.get("workflow_steps_tested", []),
                "anti_patterns_guarded_against": unit.get("anti_patterns_guarded_against", []),
                "status": status,
                "generic_contribution_status": "pass" if not generic_contribution_failures else "fail",
                "generic_contribution_failures": generic_contribution_failures,
                "qa_flags": qa_flags,
            }
        )
        result["generic_contribution_results"].append(
            {
                "source_unit": unit_key,
                "contribution_tested": unit.get("generic_contribution"),
                "transferable_rule": unit.get("transferable_rules", []),
                "future_unit_applicability": unit.get("future_unit_diagnostic_questions", []),
                "non_transferable_content_checked": bool(unit.get("non_transferable_content")),
                "pass_fail": "pass" if not generic_contribution_failures else "fail",
                "failures": generic_contribution_failures,
            }
        )

    if any(item["pass_fail"] != "pass" for item in result["generic_contribution_results"]):
        result["global_failures"].append({"type": "generic_contribution_metadata_incomplete"})
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", type=Path, default=DEFAULT_SUITE)
    parser.add_argument("--past-papers", type=Path)
    parser.add_argument("--metadata-only", action="store_true", help="Validate benchmark metadata without requiring private source files.")
    parser.add_argument("--workbook", action="append", type=Path, default=[], help="Optional generated workbook to validate with essay_style_linter.py.")
    parser.add_argument("--example-essay-docx-dir", type=Path, help="Optional Example_Essays_DOCX directory to validate.")
    parser.add_argument("--check-docx-format", action="store_true")
    parser.add_argument("--check-source-highlights", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    suite = json.loads(args.suite.read_text())
    benchmark_units = normalise_benchmark_units(suite)
    if args.metadata_only:
        result = metadata_only_result(suite, benchmark_units, args.suite.stem)
        text = json.dumps(result, indent=2)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text)
        else:
            print(text)
        return 0 if result["pass"] else 1

    result = {
        "suite": suite.get("suite_name", args.suite.stem),
        "hard_rule": suite.get("hard_rule") or "; ".join(suite.get("hard_rules", [])),
        "units": [],
        "generic_contribution_results": [],
        "workbook_lint_results": [],
        "example_essay_docx_results": [],
        "global_failures": [],
        "pass": True,
    }
    if not benchmark_units:
        result["pass"] = False
        result["global_failures"].append({"type": "no_benchmark_units"})

    seen_unit_keys = set()
    for unit in benchmark_units:
        unit_result = {
            "unit_key": unit["unit_key"],
            "unit_key_unique": unit["unit_key"] not in seen_unit_keys,
            "lecture_sources": [],
            "source_folders": [],
            "past_papers": [],
            "expected_regimes": unit.get("expected_regimes", []),
            "required_archetypes": unit.get("required_archetypes", []),
            "must_not": unit.get("must_not", []),
            "generic_contribution": unit.get("generic_contribution"),
            "transferable_rules": unit.get("transferable_rules", []),
            "future_unit_diagnostic_questions": unit.get("future_unit_diagnostic_questions", []),
            "non_transferable_content": unit.get("non_transferable_content", []),
            "workflow_steps_tested": unit.get("workflow_steps_tested", []),
            "anti_patterns_guarded_against": unit.get("anti_patterns_guarded_against", []),
            "status": "pass",
            "generic_contribution_status": "pass",
            "generic_contribution_failures": [],
            "qa_flags": [],
        }
        seen_unit_keys.add(unit["unit_key"])

        for field, flag in REQUIRED_CONTRIBUTION_FIELDS.items():
            if not unit.get(field):
                unit_result["generic_contribution_status"] = "fail"
                unit_result["generic_contribution_failures"].append(flag)
                unit_result["qa_flags"].append({"type": flag})

        for source in unit.get("lecture_source_examples", []):
            path = Path(source)
            record = {"path": str(path), "exists": path.exists(), "slide_count": None, "extractable": False}
            if path.exists() and path.suffix.lower() == ".pptx":
                try:
                    slides, text = pptx_text_and_slide_count(path)
                    record.update({"slide_count": slides, "extractable": bool(text.strip()), "sample_text": text[:300]})
                except Exception as exc:
                    record["error"] = str(exc)
            elif path.exists() and path.suffix.lower() == ".pdf":
                text = pdf_text(path)
                record.update({"extractable": bool(text.strip()), "sample_text": text[:300]})
            else:
                record["error"] = "missing_or_unsupported"
            if not record["exists"] or not record["extractable"]:
                unit_result["status"] = "fail"
                unit_result["qa_flags"].append({"type": "lecture_source_not_extractable", "path": str(path)})
            unit_result["lecture_sources"].append(record)

        for folder_source in unit.get("source_folder_examples", []):
            folder = Path(folder_source)
            record = {
                "path": str(folder),
                "exists": folder.exists(),
                "is_dir": folder.is_dir(),
                "file_count": None,
            }
            if folder.exists() and folder.is_dir():
                record["file_count"] = sum(1 for item in folder.rglob("*") if item.is_file())
            else:
                unit_result["status"] = "fail"
                unit_result["qa_flags"].append({"type": "source_folder_missing", "path": str(folder)})
            unit_result["source_folders"].append(record)

        explicit_papers = [Path(path) for path in unit.get("past_paper_paths", [])]
        if explicit_papers:
            papers = explicit_papers
            paper_source_record = {"source": "explicit_paths", "count": len(explicit_papers)}
        else:
            pattern = unit.get("past_paper_glob", "*")
            papers = sorted(args.past_papers.glob(pattern)) if args.past_papers else []
            paper_source_record = {
                "source": "glob",
                "glob": pattern,
                "count": len(papers),
                "past_papers_root": str(args.past_papers) if args.past_papers else None,
            }
        if not papers:
            unit_result["status"] = "fail"
            unit_result["qa_flags"].append({"type": "no_past_papers_found", **paper_source_record})
        for paper in papers:
            if not paper.exists():
                unit_result["status"] = "fail"
                unit_result["qa_flags"].append({"type": "past_paper_missing", "path": str(paper)})
                unit_result["past_papers"].append({
                    "path": str(paper),
                    "exists": False,
                    "year": year_from_name(paper.name),
                    "regime_signals": ["missing"],
                })
                continue
            text = pdf_text(paper) if paper.suffix.lower() == ".pdf" else ""
            unit_result["past_papers"].append({
                "path": str(paper),
                "exists": True,
                "year": year_from_name(paper.name),
                "regime_signals": infer_regime(text),
            })

        if not unit_result["unit_key_unique"]:
            unit_result["status"] = "fail"
            unit_result["qa_flags"].append({"type": "duplicate_unit_key"})
        result["generic_contribution_results"].append(
            {
                "source_unit": unit["unit_key"],
                "contribution_tested": unit.get("generic_contribution"),
                "transferable_rule": unit.get("transferable_rules", []),
                "future_unit_applicability": unit.get("future_unit_diagnostic_questions", []),
                "non_transferable_content_checked": bool(unit.get("non_transferable_content")),
                "pass_fail": unit_result["generic_contribution_status"],
                "failures": unit_result["generic_contribution_failures"],
            }
        )
        if unit_result["status"] != "pass" or unit_result["generic_contribution_status"] != "pass":
            result["pass"] = False
        result["units"].append(unit_result)

    contribution_failures = [
        item
        for item in result["generic_contribution_results"]
        if item["pass_fail"] != "pass"
    ]
    if contribution_failures:
        result["global_failures"].append(
            {
                "type": "generic_contribution_metadata_incomplete",
                "count": len(contribution_failures),
            }
        )

    for workbook in args.workbook:
        if lint_records is None or workbook_records is None:
            lint_result = {
                "path": str(workbook),
                "pass": False,
                "fail_reasons": ["essay_style_linter_unavailable"],
            }
        else:
            try:
                records = workbook_records(workbook)
                lint_result = lint_records(records, min_words=60, max_words=260)
                lint_result["path"] = str(workbook)
            except Exception as exc:
                lint_result = {
                    "path": str(workbook),
                    "pass": False,
                    "fail_reasons": ["workbook_lint_error"],
                    "error": str(exc),
                }
        result["workbook_lint_results"].append(lint_result)
        if not lint_result.get("pass"):
            result["pass"] = False
            result["global_failures"].append(
                {
                    "type": "workbook_essay_style_lint_failed",
                    "path": str(workbook),
                    "fail_reasons": lint_result.get("fail_reasons", []),
                }
            )

    if args.example_essay_docx_dir:
        docx_dir = args.example_essay_docx_dir
        docx_files = sorted(docx_dir.glob("*.docx")) if docx_dir.exists() else []
        manifest = docx_dir / "example_essay_manifest.json"
        source_audit = docx_dir / "example_essay_source_audit.json"
        docx_result = {
            "path": str(docx_dir),
            "exists": docx_dir.exists(),
            "docx_count": len(docx_files),
            "manifest_exists": manifest.exists(),
            "source_audit_exists": source_audit.exists(),
            "docx_lint_reports": [],
            "pass": True,
            "fail_reasons": [],
        }
        if not docx_dir.exists():
            docx_result["pass"] = False
            docx_result["fail_reasons"].append("example_essay_docx_dir_missing")
        if not docx_files:
            docx_result["pass"] = False
            docx_result["fail_reasons"].append("no_standalone_docx_essays_found")
        if not manifest.exists():
            docx_result["pass"] = False
            docx_result["fail_reasons"].append("example_essay_manifest_missing")
        if not source_audit.exists():
            docx_result["pass"] = False
            docx_result["fail_reasons"].append("example_essay_source_audit_missing")
        if (args.check_docx_format or args.check_source_highlights) and lint_docx is None:
            docx_result["pass"] = False
            docx_result["fail_reasons"].append("docx_format_linter_unavailable")
        elif args.check_docx_format or args.check_source_highlights:
            for docx_file in docx_files:
                try:
                    lint_report = lint_docx(docx_file)
                except Exception as exc:
                    lint_report = {"docx": str(docx_file), "status": "fail", "qa_flags": ["docx_lint_error"], "error": str(exc)}
                docx_result["docx_lint_reports"].append(lint_report)
                if lint_report.get("status") != "pass":
                    docx_result["pass"] = False
                    docx_result["fail_reasons"].append("docx_format_or_source_lint_failed")
        result["example_essay_docx_results"].append(docx_result)
        if not docx_result["pass"]:
            result["pass"] = False
            result["global_failures"].append(
                {
                    "type": "example_essay_docx_validation_failed",
                    "path": str(docx_dir),
                    "fail_reasons": docx_result["fail_reasons"],
                }
            )

    text = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    else:
        print(text)
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
