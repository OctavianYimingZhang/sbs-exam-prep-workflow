# SBS Exam Prep Workflow

`sbs-exam-prep-workflow` is a Codex Skill for building an Excel-first exam preparation workflow from lecture materials, past papers, mocks, practice materials, exemplars, notes, and marking guidance.

The workflow is archetype-centric rather than topic-hotness-first:

```text
Exam blueprint -> question archetype -> slot grammar -> compatible knowledge points -> preparation action
```

## Academic Integrity Boundary

This Skill is for preparation, revision, source organization, workbook generation, and practice-question planning. It must not be used for a live exam, active assessed submission, or contract-cheating request.

Essay/problem-essay predictions must be labelled as predicted themes, with any stems marked only as practice variants. No prediction should be presented as an official exam question.

## Repository Contents

- `SKILL.md`: top-level Skill instructions and output contract.
- `references/`: protocol documents for input processing, question-type routing, scoring, shared language quality, example analysis, gap closure, Excel/DOCX output, evidence policy, and regression checks.
- `scripts/`: helper CLIs for source extraction, target grouping, archetype models, example-corpus analysis, workbook and Example Essay language linting, DOCX generation/linting, citation resolution, extra-reading matching, gap reporting, identity scanning, GitHub-ready QA, and regression checks.
- `schemas/`: JSON schemas for language deltas, example contributions, Example Essay plans, and gap reports.
- `benchmarks/`: sanitized benchmark metadata and lint fixtures. These files preserve transferable regression rules only; they do not contain private source files.
- `agents/`: optional Skill interface metadata.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The scripts are plain Python files. Optional document extraction quality depends on installed PDF/DOCX libraries and source-file quality.

## Common Commands

Inventory sources:

```bash
python scripts/extract_sources.py /path/to/input_dir --output /path/to/output_dir --target "Target Course"
```

Group sources by target/regime after inventory:

```bash
python scripts/target_grouper.py /path/to/output_dir/source_scan.json --output /path/to/output_dir/target_groups.json
```

Lint generated workbook prose:

```bash
python scripts/essay_style_linter.py --workbook /path/to/workbook.xlsx
```

Lint complete Example Essay language:

```bash
python scripts/example_essay_language_linter.py --plan /path/to/example_essay_plan.json
```

Lint essay/problem-essay prediction wording:

```bash
python scripts/essay_theme_prediction_linter.py
```

Prepare citation resolution or classic-experiment fallback for Example Essay mode:

```bash
python scripts/lecture_citation_resolver.py --input /path/to/slides.pptx --output-dir /path/to/internal_qa --classic-search-if-no-citations
```

Check that a public output folder excludes internal helper artefacts:

```bash
python scripts/final_deliverable_linter.py /path/to/public_output
```

Analyse external examples into transferable deltas:

```bash
python scripts/analyze_example_corpus.py /path/to/examples --output /path/to/example_analysis.json --max-files 80
```

Run public metadata-only regression checks:

```bash
python scripts/cross_subject_regression_check.py --metadata-only --suite benchmarks/cross_subject_regression_suite.json
python scripts/cross_subject_regression_check.py --metadata-only --suite benchmarks/method_long_answer_suite.json
```

Run full regression checks against private local materials:

```bash
python scripts/cross_subject_regression_check.py \
  --suite benchmarks/cross_subject_regression_suite.json \
  --past-papers /path/to/private/past_papers
```

Run the full GitHub-ready local gate:

```bash
python scripts/github_ready_check.py
```

## Benchmark Sanitization

The benchmark files are contribution and regression fixtures. They preserve generic workflow lessons such as regime splitting, question-type routing, workbook layout adaptation, and cross-target leakage prevention.

They intentionally exclude real lecture slides, past papers, notes, mocks, student files, generated workbooks, local absolute paths, and cached run outputs.

## License

MIT.
