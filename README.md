# SBS Exam Prep Workflow

`sbs-exam-prep-workflow` is a Codex Skill for building an Excel-first exam preparation workflow from lecture materials, past papers, mocks, practice materials, exemplars, notes, and marking guidance.

The workflow is archetype-centric rather than topic-hotness-first:

```text
Exam blueprint -> question archetype -> slot grammar -> compatible knowledge points -> preparation action
```

## Academic Integrity Boundary

This Skill is for preparation, revision, source organization, workbook generation, and practice-question planning. It must not be used for a live exam, active assessed submission, or contract-cheating request.

Predictions must be labelled as predicted practice questions, never official exam questions.

## Repository Contents

- `SKILL.md`: top-level Skill instructions and output contract.
- `references/`: protocol documents for input processing, question-type routing, scoring, essay synthesis, Excel output, evidence policy, and regression checks.
- `scripts/`: helper CLIs for source extraction, unit grouping, archetype models, workbook language linting, example-essay DOCX generation, DOCX linting, citation resolution, extra-reading matching, and regression checks.
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
python scripts/extract_sources.py /path/to/input_dir --output /path/to/output_dir --target-unit "Target Unit"
```

Group sources by unit/regime after inventory:

```bash
python scripts/unit_grouper.py /path/to/output_dir/source_manifest.json --output /path/to/output_dir/unit_groups.json
```

Lint generated workbook prose:

```bash
python scripts/essay_style_linter.py --workbook /path/to/workbook.xlsx
```

Run public metadata-only regression checks:

```bash
python scripts/cross_subject_regression_check.py --metadata-only --suite benchmarks/cross_subject_regression_suite.json
python scripts/cross_subject_regression_check.py --metadata-only --suite benchmarks/biol21111_long_answer_suite.json
```

Run full regression checks against private local materials:

```bash
python scripts/cross_subject_regression_check.py \
  --suite benchmarks/cross_subject_regression_suite.json \
  --past-papers /path/to/private/past_papers
```

## Benchmark Sanitization

The benchmark files are contribution and regression fixtures. They preserve generic workflow lessons such as regime splitting, question-type routing, workbook layout adaptation, and cross-unit leakage prevention.

They intentionally exclude real lecture slides, past papers, notes, mocks, student files, generated workbooks, local absolute paths, and cached run outputs.

## License

MIT.
