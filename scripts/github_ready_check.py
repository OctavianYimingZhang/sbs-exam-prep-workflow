#!/usr/bin/env python3
"""Run the local GitHub-ready QA gate for this Skill repository."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def run_command(name: str, command: list[str], *, expect_failure: bool = False) -> dict[str, Any]:
    proc = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    passed = proc.returncode != 0 if expect_failure else proc.returncode == 0
    return {
        "name": name,
        "command": " ".join(command),
        "returncode": proc.returncode,
        "expected_failure": expect_failure,
        "status": "pass" if passed else "fail",
        "stdout": proc.stdout[-4000:],
        "stderr": proc.stderr[-4000:],
    }


def public_safety_scan() -> dict[str, Any]:
    patterns = [
        "/" + "Users/",
        "One" + "Drive",
        "Cloud" + "Storage",
        "octavian" + "zhang",
        "Desk" + "top",
        "University of " + "Manchester",
        "School of " + "Biological",
    ]
    regex = re.compile("|".join(re.escape(pattern) for pattern in patterns))
    hits = []
    for path in ROOT.rglob("*"):
        if any(part in {".git", "__pycache__", ".venv"} for part in path.parts) or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if regex.search(text):
            hits.append(str(path.relative_to(ROOT)))
    return {
        "name": "public_safety_scan",
        "command": "internal public safety scan",
        "status": "pass" if not hits else "fail",
        "hits": hits,
    }


def git_status_check(require_clean: bool) -> dict[str, Any]:
    proc = subprocess.run(["git", "status", "--short"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    dirty = bool(proc.stdout.strip())
    passed = proc.returncode == 0 and (not require_clean or not dirty)
    return {
        "name": "git_status",
        "command": "git status --short",
        "status": "pass" if passed else "fail",
        "dirty": dirty,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run GitHub-ready checks.")
    parser.add_argument("--ci", action="store_true")
    parser.add_argument("--require-clean", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    py = sys.executable
    checks: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="sbs_github_ready_") as tmp:
        tmp_dir = Path(tmp)
        positive_dir = tmp_dir / "positive_docx"
        negative_dir = tmp_dir / "negative_docx"
        deliverable_dir = tmp_dir / "deliverable_docx"
        deliverable_qa_dir = tmp_dir / "deliverable_docx_internal_qa"
        bad_public_dir = tmp_dir / "bad_public_output"
        citation_fallback_dir = tmp_dir / "citation_fallback"
        past_paper_extract_dir = tmp_dir / "past_paper_question_extract"
        bad_public_dir.mkdir(parents=True, exist_ok=True)
        (bad_public_dir / "example_essay_manifest.json").write_text("{}", encoding="utf-8")
        checks.extend(
            [
                run_command("compile_scripts", [py, "-m", "compileall", "-q", "scripts"]),
                run_command("ontology_contract", [py, "scripts/ontology_linter.py"]),
                run_command("workbook_language_fixture", [py, "scripts/essay_style_linter.py", "--fixture", "benchmarks/kp_essay_style_linter_fixtures.json"]),
                run_command("example_essay_language_fixture", [py, "scripts/example_essay_language_linter.py", "--fixture", "benchmarks/example_essay_language_linter_fixtures.json"]),
                run_command("essay_theme_prediction_language", [py, "scripts/essay_theme_prediction_linter.py"]),
                run_command(
                    "citation_fallback_fixture",
                    [
                        py,
                        "scripts/lecture_citation_resolver.py",
                        "--input",
                        "tests/fixtures/citation_fallback/no_citation_lecture.txt",
                        "--output-dir",
                        str(citation_fallback_dir),
                        "--classic-search-if-no-citations",
                    ],
                ),
                run_command("citation_fallback_lint", [py, "scripts/citation_fallback_linter.py", "--dir", str(citation_fallback_dir), "--require-classic-plan"]),
                run_command("cross_subject_metadata", [py, "scripts/cross_subject_regression_check.py", "--metadata-only", "--suite", "benchmarks/cross_subject_regression_suite.json"]),
                run_command("method_long_answer_metadata", [py, "scripts/cross_subject_regression_check.py", "--metadata-only", "--suite", "benchmarks/method_long_answer_suite.json"]),
                run_command("past_paper_prediction_metadata", [py, "scripts/cross_subject_regression_check.py", "--metadata-only", "--suite", "benchmarks/past_paper_prediction_suite.json"]),
                run_command(
                    "past_paper_question_extract_fixture",
                    [
                        py,
                        "scripts/extract_past_paper_questions.py",
                        "tests/fixtures/past_paper_question_extraction/fake_mixed_paper_2025.txt",
                        "--target-group-key",
                        "Benchmark_Generic",
                        "--current-regime-key",
                        "current_2025",
                        "--output-dir",
                        str(past_paper_extract_dir),
                    ],
                ),
                run_command(
                    "past_paper_prediction_lint",
                    [
                        py,
                        "scripts/past_paper_prediction_linter.py",
                        "--input",
                        str(past_paper_extract_dir / "past_paper_questions.json"),
                        "--suite",
                        "benchmarks/past_paper_prediction_suite.json",
                    ],
                ),
                run_command("identity_trigger_scan", [py, "scripts/no_identity_trigger_linter.py"]),
                run_command(
                    "positive_docx_generate_strict",
                    [
                        py,
                        "scripts/generate_example_essay_docx.py",
                        "--plan",
                        "tests/fixtures/example_essay_docx/positive_docx_plan.json",
                        "--output-dir",
                        str(positive_dir),
                        "--clean",
                        "--strict",
                    ],
                ),
            ]
        )
        checks.append(run_command("positive_docx_format_and_language", [py, "scripts/docx_format_linter.py", str(positive_dir), "--check-language"]))
        checks.append(
            run_command(
                "deliverable_only_docx_generate",
                [
                    py,
                    "scripts/generate_example_essay_docx.py",
                    "--plan",
                    "tests/fixtures/example_essay_docx/positive_docx_plan.json",
                    "--output-dir",
                    str(deliverable_dir),
                    "--qa-dir",
                    str(deliverable_qa_dir),
                    "--clean",
                    "--strict",
                    "--deliverable-only",
                ],
            )
        )
        checks.append(run_command("public_output_has_no_helper_artifacts", [py, "scripts/final_deliverable_linter.py", str(deliverable_dir)]))
        checks.append(
            run_command(
                "public_output_rejects_helper_artifacts",
                [py, "scripts/final_deliverable_linter.py", str(bad_public_dir)],
                expect_failure=True,
            )
        )
        checks.append(
            run_command(
                "negative_docx_strict_rejects_bad_source_plan",
                [
                    py,
                    "scripts/generate_example_essay_docx.py",
                    "--plan",
                    "tests/fixtures/example_essay_docx/negative_source_plan.json",
                    "--output-dir",
                    str(negative_dir),
                    "--clean",
                    "--strict",
                ],
                expect_failure=True,
            )
        )

    checks.append(public_safety_scan())
    checks.append(git_status_check(require_clean=args.require_clean))

    passed = all(check.get("status") == "pass" for check in checks)
    result = {
        "status": "pass" if passed else "fail",
        "checks": checks,
    }
    text = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
