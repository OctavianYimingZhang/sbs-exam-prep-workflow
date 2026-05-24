# User Interaction Protocol

This protocol turns a user request into explicit objects, output modes, coverage gates, and blocking-gap handling. It is not a source of factual course content.

## Interaction Objects

Use these objects for non-trivial runs:

- `UserExamPrepRequest`: raw request, requested mode, language, target group if known, focus areas, source policy, user-provided sources, and academic-integrity status.
- `UserConstraint`: time budget, preferred depth, requested artifacts, audit-package permission, and deadline if supplied.
- `SourceCoverageMap`: source classes required for the requested mode, available classes, missing blocking sources, freshness status, unreadable sources, and blocked conclusions.
- `GateResult`: pass/warn/block status for intake, source coverage, ontology validation, output view, and publish gates.
- `OutputView`: selected projection from the same object graph.

## Mode Selector

Classify the request into one mode before deep analysis:

| Mode | Use when | Main output |
| --- | --- | --- |
| `full_workflow` | User wants complete exam-prep workflow or does not specify a narrower mode. | Source coverage card plus Excel-first workbook and requested add-ons. |
| `source_inventory` | User asks only to inspect or classify files. | File roles, extraction status, trust level, and evidence permissions. |
| `exam_format_diagnosis` | User asks what the exam format rewards. | Sections, question types, answer rules, and recommended prep routes. |
| `prediction_workbook` | User asks for past-paper prediction or exam-prep Excel. | Archetype-based workbook with confidence bands and prep actions. |
| `mcq_prep` | User asks for MCQ preparation. | Discriminators, traps, contrast tables, and scoring policy when visible. |
| `short_answer_prep` | User asks for short-answer practice. | Bounded variants, mark schemas, concise answers, and reference expansions. |
| `practical_data_prep` | User asks for practical, data, graph, protocol, calculation, or case prep. | Input -> operation -> inference -> limitation -> follow-up drills. |
| `long_answer_plan` | User asks for project/scenario long-answer planning. | Method blocks, readouts, controls, caveats, and compact model answers when requested. |
| `essay_theme_plan` | User asks for essay preparation but not full essays. | Essay themes, coverage plans, paragraph skeletons, evidence banks. |
| `example_essay_docx` | User explicitly asks for complete Example Essays or model essay documents. | One DOCX per essay plus source audit. |
| `evidence_gap_audit` | User asks what is missing or why output is blocked. | Source coverage map, blocking gaps, stale evidence, and next-source checklist. |
| `incremental_refresh` | User supplies new slides, papers, readings, answers, or feedback after a prior run. | Only affected objects, sections, artifacts, and QA results are refreshed. |

If the user provides only materials and asks for exam prep, default to `full_workflow`. If the user asks for a specific artifact, choose the narrowest mode that can produce it validly.

## Clarification Rules

Ask at most one clarification question at a time.

Ask only when the missing input blocks a requested conclusion and cannot be safely inferred from the source set. Otherwise proceed and mark the issue as a `DataGap` or `QAFlag`.

Blocking examples:

- target source set is ambiguous and the files cannot be grouped safely;
- Example Essay mode is requested but no essay question, prompt, or answer scope exists;
- source files are unreadable and the requested artifact depends on their hidden content;
- exact citation, answer key, mark scheme, or official answer is requested but the relevant source is absent;
- live-exam or active-assessment risk cannot be ruled out.

Non-blocking examples:

- student time budget is missing: omit personalized priority terms and use evidence-only ranking;
- extra reading is missing: perform academic search if the mode needs it and record what was verified;
- old-format papers are present: use them for coverage only and label current prediction confidence conservatively;
- no answer key exists: produce lecture-supported answer logic and do not claim official answers.

## Source Coverage Card

Before generating a major workbook, Example Essay package, or prediction artifact, create a concise source coverage card internally and show it when useful:

```text
Mode:
Target source set:
Lecture slides / official notes:
Formal past papers:
Answer keys / mark schemes:
Practical or data materials:
Extra reading / recommended books:
Unreadable or weakly extracted sources:
Blocking gaps:
Blocked conclusions:
```

Keep the card short. Its purpose is to expose blocked conclusions before generation, not to become a second audit report.

## Best Source Pack

For the strongest exam-prep run, request or search for these source classes as applicable:

1. lecture slides and official notes;
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
- `prediction_brief`;
- `mcq_drill`;
- `short_answer_bank`;
- `practical_data_drill`;
- `essay_theme_plan`;
- `long_answer_method_blocks`;
- `example_essay_docx`;
- `evidence_gap_audit`;
- `incremental_refresh`.

Do not generate full workbooks, DOCX essays, audit packages, or helper files unless the selected mode or user request requires them.

## Follow-Up Options

When interactive guidance is useful, end the student-facing result with short follow-up options that reuse the same object graph:

- refresh from newly uploaded papers or slides;
- convert prediction results into a focused MCQ, short-answer, essay, or practical drill;
- generate Example Essay DOCX from a chosen theme;
- audit source gaps only;
- rerun QA after adding missing answer keys, readings, or mark schemes.

Do not add follow-up options when the user requested only a file, strict output, or no extra text.
