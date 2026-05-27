---
name: everything-exam-preparation
description: Word-first exam-preparation workflow for lecture slides, past papers, practical materials, MCQ, short-answer, long-answer, project/scenario prompts, essay prompts, extra reading recommendations, recommended books, exemplars, marking guidance, and DOCX add-on reports.
---

# Everything Exam Preparation

Use this Skill to turn a student's supplied exam materials into evidence-grounded, Word-first revision artifacts. The Skill is a router plus protocol bundle: keep `SKILL.md` focused on trigger selection, evidence boundaries, output boundaries, and reference navigation; load detailed protocols only when the selected route needs them.

The first-principles chain is:

```text
inputs -> exam format -> question type -> examiner operation -> knowledge point -> preparation output
```

## Purpose And Trigger Boundary

Trigger this Skill for:

- lecture slides, official notes, past papers, practical/data/problem materials, answer keys, rubrics, mocks, quizzes, exemplars, feedback, extra reading, recommended books, or academic papers used for exam preparation;
- general lecture review, exam-format diagnosis, MCQ prep, short-answer prep, long-answer/project/scenario prep, practical/data prep, essay prep, complete Example Essays, or audit-only checks;
- requests to update, validate, or release this Skill package.

Default behaviour:

- If the user provides materials and asks to revise, go through lectures, or prepare generally without naming a narrower artifact, select `knowledge_walkthrough_docx`.
- If the user asks for MCQ, Short Answer, Long Answer/Project/Scenario, Practical/Data, or Essay preparation, generate the lecture walkthrough as the foundation unless the user explicitly opts out, then add the matching DOCX report.
- If the user asks only for past-paper analysis, exam format, or likely emphasis before generation, produce a chat-only `exam_analysis_brief`; do not create a public prediction file.
- For essay/problem-essay prediction language, use `Predicted essay theme` as the default label, not predicted question wording.
- If the user asks only for inventory, linting, QA, or release checks, run the narrow audit route and do not generate study artifacts.

Hard boundaries:

- Do not support live exams, active assessed submissions, or contract-cheating requests.
- Do not use hard-coded course, lecture, source-pack, benchmark, or example names as production triggers.
- Do not claim exact future exam questions, official answers, mark schemes, citations, statistics, mechanisms, dates, source names, or lecturer preferences unless verified from reliable evidence.
- Do not generate Excel workbooks, prediction workbooks, confidence-band files, archetype-registry files, or helper JSON as ordinary student-facing outputs.
- Do not edit, rename, delete, or overwrite source files.

## Routing Decision Tree

For non-trivial runs, create or conceptually maintain:

```text
UserExamPrepRequest -> SkillConfig -> WorkflowPlan -> InputReadinessReport -> OutputView
```

Use `references/user_interaction_protocol.md` as the source of truth for mode selection. Use `references/interactive_setup_protocol.md` for setup objects and readiness gates. Choose the narrowest valid route:

| User signal | Route | Student-facing output |
| --- | --- | --- |
| general lecture review, revise the material, go through the lectures | `knowledge_walkthrough_docx` | `Lecture_Knowledge_Walkthrough.docx` |
| inspect/classify/extract supplied files only | `source_inventory_only` | source coverage or inventory response |
| exam format, past-paper pattern, what the exam rewards | `exam_format_diagnosis` / `exam_analysis_brief` | chat-only brief unless a report is explicitly requested |
| MCQ, single-best-answer, option traps | `mcq_exam_prep` | walkthrough plus `MCQ_Exam_Analysis_Report.docx` |
| short answer, fill-blank, concise answer practice | `short_answer_exam_prep` | walkthrough plus `ShortAnswer_Exam_Analysis_Report.docx` |
| long answer, project, scenario, practical, data, graph, protocol, calculation, case | `long_answer_project_scenario_prep` | walkthrough plus `LongAnswer_Project_Scenario_Report.docx` |
| essay prep, model essay, complete Example Essay, full essay-style answer | `essay_exam_prep` | walkthrough plus `Essay_Module_Example_Essays.docx` |
| gap audit, output lint, repository QA, release check | `audit_lint_only` or `github_ready_qa` | QA result only |

Routing rules:

- Run only the requested route and its minimum dependencies.
- Do not apply essay-only scoring or Example Essay logic to MCQ, short-answer, data/problem, practical, project, or scenario routes.
- Before major DOCX generation, Example Essay generation, or prediction-heavy analysis, prepare a concise `SourceCoverageMap` and `WorkflowPlan` preview when blockers or skipped modules matter.
- Ask at most one clarification question at a time, and only when missing input blocks the requested conclusion and cannot be inferred from available sources.
- If a source class is missing but the requested output can still be supported, continue with conservative claims and record the limitation.

## Evidence And Output Boundaries

Evidence hierarchy:

- Lecture slides and official notes are the primary factual source for course content.
- Formal past papers define exam format, answer rules, question families, and current pattern evidence.
- Practical materials, mocks, quizzes, answer keys, rubrics, and exemplars support operations, answer style, and practice planning only within their evidence limits.
- Extra Reading recommendations, recommended books, lecture-cited originals, classic studies, and academic search results may enrich claims only after the relevant chapter, section, paper, DOI, PubMed record, publisher page, or textbook source is verified.
- Student annotations, images, external examples, and benchmark fixtures may shape style, density, or workflow rules only; they are not factual authority for a new source set unless independently verified.

Use the operational ontology in `ontology/ontology.json` and `references/operational_ontology_protocol.md` when multiple source roles, past-paper prediction, Example Essay source audits, or public artifacts require support-link validation.

Student-facing output filter:

- Public prose must be directly usable revision content, not an audit trace.
- Do not expose source anchors, confidence bands, recurrence counts, lecture centrality, examiner-operation labels, task verbs, discriminator axes, reference expansion, evidence limits, internal priority scores, source maps, QA JSON, run manifests, lineage files, citation logs, or rendered previews unless the user explicitly asks for an audit package.
- Visible priority labels are only `必备`, `重点`, and `补充`.
- Internal helper artifacts may be generated for validation, but they must stay outside ordinary student-facing output folders.

Public output contract:

- `Lecture_Knowledge_Walkthrough.docx`
- `MCQ_Exam_Analysis_Report.docx`
- `ShortAnswer_Exam_Analysis_Report.docx`
- `LongAnswer_Project_Scenario_Report.docx`
- `Essay_Module_Example_Essays.docx`

Example Essay hard gates:

- Trigger complete Example Essay mode only when the user asks for essay preparation, model essays, full essay-style answers, or complete essay documents.
- Follow `references/essay_generation_protocol.md` and `references/example_essay_docx_output_protocol.md`.
- Use lecture/PPT/source logic as the skeleton; Extra Reading is a precision layer, not a replacement.
- Add molecular, cellular, channel, receptor, pathway, assay, circuit, gene, method, or case detail only when it sharpens a parent source mechanism slot and preserves claim level, scope, and exam function.
- Run citation/Extra Reading integration before final compression; estimate a safe compression budget and preserve protected source skeleton, evidence, named academic details, and analytic limitations.
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
- `references/knowledge_walkthrough_docx_protocol.md`: lecture-first walkthrough route and DOCX structure.
- `references/question_type_protocol.md`: MCQ, short-answer, essay, and long-answer routing.
- `references/kp_essay_synthesis_protocol.md`: knowledge-point synthesis.
- `references/long_answer_example_protocol.md`: project/scenario long-answer model-answer logic.
- `references/practical_data_problem_protocol.md`: practical, data, problem, numerical, spotter, and answer-key workflows.

Example Essays and prose:

- `references/essay_generation_protocol.md`: Example Essay planning, source logic, Extra Reading integration, compression budget, and examiner-fit checks.
- `references/example_essay_docx_output_protocol.md`: DOCX-first Example Essay formatting, highlighting, source mapping, and source audit.
- `references/language_quality_contract.md`: shared prose-quality rules for KP synthesis, Example Essays, and long-answer prose.
- `references/essay_synthesis_protocol.md`: essay-style lecture knowledge synthesis.

Examples, regression, and release:

- `references/example_analysis_protocol.md`: convert examples and reviews into transferable rules without factual leakage.
- `references/cross_subject_regression_protocol.md`: benchmark rules that validate generic behaviour without production triggers.
- `references/gap_closure_loop_protocol.md`: iterative example-analysis, update, lint, and gap-closure completion condition.
- `references/subagent_protocol.md`: optional modular/subagent responsibilities and validation discipline.
- `references/github_release_protocol.md`: local QA, installed Skill sync, commit, and push requirements.

Use helper scripts when available for deterministic planning, extraction, validation, linting, DOCX generation, source audit, render QA, gap reporting, and release checks. Scripts are implementation aids; production behaviour must be controlled by source evidence and route selection, not by benchmark names.

## QA And Release Gate

Before delivery, fail or rewrite outputs that contain:

- unsupported factual claims, invented citations, fake precision, or unverified official answers;
- slide/page/source-route narration inside answer prose;
- how-to-write instructions inside the answer body;
- public exposure of internal source anchors, confidence, task verbs, discriminator axes, source maps, QA JSON, manifests, or lineage files;
- Example Essay content that replaces lecture logic with Extra Reading, overstates citation strength, leaks process language, or loses protected source skeleton during compression;
- benchmark/example factual leakage into production content.

Targeted checks:

```bash
python3 scripts/no_identity_trigger_linter.py --forbid-legacy-label
python3 scripts/validate_workflow_planning_contract.py
python3 scripts/validate_interaction_contract.py
python3 scripts/validate_student_output_contract.py
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
