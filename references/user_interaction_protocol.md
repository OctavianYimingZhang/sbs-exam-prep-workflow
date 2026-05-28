# User Interaction Protocol

This protocol turns a user request into explicit setup objects, output modes, coverage gates, plan previews, and blocking-gap handling. It is not a source of factual course content.

## Interaction Objects

Use these objects for non-trivial runs:

- `UserExamPrepRequest`: raw request, requested mode, language, target group if known, focus areas, source policy, user-provided sources, and academic-integrity status.
- `UserConstraint`: time budget, preferred depth, requested artifacts, audit-package permission, and deadline if supplied.
- `SkillConfig`: target, source inputs, source policy, output preset, QA strictness, and advanced reuse settings.
- `WorkflowPlan`: ordered actions, dependencies, expected outputs, skipped modules, blockers, and publish gate.
- `InputReadinessReport`: required source classes, available source classes, missing inputs, blockers, warnings, and can-run status.
- `SourceCoverageMap`: source classes required for the requested mode, available classes, missing blocking sources, freshness status, unreadable sources, and blocked conclusions.
- `GateResult`: pass/warn/block status for intake, source coverage, ontology validation, output view, and publish gates.
- `OutputView`: selected projection from the same object graph.

The setup chain is:

```text
User request -> SkillConfig -> WorkflowPlan -> InputReadinessReport -> OutputView
```

## Mode Selector

Classify the request into one mode before deep analysis. This table is the authoritative route selector for `SKILL.md`, `interactive_setup_protocol.md`, and `best_usage_guide.md`.

| Mode | Use when | Main output |
| --- | --- | --- |
| `full_workflow` | User wants default revision, exam-prep notes, or does not specify a narrower mode. | Source coverage card plus Academic Exam-Ready Notes in `Lecture_Knowledge_Walkthrough.docx`. |
| `source_inventory` | User asks only to inspect or classify files. | File roles, extraction status, trust level, and evidence permissions. |
| `exam_format_diagnosis` | User asks what the exam format rewards. | Sections, question types, answer rules, and recommended prep routes. |
| `exam_prep_notes_docx` | User asks for notes, revision, exam-prep notes, or to go through the material generally. | Exam-informed Academic Exam-Ready Notes in a Word document. |
| `knowledge_walkthrough_docx` | User explicitly asks to go through lecture knowledge in source order. | Lecture-first Word walkthrough with conceptual modules. |
| `exam_analysis_brief` | User asks for past-paper analysis before file generation. | Chat-only brief covering exam type, evidence limits, module/point selection, and recommended output route. |
| `mcq_exam_prep` | User asks for MCQ preparation. | Lecture walkthrough plus MCQ Point Card DOCX report. |
| `short_answer_exam_prep` | User asks for short-answer practice. | Lecture walkthrough plus module logic, point cards, highlighted keywords, and Example Answers. |
| `long_answer_project_scenario_prep` | User asks for practical, data, graph, protocol, calculation, case, project, scenario, or long-answer prep. | Lecture walkthrough plus question analysis, reusable mechanism/method/readout/interpretation/control/limitation blocks, Example Answer, and adaptation notes. |
| `essay_exam_prep` | User asks for essay preparation or complete Example Essays. | Lecture walkthrough plus module-level Example Essays, adaptation maps, and paragraph banks. |
| `essay_planning_only` | User asks for a plan, outline, thesis, essay structure, or pre-draft DeepResearch plan. | Chat-only detailed essay plan with subtitle-level body logic, citation strategy, visual/data strategy, assumptions, and blockers. |
| `evidence_gap_audit` | User asks what is missing or why output is blocked. | Source coverage map, blocking gaps, stale evidence, and next-source checklist. |
| `incremental_refresh` | User supplies new slides, papers, readings, answers, or feedback after a prior run. | Only affected objects, sections, artifacts, and QA results are refreshed. |

If the user provides only materials and asks for general lecture review, notes, or exam prep without naming a narrower artifact, default to `full_workflow`, which maps to `exam_prep_notes_docx`. If the user asks for a specific artifact, choose the narrowest mode that can produce it validly.

Map interaction modes to execution presets before planning:

| Interaction mode | Execution preset |
| --- | --- |
| `full_workflow` | `exam_prep_notes_docx` |
| `source_inventory` | `source_inventory_only` |
| `exam_format_diagnosis` | `exam_format_diagnosis` |
| `exam_prep_notes_docx` | `exam_prep_notes_docx` |
| `knowledge_walkthrough_docx` | `knowledge_walkthrough_docx` |
| `exam_analysis_brief` | `exam_format_diagnosis` |
| `mcq_exam_prep` | `mcq_exam_prep` |
| `short_answer_exam_prep` | `short_answer_exam_prep` |
| `long_answer_project_scenario_prep` | `long_answer_project_scenario_prep` |
| `essay_exam_prep` | `essay_exam_prep` |
| `essay_planning_only` | `essay_exam_prep` with draft generation disabled |
| `evidence_gap_audit` | `audit_lint_only` |
| `incremental_refresh` | narrowest affected preset |

## Clarification Rules

Ask at most one clarification question at a time.

Ask only when the missing input blocks a requested conclusion and cannot be safely inferred from the source set. Otherwise proceed and mark the issue as a `DataGap` or `QAFlag`.

Blocking examples:

- target source set is ambiguous and the files cannot be grouped safely;
- Example Essay mode is requested but no essay question, prompt, or answer scope exists;
- source files are unreadable and the requested artifact depends on their hidden content;
- exact citation, answer key, mark scheme, or official answer is requested but the relevant source is absent;
- live-exam or active-assessment risk cannot be ruled out.
- complete essay drafting is requested, but the user has not approved the detailed plan and did not request direct generation.

Non-blocking examples:

- student time budget is missing: omit personalized priority terms and use evidence-only ranking;
- extra reading is missing: perform academic search if the mode needs it and record what was verified;
- old-format papers are present: use them for coverage only and label current prediction confidence conservatively;
- no answer key exists: produce lecture-supported answer logic and do not claim official answers.
- citation style is missing during planning: mark it as pending and resolve before final draft or DOCX.

## Source Coverage Card

Before generating a major DOCX report, Example Essay package, or exam-analysis brief, create a concise source coverage card internally and show it when useful:

```text
Mode:
Target source set:
Lecture slides / official notes:
Readable course notes:
Formal past papers:
Answer keys / mark schemes:
Practical or data materials:
Extra reading / recommended books:
Unreadable or weakly extracted sources:
Blocking gaps:
Blocked conclusions:
```

Keep the card short. Its purpose is to expose blocked conclusions before generation, not to become a second audit report.

## Plan Preview

Create a `WorkflowPlan` before executing the selected preset. Show a short preview when the run is complex, blocked, prediction-heavy, or likely to create public artifacts:

```text
Selected preset:
Target:
Actions to run:
Modules skipped:
Blocking inputs:
Publish gate:
```

The plan preview is not a student-facing deliverable unless the user asks for an audit or setup report.

## Best Source Pack

For the strongest exam-prep run, request or search for these source classes as applicable:

1. lecture slides, official notes, lecturer-provided notes, and readable ordered course notes;
2. formal past papers and exam guidance;
3. mark schemes, answer keys, rubrics, or feedback where available;
4. practical protocols, data/problem sheets, workshops, mocks, quizzes, and exemplars;
5. essay prompts, long-answer prompts, or model-answer guidance;
6. extra reading recommendations, recommended books, chapters, papers, DOI/PubMed records, or publisher pages;
7. the student's target artifact preferences, weak areas, and time budget if personalization is requested.

The Skill should still proceed without a complete source pack when the requested output can be supported. It should block only conclusions that the available source set cannot verify.

## Output View Rules

Every view is a projection from the same evidence object graph. A focused view must not bypass evidence, ontology, citation, language, or deliverable QA.

Allowed focused views:

- `source_inventory`;
- `source_coverage_card`;
- `exam_prep_notes_docx`;
- `knowledge_walkthrough_docx`;
- `exam_analysis_brief`;
- `mcq_exam_prep`;
- `short_answer_exam_prep`;
- `long_answer_project_scenario_prep`;
- `essay_exam_prep`;
- `evidence_gap_audit`;
- `incremental_refresh`.

Do not generate Excel workbooks, prediction files, audit packages, or helper files as ordinary student-facing output. Generate DOCX essays or reports only when the selected mode or explicit user request requires them.

## Follow-Up Options

When interactive guidance is useful, end the student-facing result with short follow-up options that reuse the same object graph:

- refresh from newly uploaded papers or slides;
- convert the exam-analysis brief into a focused MCQ, short-answer, essay, long-answer, project/scenario, or practical/data report;
- generate Essay Module Example Essays from a supported essay scope;
- convert the same lecture modules into MCQ or short-answer reports;
- audit source gaps only;
- rerun QA after adding missing answer keys, readings, or mark schemes.

Do not add follow-up options when the user requested only a file, strict output, or no extra text.
