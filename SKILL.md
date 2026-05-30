---
name: everything-exam-preparation
description: Word-first exam-preparation workflow for lecture slides, official notes, ordered course notes, past papers, practical materials, MCQ, short-answer, long-answer, project/scenario prompts, essay prompts, extra reading recommendations, recommended books, exemplars, marking guidance, Academic Exam-Ready Notes, optional visual aids, DOCX add-on reports, and explicit repository self-check/update maintenance.
---

# Everything Exam Preparation

Use this Skill to turn a student's supplied exam materials into evidence-grounded, Word-first revision artifacts. The Skill is a router plus protocol bundle: keep `SKILL.md` focused on trigger selection, evidence boundaries, output boundaries, and reference navigation; load detailed protocols only when the selected route needs them.

The first-principles chain is:

```text
inputs -> source authority -> course reconstruction -> atomic knowledge ledger -> source-first baseline notes -> coverage QA -> knowledge-only public view -> public output points -> exam overlay -> preparation output
```

## Purpose And Trigger Boundary

Trigger this Skill for:

- lecture slides, official notes, past papers, practical/data/problem materials, answer keys, rubrics, mocks, quizzes, exemplars, feedback, extra reading, recommended books, or academic papers used for exam preparation;
- general lecture review, exam-format diagnosis, MCQ prep, short-answer prep, long-answer/project/scenario prep, practical/data prep, essay prep, complete Example Essays, or audit-only checks;
- requests to doctor, self-check, update, validate, repair, refresh, or release this Skill package.

Default behaviour:

- If the user provides materials and asks to revise, make notes, go through the material, or prepare generally without naming a narrower artifact, select `exam_prep_notes_docx`. This route emits the compatible `Lecture_Knowledge_Walkthrough.docx` public artifact by building source-first baseline notes, running protected coverage QA, then applying an exam overlay.
- Keep `knowledge_walkthrough_docx` as a compatibility route when the user explicitly asks for a lecture-first walkthrough in source order; it must use the compact revision-note DOCX style, not the essay-submission style.
- If the user asks for MCQ, Short Answer, Long Answer/Project/Scenario, Practical/Data, or Essay preparation, generate the Academic Exam-Ready Notes foundation unless the user explicitly opts out, then add the matching DOCX report.
- If the user asks only for past-paper analysis, exam format, or likely emphasis before generation, produce a chat-only `exam_analysis_brief`; do not create a public prediction file.
- For essay/problem-essay prediction language, use `Predicted essay theme` as the default label, not predicted question wording.
- If the user asks only for inventory, linting, QA, or release checks, run the narrow audit route and do not generate study artifacts.
- When formal past papers are supplied with ordinary notes generation, route them through optional exam-regime, question-record, archetype, and examiner-operation planning actions. These actions may shape overlay emphasis and add-ons but must not become factual authority, exact future-question claims, or reasons to delete source-backed baseline modules.
- When style examples, feedback, or cross-target examples are supplied, run the example-learning chain: one review record per example, transferable-rule synthesis, rule-promotion gate, and example-transfer linting. Example content may teach generic structure, density, language, and QA only; it must not support target factual claims, prediction claims, or production branching on example identity.
- When sources contain diagrams, tables, figures, presentations, or image-only content, preserve visual-inspection metadata and warn internally before relying on visual content.

Hard boundaries:

- Do not use hard-coded course, lecture, source-pack, benchmark, or example names as production triggers.
- Do not claim exact future exam questions, official answers, mark schemes, citations, statistics, mechanisms, dates, source names, or lecturer preferences unless verified from reliable evidence.
- Do not generate Excel workbooks, prediction workbooks, confidence-band files, archetype-registry files, or helper JSON as ordinary student-facing outputs.
- Do not edit, rename, delete, or overwrite source files.
- Do not self-update the Skill package silently; package updates must be previewed, approved, backed up, and health-checked.

Quality target:

- For permitted revision-exemplar runs, complete Example Essay outputs should be written and formatted to the standard expected of submission-ready assessed work: polished argument, accurate synthesis, complete source grounding, examiner-fit structure, and clean DOCX presentation.

## Routing Decision Tree

For non-trivial runs, create or conceptually maintain:

```text
UserExamPrepRequest -> SkillConfig -> WorkflowPlan -> InputReadinessReport -> OutputView
```

Use `references/user_interaction_protocol.md` as the source of truth for mode selection. Use `references/interactive_setup_protocol.md` for setup objects and readiness gates. Choose the narrowest valid route:

| User signal | Route | Student-facing output |
| --- | --- | --- |
| general revision, make exam-prep notes, revise the material, go through the material | `exam_prep_notes_docx` | `Lecture_Knowledge_Walkthrough.docx` |
| explicitly lecture-first walkthrough in source order | `knowledge_walkthrough_docx` | `Lecture_Knowledge_Walkthrough.docx` |
| inspect/classify/extract supplied files only | `source_inventory_only` | source coverage or inventory response |
| exam format, past-paper pattern, what the exam rewards | `exam_format_diagnosis` / `exam_analysis_brief` | chat-only brief unless a report is explicitly requested |
| MCQ, single-best-answer, option traps | `mcq_exam_prep` | base notes plus `MCQ_Exam_Analysis_Report.docx` |
| short answer, fill-blank, concise answer practice | `short_answer_exam_prep` | base notes plus `ShortAnswer_Exam_Analysis_Report.docx` |
| long answer, project, scenario, practical, data, graph, protocol, calculation, case | `long_answer_project_scenario_prep` | base notes plus `LongAnswer_Project_Scenario_Report.docx` |
| essay prep, model essay, complete Example Essay, full essay-style answer | `essay_exam_prep` | base notes plus `Essay_Module_Example_Essays.docx` |
| gap audit, output lint, repository QA, release check | `audit_lint_only` or `github_ready_qa` | QA result only |

Routing rules:

- Run only the requested route and its minimum dependencies.
- Do not apply essay-only scoring or Example Essay logic to MCQ, short-answer, data/problem, practical, project, or scenario routes.
- Before major DOCX generation, Example Essay generation, or prediction-heavy analysis, prepare a concise `SourceCoverageMap` and `WorkflowPlan` preview when blockers or skipped modules matter.
- Ask at most one clarification question at a time, and only when missing input blocks the requested conclusion and cannot be inferred from available sources.
- If a source class is missing but the requested output can still be supported, continue with conservative claims and record the limitation.

## Evidence And Output Boundaries

Evidence hierarchy:

- Official lecture slides, official notes, official handouts, and lecturer-provided PDF/DOCX notes are the primary factual source for course content.
- Student typed notes, handwritten notes, annotated screenshots, flashcards, Notion-style notes, and unknown-provenance summaries may be used as intake cues only unless verified against official course material or reliable academic sources.
- AI-generated notes have no factual authority. Use them only as structure hints after independent verification.
- Formal past papers define exam format, answer rules, question families, and current pattern evidence.
- Practical materials, mocks, quizzes, answer keys, rubrics, and exemplars support operations, answer style, and practice planning only within their evidence limits.
- Extra Reading recommendations, recommended books, lecture-cited originals, classic studies, and academic search results may enrich claims only after the relevant chapter, section, paper, DOI, PubMed record, publisher page, or textbook source is verified.
- Student annotations, images, external examples, formatting references, and benchmark fixtures may shape style, density, layout, or workflow rules only; they are not factual authority for a new source set unless independently verified.

Use the operational ontology in `ontology/ontology.json` and `references/operational_ontology_protocol.md` when multiple source roles, past-paper prediction, Example Essay source audits, or public artifacts require support-link validation.

Student-facing output filter:

- Public prose must be directly usable revision content, not an audit trace.
- Ordinary Academic Exam-Ready Notes are knowledge documents, not exam-format audits. Do not expose assessment percentages, exam timing, mark splits, Section A/Section B administrative rules, historical-paper comparability notes, no-mark-scheme notes, coverage notes, source-quality caveats, ELM-check warnings, provenance text, or extraction-quality warnings in the public DOCX.
- Do not expose source anchors, confidence bands, recurrence counts, lecture centrality, examiner-operation labels, task verbs, discriminator axes, reference expansion, evidence limits, internal priority scores, source maps, QA JSON, run manifests, lineage files, citation logs, or rendered previews unless the user explicitly asks for an audit package.
- Visible priority labels are only `★★★`, `★★`, and `★`.
- Use `Course Knowledge Map` as the public top matter for ordinary notes. Do not use `Course-Level Exam Map` in public notes.
- Ordinary Academic Exam-Ready Notes render compact `PublicOutputPoint` blocks by lecture. Do not expose internal headings named `Exam Specificity`, `Core Exam Claim`, `Exam Use`, `Common Error / Trap`, or `Must Master`.
- Ordinary Academic Exam-Ready Notes must pass a public-point consistency gate: every visible KnowledgeCard maps to a public point, every public point references valid source cards, block-level atomic coverage is visible, and coverage bindings match the public point coverage.
- Ordinary notes and compatibility walkthroughs must pass a knowledge-only rendering gate: public output may contain source-backed definitions, mechanisms, criteria, calculations, graph/data rules, method workflows, examples, comparisons, limitations, and factual knowledge points only. Do not render generic answer advice, recommended approaches, integrated-reasoning sections, `How To Answer`, `How To Use`, `A strong answer should`, `Use this module`, or question-type reliability commentary unless the user explicitly requests a question-type add-on.
- When academic paper content is used as Extra Reading, a lecture-cited original, or a classic-source fallback, keep author names out of the sentence grammar. Write the claim as prose and place verified author-year attribution only in a parenthetical in-text citation, unless the user explicitly asks for literature-history narration or author attribution.
- Skill package files, fixtures, and protocol text are authored in English. This is a package-authoring convention, not a restriction on user-requested outputs.
- Select an `OutputLanguageProfile` only to honor an explicit user language request or to keep default English labels. Do not infer or force multilingual output from mixed-language sources; if the user wants multilingual output, they must request it.
- Select a route-specific DOCX style: `exam_prep_notes_docx` and `knowledge_walkthrough_docx` use Arial, 2.0 cm margins, compact line spacing, left-aligned body text, black text, and lecture page breaks. Example Essay DOCX formatting remains separate.
- Internal helper artifacts may be generated for validation, but they must stay outside ordinary student-facing output folders.

Public output contract:

- `Lecture_Knowledge_Walkthrough.docx`
- `MCQ_Exam_Analysis_Report.docx`
- `ShortAnswer_Exam_Analysis_Report.docx`
- `LongAnswer_Project_Scenario_Report.docx`
- `Essay_Module_Example_Essays.docx`

Example Essay hard gates:

- Trigger complete Example Essay mode only when the user asks for essay preparation, model essays, full essay-style answers, or complete essay documents.
- For complete essay planning or assessed-style drafting, follow `references/essay_tutor_workflow_protocol.md` before drafting: collect essay constraints, run DeepResearch, produce a subtitle-level plan, and use the plan-approval gate unless the user explicitly asks for direct generation.
- Follow `references/essay_generation_protocol.md` and `references/example_essay_docx_output_protocol.md`.
- Use lecture/PPT/source logic as the skeleton; Extra Reading is a precision layer, not a replacement.
- Do not pad Example Essays to increase Extra Reading, citation, or molecular-detail volume; add external detail only when it replaces vague wording or sharpens an existing lecture/source mechanism slot.
- Add molecular, cellular, channel, receptor, pathway, assay, circuit, gene, method, or case detail only when it sharpens a parent source mechanism slot and preserves claim level, scope, and exam function.
- Run citation/Extra Reading integration before final compression; estimate a safe compression budget and preserve protected source skeleton, evidence, named academic details, and analytic limitations.
- Example Essay DOCX output must use 0 pt paragraph spacing; the main title is centered, while the essay-question/topic subtitle is plain, left-aligned, not bold, not italic, and not enlarged.
- Final Example Essay DOCX output must not include public preambles, source-basis disclaimers, `Model answer built from...`, `This is not a predicted exam question`, `Exam-style question`, decorative `Question:` / `Essay Topic:` labels, or standalone `Example essay` labels.
- Distinguish Citation / Extra Reading Papers from Extra Reading Books: verified paper-derived content is green with parenthetical author-year citation; uploaded book/chapter content is yellow with chapter/section anchoring. Do not yellow-highlight papers.
- Run language lint, DOCX formatting lint, source audit, and render/structural QA where scripts exist.

## Reference Map

Load only the references required by the selected route.

Intake, routing, and setup:

- `references/user_interaction_protocol.md`: mode selector, output views, source coverage cards, plan previews, and blocking-gap rules.
- `references/interactive_setup_protocol.md`: `SkillConfig`, `WorkflowPlan`, `InputReadinessReport`, setup wizard, and readiness gate.
- `references/best_usage_guide.md`: best source pack, source-pack guidance, and helper planning commands.
- `references/modular_entrypoints_protocol.md`: standalone module behaviour and composition rules.

Evidence, ontology, and pattern analysis:

- `references/input_processing_protocol.md`: source roles, trust levels, evidence permissions, extraction, and format fields.
- `references/evidence_policy.md`: source hierarchy, citation verification, Extra Reading policy, and hard negatives.
- `references/operational_ontology_protocol.md`: object-link-action graph and ontology validation.
- `references/scoring_and_pattern_protocol.md`: pattern inference, retention, recency, confidence, and scoring discipline.
- `references/past_paper_prediction_protocol.md`: internal past-paper extraction, archetypes, scoring bands, and hard failures.

Student-facing outputs:

- `references/student_facing_output_policy.md`: visible output filters and final report contracts.
- `references/exam_prep_notes_protocol.md`: default Academic Exam-Ready Notes route, source-authority rules, exam-emphasis mapping, question-type add-ons, and definition policy.
- `references/knowledge_walkthrough_docx_protocol.md`: lecture-first walkthrough route and DOCX structure.
- `references/question_type_protocol.md`: MCQ, short-answer, essay, and long-answer routing.
- `references/kp_essay_synthesis_protocol.md`: knowledge-point synthesis.
- `references/long_answer_example_protocol.md`: project/scenario long-answer model-answer logic.
- `references/practical_data_problem_protocol.md`: practical, data, problem, numerical, spotter, and answer-key workflows.

Example Essays and prose:

- `references/essay_tutor_workflow_protocol.md`: essay-specific intake, DeepResearch, detailed plan schema, approval loop, subagent roles, citation modes, figure/table/data rules, and final essay QA.
- `references/essay_generation_protocol.md`: Example Essay planning, source logic, Extra Reading integration, compression budget, and examiner-fit checks.
- `references/example_essay_docx_output_protocol.md`: DOCX-first Example Essay formatting, highlighting, source mapping, and source audit.
- `references/language_quality_contract.md`: shared prose-quality rules for KP synthesis, Example Essays, and long-answer prose.
- `references/essay_synthesis_protocol.md`: essay-style lecture knowledge synthesis.
- `references/visual_aid_generation_protocol.md`: optional generated schematic planning, captions, source boundaries, and visual QA.

Examples, regression, and release:

- `references/example_analysis_protocol.md`: convert examples and reviews into transferable rules without factual leakage.
- `references/cross_subject_regression_protocol.md`: benchmark rules that validate generic behaviour without production triggers.
- `references/gap_closure_loop_protocol.md`: iterative example-analysis, update, lint, and gap-closure completion condition.
- `references/subagent_protocol.md`: optional modular/subagent responsibilities and validation discipline.
- `references/github_release_protocol.md`: local QA, installed Skill sync, commit, and push requirements.
- `skill_manifest.json`: package identity, repository metadata, health commands, and post-update commands.
- `scripts/skill_maintenance.py`: read-only doctor, explicit update preview, gated fast-forward update, backup, and health validation.

Use helper scripts when available for deterministic planning, extraction, validation, linting, DOCX generation, source audit, render QA, gap reporting, and release checks. Scripts are implementation aids; production behaviour must be controlled by source evidence and route selection, not by benchmark names.

## Maintenance And Safe Update

When the user asks to check, doctor, validate, update, repair, refresh, sync, or release this Skill package:

1. Run the read-only doctor first:

```bash
python3 scripts/skill_maintenance.py doctor
```

2. For update requests, preview before modifying files:

```bash
python3 scripts/skill_maintenance.py update --dry-run
```

3. Run the real update only after explicit user approval:

```bash
python3 scripts/skill_maintenance.py update --yes
```

Maintenance rules:

- Do not run update on a dirty git working tree.
- Do not update non-git installed copies in place; replace them only by preserving a backup and installing from the public repository.
- Do not modify private source materials, generated student outputs, helper artifacts, source maps, QA JSON, run manifests, lineage files, citation logs, rendered previews, or local audit folders.
- After a real update, run every health command in `skill_manifest.json`.
- If health validation fails, treat the update as failed and do not rely on the new Skill state.
- For proposed Skill improvements, produce a patch, issue, or PR-style proposal unless the user explicitly asks you to edit the package.

## QA And Release Gate

Before delivery, fail or rewrite outputs that contain:

- unsupported factual claims, invented citations, fake precision, or unverified official answers;
- slide/page/source-route narration inside answer prose;
- how-to-write instructions inside the answer body;
- public exposure of internal source anchors, confidence, task verbs, discriminator axes, source maps, QA JSON, manifests, or lineage files;
- Example Essay content that replaces lecture logic with Extra Reading, overstates citation strength, leaks process language, or loses protected source skeleton during compression;
- benchmark/example factual leakage into production content.
- promoted example-derived rules that lack good/bad analysis, non-transferable content, an anti-overfit rule, a destination, and a validation check.

Targeted checks:

```bash
python3 scripts/no_identity_trigger_linter.py --forbid-legacy-label
python3 scripts/validate_workflow_planning_contract.py
python3 scripts/validate_interaction_contract.py
python3 scripts/validate_student_output_contract.py
python3 scripts/example_transfer_linter.py tests/fixtures/example_learning/valid_example_review_ledger.json
python3 scripts/example_essay_language_linter.py --fixture benchmarks/example_essay_language_linter_fixtures.json
```

Full release gate:

```bash
python3 scripts/github_ready_check.py --ci
python3 scripts/github_ready_check.py --ci --require-clean
```

When modifying this Skill package:

- keep repository and installed Skill copy synced before release;
- do not commit private lectures, papers, books, student data, generated student outputs, helper artifacts, source maps, QA JSON, run manifests, lineage files, citation logs, rendered previews, or internal audit folders;
- run GitHub-ready QA before commit and push.
