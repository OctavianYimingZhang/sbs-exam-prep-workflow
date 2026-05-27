# Cross-Subject Regression Protocol

Benchmark fixtures are used only to test generic Skill behaviour. A benchmark name, course name, example topic, lecturer, year, or recurring content pattern must never trigger production logic.

Regression asks whether the workflow obeys general evidence and output rules when faced with different source shapes. It does not ask whether the workflow can repeat the same old example.

Hard rule:

```text
Target source-set evidence = factual content + direct prediction evidence.
Old or structurally different target evidence = coverage/schema evidence unless comparability is proven.
External examples = transferable workflow lessons only.
Style/layout exemplars = wording, structure, density, formatting, and answer organisation only.
Benchmark fixtures = tests only; never production rules.
```

## Benchmark Contribution Schema

Every benchmark or external example must be converted into this schema before it can influence workflow design:

```yaml
BenchmarkContribution:
  benchmark_id:
  source_materials:
    - lecture_slides
    - lecture_notes
    - formal_past_papers
    - practical_materials
    - mocks_or_quizzes
    - answer_keys
    - marking_guidance
    - exemplar_answers
    - image_examples
  observed_source_pattern:
  what_worked:
    - reusable workflow behaviour demonstrated by the example
  what_failed_or_should_not_transfer:
    - concrete topic/content/example/lecturer/year/detail that must not be reused
  generic_skill_contribution:
    - evidence handling
    - regime split
    - question-type routing
    - answer-shape modelling
    - output layout
    - Example Essay language quality
    - citation or extra-reading discipline
    - QA rule
  transferable_rule:
    - evidence-condition-based rule for future source sets
  diagnostic_questions:
    - question to ask before applying the rule
  anti_patterns_prevented:
    - content leakage
    - production branching on benchmark identity
  validation_checks:
    - check
```

## Required Regression Axes

Each benchmark run should validate the generic behaviour it claims to teach.

Source handling:

- files are classified by role and trust level before analysis;
- unreadable or weak-OCR material is flagged rather than inferred;
- old or structurally different papers are separated from current prediction evidence;
- external examples are recorded as transferable workflow lessons, not content evidence.

Question-type routing:

- MCQ, short answer, essay, data/problem, and project/scenario long answer are separated;
- essay-only logic is not applied to MCQ or problem/data questions;
- mixed-format papers keep separate section logic.

Exam-strategy inference:

- answer-all versus answer-one rules are detected;
- section structure, mark weights, word limits, and timing are parsed;
- current-regime predictions are not driven by old-regime format;
- confidence is reported without fake precision.

Knowledge-point construction:

- KPs are built from examinable reasoning blocks rather than slide count;
- adjacent source pages are merged only when they teach one examinable mechanism, process, comparison, method, data operation, or scenario;
- source order is preserved in the compatibility lecture walkthrough and used diagnostically in Academic Exam-Ready Notes;
- page/slide coverage is kept in images/source maps, not narrated inside student prose.

Language quality:

- student-facing explanations use `claim -> mechanism/process/evidence -> consequence`;
- complete Example Essays use paragraph functions, not slide summaries;
- examples support wider claims instead of becoming disconnected case descriptions;
- repeated low-value detail is compressed;
- necessary academic mechanisms are preserved;
- contrast language is explicit;
- citations are minimal, sufficient, and verified.

Output layout:

- student-facing outputs keep evidence/provenance fields out unless an audit package is requested;
- original slide/page images remain visible and aspect-ratio-preserved when included;
- the add-on report adapts to question type;
- complete Example Essays are in DOCX output, not spreadsheet cells.

QA:

- predictions are labelled conservatively by question type, including predicted essay themes for essay/problem-essay outputs;
- source uncertainty is flagged;
- unsupported claims are omitted or flagged;
- benchmark/example leakage is flagged;
- generated prose is linted when tooling exists.

## Example Essay DOCX Regression

When an Example Essay DOCX directory is supplied to the regression checker, validate:

- complete essays are present in the requested DOCX output, either inside `Essay_Module_Example_Essays.docx` or as separate `.docx` files when separate files are requested;
- internal QA artefacts such as `example_essay_manifest.json` and `example_essay_source_audit.json` exist in a separate internal QA directory unless the user explicitly asks for an audit package;
- no generated Example Essay exists only as a spreadsheet row;
- DOCX formatting passes the current contract: Arial, 2.5 cm margins, 1.5 line spacing, justified body, centered title, left-aligned subtitles/headings, and no empty spacer paragraphs;
- yellow-highlighted runs map to uploaded Extra Reading Book chapter/section anchors;
- green-highlighted runs map to read lecture-slide citation originals and include author-year in-text citation;
- every body paragraph has source anchors;
- language checks pass for compression, claim-led paragraphs, citation discipline, and example-as-evidence use.

## Benchmark Pass/Fail Output

Regression output must report both:

- benchmark fixture pass/fail; and
- generic contribution pass/fail.

```yaml
RegressionResult:
  benchmark_id:
  fixture_status: pass | fail
  generic_contribution_status: pass | fail
  validated_transferable_rules:
    - rule:
      evidence:
      checks_passed:
  leakage_checks:
    benchmark_identity_used_as_trigger: false
    benchmark_content_used_as_fact: false
    external_example_used_as_prediction: false
  qa_flags:
    - flag
```

## Automatic Fail Conditions

Fail regression if:

- production logic branches on benchmark identity;
- benchmark factual content appears in a new source set's factual answer or prediction evidence without independent target-source verification;
- a benchmark lacks generic contribution metadata;
- a benchmark lacks non-transferable-content metadata;
- old or structurally different papers drive current-regime predictions without comparability evidence;
- generated student-facing prose contains slide/page narration as the main explanation;
- complete Example Essays are exported only as spreadsheet rows;
- Example Essay DOCX formatting or source-highlighting checks fail;
- extra-reading or citation-source content is used without verification.

## Success Condition

The regression suite passes when benchmark examples improve only generic workflow behaviour:

- evidence separation;
- exam-regime split;
- question-type routing;
- KP granularity;
- source-order coverage;
- output layout adaptation;
- Example Essay language quality;
- citation and extra-reading discipline;
- no factual leakage from examples into new work.
