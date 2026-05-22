---
name: sbs-exam-prep-workflow
description: Excel-first exam-preparation workflow for lecture slides, past papers, practical materials, MCQ, short-answer, long-answer, essay prompts, extra reading recommendations, recommended books, exemplars, marking guidance, and optional DOCX-first Example Essays.
---

# SBS Exam Prep Workflow

Build an evidence-grounded exam-preparation system from the student's supplied materials. The workflow starts from first principles:

```text
Inputs -> exam format -> question type -> examiner operation -> knowledge point -> preparation output
```

The workflow is not topic-hotness-first. Frequency and recency are auxiliary signals. The core task is to infer how the examiner asks questions, what kind of answer each question type rewards, and what preparation artefact best matches that strategy.

Default output is an Excel-first student workbook. Complete Example Essays are generated only when explicitly requested; they are DOCX-first and one document per essay. Do not help with a live exam, active assessed submission, or contract-cheating request.

## Evidence Boundary

Classify every input before analysis:

- Lecture slides and official notes are the primary source for factual course content.
- Formal past papers define exam format, answer rules, question type, and current prediction evidence.
- Practical materials, mocks, quizzes, answer keys, and exemplars support coverage, answer style, and practice planning only unless official guidance says they are representative.
- Extra Reading recommendations and recommended books enrich an answer only after the relevant chapter, section, paper, DOI, PubMed record, publisher page, or textbook source has been verified.
- If no extra reading is supplied, perform online academic search only for directly relevant peer-reviewed papers, textbooks, publisher pages, PubMed/Google Scholar/DOI records, or official academic sources.
- If the user asks for Example Essays but supplies no citations, first mine the relevant lecture slides for citation information and resolve/read the original source. If the slides contain no usable citations, find several verified classic experiments or landmark primary studies that directly support the lecture mechanism. Do not insert any citation until the source is verified and read.
- Student annotations and image examples can teach style or interpretation, but they are not factual authority unless verified against official course material or reliable academic sources.
- Cross-course examples and benchmark fixtures are tests and style references only. They must be abstracted into transferable workflow rules and never used as factual content or prediction evidence for a new source set.

## Mandatory References

- `references/input_processing_protocol.md`: source roles, trust levels, evidence use, extraction, and format fields.
- `references/modular_entrypoints_protocol.md`: standalone and full-workflow entry points.
- `references/question_type_protocol.md`: MCQ, short-answer, essay, and long-answer routing.
- `references/scoring_and_pattern_protocol.md`: pattern inference, retention, recency, and confidence rules.
- `references/kp_essay_synthesis_protocol.md`: workbook explanation synthesis.
- `references/language_quality_contract.md`: shared prose-quality rules for KP synthesis, Example Essays, and long-answer prose.
- `references/example_analysis_protocol.md`: how examples and external reviews become transferable rules without becoming factual content.
- `references/gap_closure_loop_protocol.md`: iterative example-analysis, update, lint, and gap-closure completion condition.
- `references/essay_generation_protocol.md`: Example Essay planning, lecture-logic extraction, language quality, extra-reading integration, and examiner-fit checks.
- `references/example_essay_docx_output_protocol.md`: DOCX-first Example Essay output, formatting, highlighting, source audit, and linting.
- `references/essay_synthesis_protocol.md`: essay-style lecture knowledge synthesis.
- `references/long_answer_example_protocol.md`: project/scenario long-answer model-answer logic.
- `references/practical_data_problem_protocol.md`: practical, data, problem, case-study, numerical, spotter, and answer-key workflows.
- `references/excel_output_protocol.md`: workbook layout and student-facing formatting.
- `references/subagent_protocol.md`: optional modular/subagent responsibilities and handoff schemas.
- `references/evidence_policy.md`: source hierarchy, citation verification, extra-reading policy, and hard negatives.
- `references/cross_subject_regression_protocol.md`: benchmark rules that validate generic behaviour without becoming production triggers.
- `references/github_release_protocol.md`: local QA, sync, commit, and push requirements.

Use helper scripts where available for source extraction, example-corpus analysis, grouping, archetype schemas, workbook language linting, Example Essay language linting, DOCX generation, DOCX formatting linting, citation resolution, extra-reading chapter matching, source audit, render QA, identity-trigger linting, gap reporting, GitHub-ready QA, and regression checks. Helper scripts are implementation aids; production behaviour must be controlled by parsed evidence conditions, not by benchmark names.

## Workflow

### 0. Route The Request

Decide whether the user requested:

- source inventory only;
- exam-format diagnosis;
- prediction workbook;
- MCQ prep;
- short-answer prep;
- long-answer/project answer planning;
- complete Example Essays;
- audit/regression only;
- the full workflow.

Run only the requested module and its minimum dependencies. If the user supplies valid intermediate artefacts, use them directly. Report modules run, modules skipped, and artefacts generated.

### 1. Build Source Inventory

For every supplied or discovered file, record:

- file role;
- source trust level;
- extraction status;
- year if safely detectable;
- target course/module group if safely detectable;
- exam regime if safely detectable;
- allowed evidence use;
- unresolved extraction or OCR risks.

Never infer hidden content from failed extraction, unsupported files, weak OCR, or unreadable images.

### 2. Split Exam Regimes

Compare papers only inside the same target course/module group. Split regimes when answer rules, timing, mark weights, section structure, permitted choices, dominant question type, or submission format changes.

Old or structurally different papers can support concept coverage and answer-schema practice. They must not control current blueprint prediction unless comparability is proven.

### 3. Classify Question Type

Classify each question before prediction:

- MCQ / single best answer;
- fill-blank;
- short answer;
- structured practical/problem/data question;
- essay;
- project/scenario long answer;
- mixed-format paper.

Do not apply essay-only scoring logic to MCQ, fill-blank, short-answer, or problem/data questions. The far-right workbook preparation area must adapt to detected question type.

If examples, answer keys, feedback slides, existing analysis workbooks, practical protocols, or external review notes are supplied, run Automatic Example Analysis before using them. Convert them into `ExampleContribution` or `LanguageDelta` records. Do not use their factual content as target evidence unless independently verified from the target source set.

### 4. Diagnose Exam Strategy

Parse:

- duration;
- sections;
- answer-all versus answer-one rules;
- question counts;
- mark weights;
- word/page limits;
- figure, citation, calculator, or formatting rules;
- practical/data requirements;
- scenario/project requirements;
- missing or contradictory evidence.

The selected preparation strategy follows the exam strategy:

- Stable essay or problem-essay regime: predict examinable themes by lecture scope, then build paragraph plans and essay-ready KP synthesis. Do not make exact question wording the default prediction product.
- MCQ-heavy regime: build discriminator axes, contrast tables, exception lists, mechanism-order traps, and wrong-option diagnosis.
- Short-answer regime: build 2/4/6/8-mark answer schemas with concise exam answers and reference expansions.
- Data/problem regime: build input -> operation -> inference -> limitation -> follow-up logic.
- Project/scenario long-answer regime: build method -> readout -> interpretation -> control -> caveat answers.
- Mixed regime: keep one workbook but separate prep logic by section and question type.
- Practical/protocol regime: build aim -> method principle -> steps -> readout -> interpretation -> control -> limitation outputs.

### 5. Segment Lecture Content

Segment lecture sources by lecture title, objectives, summaries, module markers, topic transitions, figures, methods, data, comparisons, and repeated mechanisms.

Create knowledge points from examinable reasoning blocks, not from every slide. A valid knowledge point must be usable as one MCQ concept, one short-answer mark cluster, one essay paragraph, or one part of a long-answer plan.

Use generic segmentation patterns:

```text
mechanism -> evidence -> consequence
process input -> actors -> mechanism -> output
method principle -> scenario application -> readout -> interpretation -> control
data -> inference -> limitation -> further test
comparison axis -> examples -> synthesis
problem -> proposed solution -> evidence -> sector/clinical/scientific implication
```

### 6. Produce Knowledge-Point Synthesis

For workbook explanation cells, write direct student-facing prose:

```text
claim -> mechanism -> evidence/example -> consequence
```

Remove slide/page narration, source-tracing prose, and instructions to the student. The explanation cell is not a coverage audit. Page ranges, original slide images, source maps, and diagnostics carry coverage.

If evidence is too weak, write only the conservative supported claim and flag uncertainty.

### 7. Infer Examiner Operations

Extract operations, not just topics:

```text
task verb + input format + cognitive operation + expected answer shape + marking logic
```

Track rotating slots such as examples, figures, methods, scenarios, diseases, molecules, theories, case studies, calculations, or datasets. A slot recurring does not prove that the same factual filler will recur.

Report frequency, retention, recency, lecture centrality, question-shape fit, and confidence separately. Do not report fake precision from a small paper set.

### 8. Generate Question-Type Outputs

MCQ:

- concept discriminators;
- distractor families;
- contrast tables;
- exception traps;
- mechanism-order traps;
- concise flashcards.

Short answer:

- mark-producing answer schema;
- concise `Exam Answer`;
- fuller `Reference Expansion`;
- required terms, examples, and controls.

Essay / problem-essay:

- predicted examinable themes, with lecture scope, examiner operation, and optional practice angles;
- paragraph plans;
- essay-style knowledge-point explanations;
- no complete essays unless explicitly requested.

Long answer / project / scenario:

- question deconstruction;
- method families;
- expected readouts;
- interpretation logic;
- controls, caveats, limitations;
- compact model answer only when explicitly requested.

### 9. Example Essay Mode

Trigger only when the user explicitly asks for complete `Example Essay`, `model essay`, `full essay-style answer`, `write an essay`, or equivalent complete essay documents.

Run the internal sequence in `references/essay_generation_protocol.md` before drafting:

```text
question analysis
lecture slide scope detection
lecture slide reading
lecture logic reconstruction
citation detection and original-source reading
classic-experiment fallback when slide citations are absent
extra-reading chapter matching and reading
knowledge inventory
paragraph plan
language compression plan
highlight plan
source-to-run mapping
DOCX generation
DOCX format linting
visual/render QA
source audit
examiner-fit checklist
```

Example Essay language must follow these rules:

- start each paragraph with a claim or problem, not a vague topic label;
- build the paragraph through cause, mechanism, evidence, scope, and consequence;
- for evidence-heavy paragraphs, convert examples and experiments into `evidence -> mechanism -> interpretation -> limitation`;
- compress repeated points and low-value detail, but do not remove necessary academic mechanisms;
- remove lecture-route narration and exam-guidance phrasing from the essay body; the essay must answer, not describe how the source was taught or how the student should answer;
- use examples as evidence for a broader argument, not as disconnected case descriptions;
- make contrasts explicit and non-ambiguous;
- write sector-level, system-level, biological, clinical, or methodological implications when the question requires them;
- use citations only where they support non-obvious facts, theory, mechanisms, methods, evidence, or sector-level claims;
- calibrate citation strength: use language such as `supports`, `implicates`, `is consistent with`, or `contributes to` unless the verified source directly proves the stronger causal claim;
- avoid citation stacking;
- omit unsupported claims rather than inventing sources;
- add length only when it adds mechanism, evidence, interpretation, limitation, or a required contrast;
- conclude by synthesising the answer, not by adding new content.

Use `references/language_quality_contract.md` as the source of truth for prose quality. Use `scripts/example_essay_language_linter.py` or an equivalent check before treating the language gap as closed.

DOCX formatting for essay-style Word output must follow the workspace rule: Arial, 2.5 cm margins, body text justified, subheadings left-aligned, main titles centered, 1.5 line spacing, and all other settings left at default unless the user specifies otherwise.

### 10. Extra Reading

Use extra reading only when it directly improves the answer to the exact question.

If recommended books are supplied, match the relevant chapter/section before use. If the relevant passage is not found, flag it and do not invent. If no reading is supplied, search academic sources and record what was verified.

Extra reading should normally contribute only a small enrichment layer. It must not replace lecture logic or introduce unrelated mechanisms.

### 11. Excel Generation

Default student-facing output is a single-sheet visual workbook named `Exam_Prep_Map`.

Use a minimal column set unless the user asks for audit detail:

- `Pages`;
- `Lecture / Module`;
- `Knowledge Point`;
- `Original PPT Page` or `Original Page Image`;
- `Essay-Style Synthesis`;
- `Exam-Facing Prep`.

Do not include raw OCR dumps, extracted slide text, evidence columns, page-function labels, weak-OCR messages, internal IDs, or coverage-audit sheets in the student-facing workbook unless explicitly requested.

Stack knowledge-point blocks vertically. Preserve source order and original slide/page images inside each block. Merge adjacent slides/pages only when they teach the same examinable mechanism, process, comparison, data operation, method, or scenario.

### 12. QA

Produce diagnostics for:

- unreadable files;
- weak OCR;
- unsupported files;
- ambiguous question type;
- missing slide evidence;
- answer not found in lectures;
- unverified citation;
- old-regime evidence excluded from prediction;
- low-confidence prediction;
- extra reading not found or not verified;
- benchmark/example content leaking into production content;
- generated prose failing language lint.

Predictions must be labelled conservatively. For essay/problem-essay exams, label the default output as `Predicted essay theme`, not as an official question or guaranteed stem. Optional practice stems may be included only as practice variants derived from the theme.

Before delivery, lint generated workbook prose and Example Essay prose where scripts exist. Rewrite or fail if the output contains slide-by-slide narration, page-tracing language, unsupported claims, how-to-write instructions inside answer prose, or repeated low-value filler.

### 13. Regression / Benchmark Use

Benchmarks validate generic behaviour only:

- evidence separation;
- regime splitting;
- question-type routing;
- KP granularity;
- lecture-order coverage;
- essay language quality;
- workbook layout adaptation;
- no cross-source factual leakage.

Any benchmark-specific content, name, lecturer, example, year, topic, or recurrence pattern is non-transferable unless the new target sources independently contain and verify it.

### 14. Gap Closure And Release

When modifying the Skill itself, completion requires:

- automatic example analysis has no unresolved high or medium language/workflow gaps;
- workbook and Example Essay language checks pass where scripts exist;
- DOCX Example Essays, when requested or fixture-tested, pass formatting and source audits;
- no production logic uses source-set identity, benchmark names, or course names as triggers;
- installed Skill copy and repository copy are synced;
- GitHub-ready QA passes before commit and push.

## Output Contract

Default user-facing output:

- normally includes the requested `Exam-Prep Excel` workbook when workbook generation is requested.

Explicit Example Essay Mode user-facing output:

- normally includes one standalone `Example Essay` `.docx` per essay when complete essays are requested.

Internal helper files such as diagnostics JSON, source maps, QA JSON, manifests, citation-resolution logs, rendered previews, and source-audit files may be generated for validation, but they must not be mixed into the final user-facing output unless the user explicitly asks for an audit package.

Do not edit, rename, delete, or overwrite source files.

When the user asks to keep only the latest output, remove older generated workbook versions, previews, temporary slide-image folders, and stale diagnostics from the requested report folder after verifying the latest workbook. Do not delete source files.
