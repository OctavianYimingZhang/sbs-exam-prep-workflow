# Modular Entry Points Protocol

This Skill must support both complete end-to-end execution and independent module execution. A user may ask for one module only, several modules chained together, or the full workflow.

## Hard Rule

Do only the requested scope unless the next module is required to make the requested output valid.

Examples:

- If the user asks only for source inventory, do not generate predictions or workbooks.
- If the user asks only for DOCX linting, do not rewrite essays.
- If the user asks only for Example Essay DOCX generation and already supplies a valid document plan, do not rerun past-paper prediction.
- If the user asks for the complete default lecture-review workflow, route to `knowledge_walkthrough_docx` and run only its dependencies.

## Module Contract

Every module must define:

- trigger;
- minimum inputs;
- outputs;
- dependencies;
- standalone-use behaviour;
- composition behaviour when used inside the full workflow.

Modules must write their results in a reusable format when practical: JSON, workbook, DOCX, or a concise direct answer. Diagnostics should state which modules were run and which were intentionally skipped.

## Independent Modules

### 1. Source Inventory

Trigger:

- user asks to inventory, classify, extract, inspect, OCR, or list supplied files.

Minimum inputs:

- source files or a folder path.

Outputs:

- source inventory JSON/table;
- file roles;
- target group keys;
- extraction status;
- trust/evidence-use classification;
- QA flags for unreadable or unsupported files.

Standalone behaviour:

- stop after inventory unless the user requests analysis.

### 2. Automatic Example Analysis

Trigger:

- user supplies examples, answer keys, feedback, screenshots, existing analysis files, benchmark outputs, or asks to improve Skill logic from examples.

Minimum inputs:

- source inventory or example folder path.

Outputs:

- example category counts;
- `ExampleContribution` records;
- `LanguageDelta` records;
- non-transferable content notes;
- protocol/script gap list.

Standalone behaviour:

- do not use example factual content for target predictions.

### 3. Target Grouping / Regime Split

Trigger:

- user asks to group papers, detect regimes, compare years, or separate old/current formats.

Minimum inputs:

- source inventory or formal paper files.

Outputs:

- target-group-key grouping;
- exam-regime split;
- evidence-use labels for each regime;
- conflicts or missing years.

Standalone behaviour:

- do not generate predictions unless requested.

### 4. Question-Type Gate / Exam-Format Diagnosis

Trigger:

- user asks what type of exam it is, how questions are structured, or what preparation product fits.

Minimum inputs:

- formal papers, guidance, or source inventory.

Outputs:

- question family classification;
- section/mark/time/answer-rule summary;
- output-mode recommendation.

Standalone behaviour:

- return diagnosis and recommended next modules.

### 5. Lecture Segmentation

Trigger:

- user asks to split lectures/modules, identify lecture order, or map slides.

Minimum inputs:

- lecture slides/notes.

Outputs:

- lecture/module map;
- slide ranges;
- lecturer/module markers where available;
- title/agenda/recommended-reading exclusion candidates.

Standalone behaviour:

- do not infer exam predictions unless requested.

### 6. Knowledge-Point Optimisation

Trigger:

- user asks to create, merge, refine, or audit knowledge points.

Minimum inputs:

- lecture segmentation and source text/images.

Outputs:

- KP records;
- source anchors;
- merged slide/page ranges;
- prerequisite/linked KPs;
- examinability and likely question types.

Standalone behaviour:

- do not generate workbook unless requested.

### 7. KP Essay Synthesis

Trigger:

- user asks to rewrite KP explanations, remove page-by-page narration, make essay-style synthesis, or lint workbook language.

Minimum inputs:

- KP records or workbook explanation cells plus source anchors.

Outputs:

- concept-first synthesis paragraphs;
- essay-style linter report;
- rewrite diagnostics.

Standalone behaviour:

- only rewrite/lint the requested KP explanations.

### 8. Archetype / Past-Paper / Pattern Analysis

Trigger:

- user asks for predictions, examiner patterns, recurrence, archetypes, or past-paper mapping.

Minimum inputs:

- formal papers and KP map.

Outputs:

- question archetypes;
- past-paper mapping;
- hotness/retention/recency separated from confidence;
- pattern evidence and contradictions.

Standalone behaviour:

- do not generate workbook unless requested.

### 9. Question-Type Output Generation

Trigger:

- user asks for MCQ traps, short-answer schemas, essay prompts, data/problem prompts, or long-answer plans.

Minimum inputs:

- exam-format diagnosis and KPs.

Outputs:

- MCQ Point Cards with explanation, exam-use pattern, traps, and must-remember rules;
- short-answer module logic and point cards with highlighted keywords and example answers;
- predicted essay themes by lecture scope, with optional practice variants;
- data/problem operations;
- long-answer project method/readout/control plans.

Standalone behaviour:

- output only the requested question-type product.

### 10. Knowledge Walkthrough DOCX Generation

Trigger:

- user asks to go through lecture knowledge, revise lecture content in order, or requests the default full workflow without a narrower artifact.

Minimum inputs:

- lecture slides or official notes.

Outputs:

- one student-facing Word walkthrough;
- internal manifest or QA JSON outside the public output folder unless an audit package is requested.

Standalone behaviour:

- if supplied with a valid `KnowledgeWalkthroughPlan`, generate/lint the DOCX without rerunning upstream modules.
- preserve lecture order while splitting each lecture by conceptual function rather than slide/page number.

### 11. Explicit Excel Workbook Generation

Trigger:

- user asks for revision Excel, exam-prep workbook, visual workbook, or spreadsheet output.

Minimum inputs:

- KP map, slide images, KP synthesis, and exam-facing prep outputs.

Outputs:

- student-facing Excel workbook;
- diagnostics JSON;
- optional separate evidence workbook.

Standalone behaviour:

- if supplied with valid intermediate JSON/KP records, build the workbook without rerunning upstream modules.

### 12. Example Essay DOCX Mode

Trigger:

- user explicitly asks for complete Example Essays, model essays, full essay-style answers, or essay Word documents.

Minimum inputs:

- essay question(s);
- relevant lecture slides or lecture-source inventory;
- optional slide-cited original sources;
- optional Extra Reading Books.

Outputs:

- one standalone DOCX per essay;
- internal manifest JSON, source audit JSON, source maps, and QA JSON for validation;
- optional ZIP only if requested or needed as the final delivery format.

User-facing output should include the requested final artefacts. Keep internal validation files out of the public output folder unless the user explicitly requests an audit package.

Standalone behaviour:

- if a valid `ExampleEssayDocumentPlan` is supplied, generate/lint DOCX files without rerunning prediction.
- if no lecture slides are supplied or identifiable, do not draft a polished essay; request the missing lecture evidence or flag the blocker.

### 13. Citation Resolver

Trigger:

- user asks to detect/resolve citations from lecture slides or prepare green-highlight source material.

Minimum inputs:

- relevant slide text/images;
- optional uploaded source PDFs/books.

Outputs:

- citation candidates JSON;
- resolution log;
- read-status notes.

Standalone behaviour:

- do not insert citation-derived essay content unless the source is resolved and read.

### 14. Extra Reading Matcher

Trigger:

- user asks to integrate Extra Reading Books or locate relevant chapters.

Minimum inputs:

- essay question or KP terms;
- uploaded book/chapter files.

Outputs:

- chapter/section match log;
- selected anchors;
- insert plan;
- QA flag if no relevant chapter is found.

Standalone behaviour:

- stop after matching unless the user asks to write or update an essay.

### 15. QA / Linting

Trigger:

- user asks to check, validate, lint, audit, or verify an output.

Minimum inputs:

- workbook, DOCX directory, source maps, diagnostics, or generated artefacts.

Outputs:

- lint reports;
- pass/fail status;
- offending rows/runs/paragraphs;
- QA flags.

Standalone behaviour:

- do not rewrite files unless explicitly requested.

### 16. Cross-Subject Regression

Trigger:

- user asks to run regression, validate benchmark behaviour, or check Skill quality across outputs.

Minimum inputs:

- regression suite and optionally generated workbooks/DOCX folders.

Outputs:

- regression report JSON;
- workbook/DOCX lint results where supplied.

Standalone behaviour:

- do not make content predictions.

### 17. Gap Closure Report

Trigger:

- user asks to keep improving until no major gaps remain, or asks for final Skill readiness.

Minimum inputs:

- lint reports, regression results, source-audit reports, external review notes, or generated outputs.

Outputs:

- high/medium/low gap report;
- pass/fail completion decision;
- required follow-up edits.

Standalone behaviour:

- do not claim completion while high or medium gaps remain unresolved.

### 18. GitHub Ready QA

Trigger:

- user asks to push, publish, release, or update GitHub.

Minimum inputs:

- repository checkout.

Outputs:

- GitHub-ready QA report;
- identity-trigger scan;
- public safety scan;
- synced installed-Skill check.

Standalone behaviour:

- do not commit or push if GitHub-ready QA fails.

## Full Workflow Composition

When the user requests the complete exam-prep workflow, run modules in this order:

1. Source Inventory.
2. Automatic Example Analysis when examples, answer keys, feedback, existing analyses, or external review notes are supplied.
3. Target Grouping / Regime Split.
4. Question-Type Gate / Exam-Format Diagnosis.
5. Lecture Segmentation.
6. Knowledge-Point Optimisation.
7. KP Essay Synthesis.
8. Archetype / Past-Paper / Pattern Analysis.
9. Question-Type Output Generation.
10. Knowledge Walkthrough DOCX Generation for the default lecture-review output.
11. Explicit Excel Workbook Generation only when requested.
12. QA / Linting.
13. Cross-Subject Regression when benchmark inputs or generated outputs are supplied.
14. Gap Closure Report when modifying the Skill itself.
15. GitHub Ready QA before commit or push.

If the user also explicitly requests complete Example Essays, run Example Essay DOCX Mode as a separate branch after lecture-source grounding and question selection:

1. Lecture Slide Scope Detection.
2. Lecture Slide Reading.
3. Lecture Logic Reconstruction.
4. Citation Resolver.
5. Extra Reading Matcher when books are supplied.
6. Essay Plan.
7. DOCX Generation.
8. DOCX Format Linting.
9. Render/Structural QA.
10. Source Audit.
11. Complete Example Essay Language Linting.

## Reuse Of Intermediate Outputs

If the user supplies a valid intermediate artefact, prefer using it directly:

- source inventory JSON can feed target grouping;
- lecture segmentation can feed KP optimisation;
- KP map can feed synthesis, predictions, or workbook generation;
- workbook can feed essay-style linter;
- ExampleEssayDocumentPlan can feed DOCX generation;
- DOCX + source map can feed DOCX format linter;
- source audit can feed regression;
- automatic example analysis can feed gap closure;
- gap reports can feed GitHub-ready QA.

Do not recompute upstream analysis unless the supplied artefact is missing, stale, incompatible, or the user asks for a full rerun.

## Reporting

Every run should state:

- modules run;
- modules skipped;
- input artefacts used;
- output artefacts generated;
- QA/lint status;
- blockers if a requested module cannot run.

Keep this report concise in the final user response.
