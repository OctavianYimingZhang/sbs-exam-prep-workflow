---
name: sbs-exam-prep-workflow
description: Word-first lecture knowledge walkthrough and evidence-grounded exam-preparation workflow for lecture slides, past papers, practical materials, MCQ, short-answer, long-answer, essay prompts, extra reading recommendations, recommended books, exemplars, marking guidance, explicit Excel workbooks, and optional DOCX-first Example Essays.
---

# SBS Exam Prep Workflow

Build an evidence-grounded exam-preparation system from the student's supplied materials. The workflow starts from first principles:

```text
Inputs -> exam format -> question type -> examiner operation -> knowledge point -> preparation output
```

The workflow is not topic-hotness-first. Frequency and recency are auxiliary signals. The core task is to infer how the examiner asks questions, what kind of answer each question type rewards, and what preparation artefact best matches that strategy.

Default lecture-review output is a Word-first `Lecture Knowledge Walkthrough DOCX`: it preserves lecture order, splits each lecture into conceptual modules, and explains the knowledge in student-facing language. Excel workbooks, MCQ reports, short-answer reports, long-answer playbooks, prediction workbooks, and complete Example Essays are generated only when explicitly requested or when selected by the plan. Complete Example Essays remain DOCX-first and one document per essay. Do not help with a live exam, active assessed submission, or contract-cheating request.

For non-trivial runs, use the setup and planning chain before generation:

```text
User request -> SkillConfig -> WorkflowPlan -> InputReadinessReport -> validated output
```

This chain is the control layer. It chooses the narrowest valid preset, lists required sources, records skipped modules, exposes blockers, and prevents internal helper files from being mixed into student-facing outputs.

## Student-Facing Output Filter

The Skill may use source anchors, evidence claims, confidence bands, examiner-operation labels, recurrence, lecture centrality, and scoring logic internally. Student-facing outputs must not expose internal audit reasoning unless the user explicitly requests an audit package.

For ordinary student-facing exam-prep outputs, rewrite each item as directly usable revision content:

```text
internal reasoning: evidence -> operation -> priority -> output type
student output: priority -> point/module -> explanation -> exam-use answer or walkthrough
```

Do not show `source_anchor`, evidence rationale, confidence, recurrence count, lecture centrality, examiner operation, discriminator axis, task verb, reference expansion, common omissions, evidence limit, past-paper year mapping, or prediction score in the public student report.

Visible priority labels are only `必备`, `重点`, and `补充`.

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

## Operational Ontology Boundary

Use the operational ontology contract in `ontology/ontology.json` and `references/operational_ontology_protocol.md` when source complexity is high, past-paper prediction is requested, or multiple source roles must be reconciled.

The runtime model is:

```text
SourceDocument -> SourceFragment -> KnowledgePoint -> ExaminerOperation -> QuestionArchetype -> EvidenceClaim -> PrepArtifact -> QAFlag
```

The ontology is not a topic taxonomy. It is an evidence-permission graph. Links must encode what each source is allowed to support:

- external examples may contribute workflow rules, not factual claims;
- old or structurally different regimes may support coverage, not current blueprint prediction;
- unreadable or weakly extracted sources may create QA flags, not hidden content;
- verified reading may enrich a knowledge point, not replace lecture logic;
- public artifacts must be generated only after QA-passed object and link checks.

Use a small internal control plane when a run has more than one source role, any past-paper prediction, any Example Essay source audit, or any generated public artifact. The control plane has four layers:

```text
Bronze: SourceDocument, raw extraction metadata, source hashes
Silver: SourceFragment, FragmentPartition, PastPaperQuestion, AssessmentRegime
Gold: KnowledgePoint, ExaminerOperation, QuestionArchetype, EvidenceClaim, QAFlag
Serving: student-facing workbook, Example Essay DOCX, direct answer, optional audit package
```

Student-visible output may be generated only from Gold objects whose support links pass ontology validation. Build `FragmentPartition` metadata before deep reasoning when it can prune irrelevant slides, papers, books, answer keys, or examples. Record run manifests and lineage events for reproducibility when helper scripts create artifacts.

## Mandatory References

- `references/input_processing_protocol.md`: source roles, trust levels, evidence use, extraction, and format fields.
- `references/operational_ontology_protocol.md`: object-link-action graph, evidence-permission links, actions, query discipline, and ontology validation.
- `references/user_interaction_protocol.md`: request parsing, mode selection, source coverage cards, output views, and blocking-gap interaction.
- `references/interactive_setup_protocol.md`: `SkillConfig`, `WorkflowPlan`, `InputReadinessReport`, plan preview, and setup wizard rules.
- `references/best_usage_guide.md`: best source pack, preset selection, strategy rules, and planning commands.
- `references/student_facing_output_policy.md`: visible output filters and final student report contracts for MCQ, short-answer, long-answer, and essay outputs.
- `references/knowledge_walkthrough_docx_protocol.md`: lecture-first Word walkthrough route, module extraction, DOCX structure, and forbidden student fields.
- `references/modular_entrypoints_protocol.md`: standalone and full-workflow entry points.
- `references/question_type_protocol.md`: MCQ, short-answer, essay, and long-answer routing.
- `references/scoring_and_pattern_protocol.md`: pattern inference, retention, recency, and confidence rules.
- `references/past_paper_prediction_protocol.md`: question-level past-paper extraction, archetype registry, scoring bands, type-specific prediction targets, and hard failures.
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

Use helper scripts where available for workflow planning, input-readiness checks, plan rendering, source extraction, fragment indexing, runtime ontology validation, action writer coverage validation, interaction-contract validation, run-manifest and lineage linting, example-corpus analysis, grouping, archetype schemas, workbook language linting, Example Essay language linting, DOCX generation, DOCX formatting linting, citation resolution, extra-reading chapter matching, source audit, render QA, identity-trigger linting, gap reporting, GitHub-ready QA, and regression checks. Helper scripts are implementation aids; production behaviour must be controlled by parsed evidence conditions, not by benchmark names.

When past-paper prediction is requested, generate or conceptually maintain question-level records before ranking. The required internal path is:

```text
past papers -> current exam regime -> PastPaperQuestion records -> QuestionArchetype registry -> slot grammar -> KP compatibility -> confidence band -> PrepArtifact
```

## Workflow

### 0. Route The Request

Parse the request into `UserExamPrepRequest`, `UserConstraint`, `SkillConfig`, `WorkflowPlan`, `InputReadinessReport`, and `OutputView` when the run is non-trivial. Decide whether the selected mode is:

- `full_workflow`;
- `source_inventory`;
- `exam_format_diagnosis`;
- `knowledge_walkthrough_docx`;
- `prediction_workbook`;
- `mcq_prep`;
- `short_answer_prep`;
- `practical_data_prep`;
- `long_answer_plan`;
- `essay_theme_plan`;
- `example_essay_docx`;
- `evidence_gap_audit`;
- `incremental_refresh`;
- audit/regression only.

If the user provides only materials and asks to go through the knowledge, revise the lectures, or prepare generally without naming a question-type artifact, default to `knowledge_walkthrough_docx`. If the user asks for a specific artifact, choose the narrowest mode that can produce it validly.

Run only the requested module and its minimum dependencies. If the user supplies valid intermediate artefacts, use them directly. Report modules run, modules skipped, and artefacts generated.

When a config file is available, create the plan with:

```bash
python scripts/plan_workflow.py --config path/to/skill_config.json --output internal_qa/workflow_plan.json
python scripts/input_readiness_check.py --config path/to/skill_config.json --output internal_qa/input_readiness.json
```

Show a concise Plan Preview before executing any major generation path when the source pack has blockers, when the user asks for a prediction, or when the run will create public artifacts.

Ask at most one clarification question at a time. Ask only when the missing input blocks a requested conclusion and cannot be safely inferred from the source set. Otherwise proceed and record a `QAFlag`, `GateResult`, or source-coverage blocker.

Before generating a major workbook, Example Essay package, or prediction artifact, create a concise `SourceCoverageMap`. Expose source coverage when useful so the user can see missing source classes, unreadable files, and blocked conclusions before generation.

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

After inventory, create or conceptually maintain `FragmentPartition` metadata when downstream work needs selective reading. Partition by source role, analysis context, target group, regime, year, question type, concept type, input format, extraction confidence, allowed evidence use, and source hash. Use this metadata to skip irrelevant sources before deep analysis.

For strongest results, prefer a source pack containing lecture slides/official notes, formal past papers, answer keys or mark schemes when available, practical or data materials, essay/long-answer prompts, extra reading recommendations or books, and any user-provided weak areas or time budget. If the source pack is incomplete, continue where support is sufficient and block only unsupported conclusions.

### 2. Split Exam Regimes

Compare papers only inside the same target course/module group. Split regimes when answer rules, timing, mark weights, section structure, permitted choices, dominant question type, or submission format changes.

Old or structurally different papers can support concept coverage and answer-schema practice. They must not control current blueprint prediction unless comparability is proven.

If formal papers are supplied, extract question-level records before scoring patterns. Each record should capture year, section, question number, marks, answer rule, question type, command verbs, input format, candidate options when visible, negative marking policy when visible, and extraction confidence. If a field is not visible, leave it unknown and flag review instead of inventing.

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
- MCQ-heavy regime: build discriminator axes, contrast tables, exception lists, mechanism-order traps, wrong-option diagnosis, and a scoring policy when negative marking or multiple-response marking is visible.
- Short-answer regime: build bounded family variants from archetype, slot grammar, source-linked knowledge points, and mark scale; do not generate unbounded question lists.
- Data/problem regime: build input -> operation -> inference -> limitation -> follow-up logic.
- Project/scenario long-answer regime: build reusable method blocks: method -> readout -> interpretation -> control -> caveat. Do not predict exact rotating scenarios when the stable signal is an operation.
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

- student-visible `MCQ Point Card` only by default;
- `Priority`, `Point`, `知识点讲解`, `考试怎么考`, `常见陷阱`, and `必须记住`;
- no practice question, answer key, contrast table, separate trap bank, discriminator axis, confidence, evidence, or source anchor unless the user explicitly asks for a separate practice/audit output;
- common wrong-option logic must be folded into `常见陷阱`.

Short answer:

- module-level logic before point cards;
- `Priority`, `Point`, `常见问法`, `考点讲解（关键词高亮）`, and `Example Answer`;
- no visible mark-producing schema, required-term field, optional-example field, reference expansion, common omissions, task verb, confidence, evidence, or source anchor;
- required keywords should be bolded inside the explanation, and scoring logic should be absorbed into the natural `Example Answer`.

Essay / problem-essay:

- predicted examinable themes, with lecture scope, examiner operation, and optional practice angles;
- essay coverage plans for answer-one-from-several-options sections, prioritising enough lecture blocks for at least one high-quality answer rather than equal-depth exhaustive coverage unless requested;
- paragraph plans;
- essay-style knowledge-point explanations;
- no complete essays unless explicitly requested.

Long answer / project / scenario:

- question deconstruction;
- exam-response playbook;
- reusable answer blocks for mechanism, method/readout, interpretation, control, and limitation;
- compact model answer only when explicitly requested.

Knowledge walkthrough:

- lecture-first DOCX;
- each lecture becomes a short overview, module map, conceptual module walkthroughs, and lecture recap;
- modules are inferred by conceptual function, not by PPT page order;
- no essay skeletons, full essays, practice questions, answer keys, prediction scores, or internal audit fields.

### 9. Example Essay Mode

Trigger only when the user explicitly asks for complete `Example Essay`, `model essay`, `full essay-style answer`, `write an essay`, or equivalent complete essay documents.

Run the internal sequence in `references/essay_generation_protocol.md` for complete Example Essay generation:

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
sentence-level extra-reading micro-detail pass
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

After the draft is coherent, run the sentence-level Extra Reading micro-detail pass before highlight planning. This pass does not rewrite the essay. It scans unhighlighted mechanism, evidence, and interpretation sentences for generic slots such as channel, transporter, receptor, kinase, phosphatase, transcription factor, morphogen, ligand, cofactor, chemical species, cellular compartment, assay readout, or pathway intermediate. Insert only a short verified named detail when it improves precision without changing the claim.

Micro-detail rules:

- use only verified recommended-book chapters/sections, lecture-cited original sources, or verified academic/classic sources;
- keep the insertion as a phrase or short clause; it must not become a new explanatory sentence, paragraph, or second argument;
- highlight only the inserted phrase, not the whole lecture-derived sentence;
- recommended-book detail is yellow, verified original-paper or classic-source detail is green, and lecture-only detail is not highlighted;
- reject any insertion that lacks a source anchor, needs a new explanatory sentence, duplicates nearby detail, becomes too expansive, shifts the answer away from the question, creates citation stacking, or replaces lecture logic with extra-reading logic;
- record original phrase, inserted phrase, source class, source anchor, highlight colour, word-count delta, claim delta, and QA status in the source map or audit.

DOCX formatting for essay-style Word output must follow the workspace rule: Arial, 2.5 cm margins, body text justified, subheadings left-aligned, main titles centered, 1.5 line spacing, and all other settings left at default unless the user specifies otherwise.

### 10. Extra Reading

Use extra reading only when it directly improves the answer to the exact question.

If recommended books are supplied, match the relevant chapter/section before use. If the relevant passage is not found, flag it and do not invent. If no reading is supplied, search academic sources and record what was verified.

Extra reading should normally contribute only a small enrichment layer. It must not replace lecture logic or introduce unrelated mechanisms.

For complete Example Essays, treat Extra Reading as a precision layer. Do not ask whether more external material can be added in general. Ask whether an unhighlighted mechanism sentence contains a generic slot that can be made more specific by one verified named object, reaction step, transport form, domain, ligand, readout, or pathway module. If not, leave the sentence unchanged.

### 11. Excel Generation

Excel output is an explicit workbook route, not the default lecture-review route. When requested, the student-facing workbook is a single-sheet visual workbook named `Exam_Prep_Map`.

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
- missing workflow plan or input-readiness gate for a major generation path;
- answer not found in lectures;
- unverified citation;
- old-regime evidence excluded from prediction;
- low-confidence prediction;
- missing runtime object or invalid ontology link;
- ontology object without writer action;
- interaction mode missing or unsupported by source coverage;
- workflow action missing required source input;
- student-facing output exposes internal evidence, confidence, source-anchor, discriminator, task-verb, or examiner-operation fields;
- knowledge walkthrough DOCX follows slide/page order instead of conceptual module order;
- student-facing artifact without valid Gold-object lineage;
- missing run manifest or lineage event for generated artifacts;
- exact future-question wording claimed;
- fake precise probability from a small paper set;
- MCQ official answer claimed without answer-key evidence;
- short-answer variant generated without source-linked KP or bounded slot grammar;
- lecturer style used as strong evidence without repeated current-regime support;
- extra reading not found or not verified;
- benchmark/example content leaking into production content;
- generated prose failing language lint.

Predictions must be labelled conservatively. For essay/problem-essay exams, label the default output as `Predicted essay theme`, not as an official question or guaranteed stem. Optional practice stems may be included only as practice variants derived from the theme.

Lecturer/source-block style is auxiliary. It cannot raise confidence above `Medium` unless supported by the same current exam regime across at least two formal papers, aligned with lecture objectives or summary material, and not contradicted by recent papers.

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
- no cross-source factual leakage;
- ontology contract integrity;
- past-paper prediction hard failures;
- runtime object-store validation;
- manifest and lineage reproducibility;
- action writer coverage;
- interaction contract coverage;

Any benchmark-specific content, name, lecturer, example, year, topic, or recurrence pattern is non-transferable unless the new target sources independently contain and verify it.

### 14. Gap Closure And Release

When modifying the Skill itself, completion requires:

- automatic example analysis has no unresolved high or medium language/workflow gaps;
- workbook and Example Essay language checks pass where scripts exist;
- DOCX Example Essays, when requested or fixture-tested, pass formatting and source audits;
- no production logic uses source-set identity, benchmark names, or course names as triggers;
- every ontology object is produced by a writer action or explicitly treated as parsed user/source input;
- interaction routing, source coverage, and output-view checks pass;
- setup, workflow planning, input-readiness, and plan-preview checks pass;
- runtime object-store, manifest, and lineage checks pass when control-plane artifacts are generated;
- installed Skill copy and repository copy are synced;
- GitHub-ready QA passes before commit and push.

## Output Contract

Default user-facing output:

- normally includes the requested `Lecture Knowledge Walkthrough DOCX` when the user asks to go through lecture knowledge or provides materials without naming a narrower output.
- includes the requested `Exam-Prep Excel` workbook only when workbook generation is requested.

Explicit Example Essay Mode user-facing output:

- normally includes one standalone `Example Essay` `.docx` per essay when complete essays are requested.

Internal helper files such as diagnostics JSON, source maps, QA JSON, manifests, citation-resolution logs, rendered previews, and source-audit files may be generated for validation, but they must not be mixed into the final user-facing output unless the user explicitly asks for an audit package.

Do not edit, rename, delete, or overwrite source files.

When the user asks to keep only the latest output, remove older generated workbook versions, previews, temporary slide-image folders, and stale diagnostics from the requested report folder after verifying the latest workbook. Do not delete source files.
