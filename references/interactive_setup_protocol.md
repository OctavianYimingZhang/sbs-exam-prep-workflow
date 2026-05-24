# Interactive Setup Protocol

Use this protocol before major generation when the user has not already supplied a complete, unambiguous run configuration.

The setup layer turns a natural-language request into a typed `SkillConfig`, then into a `WorkflowPlan`, then into an `InputReadinessReport`. Generation starts only after the selected preset has enough source support for its requested conclusions.

```text
User request -> SkillConfig -> WorkflowPlan -> InputReadinessReport -> validated output
```

## Setup Sections

The setup wizard has these sections:

| Section | Purpose |
| --- | --- |
| Project | Capture target label, code, exam year, and output folder. |
| Source Inputs | List lecture slides, official notes, papers, practical material, answers, feedback, and readings. |
| Output Mode | Choose exactly one main preset and whether an audit package is requested. |
| Evidence Policy | Decide whether academic search and extra-reading enrichment are allowed. |
| QA Gates | Choose strictness for ontology, lineage, language, and blocking-flag checks. |
| Plan Preview | Show actions, skipped modules, blockers, and publish gates. |
| Run Status | Track current, completed, and blocked actions. |
| Outputs | Separate student-facing outputs from internal QA outputs. |

## SkillConfig Rules

Create a `SkillConfig` object when the run has more than one source role, any prediction request, any Example Essay request, or any public artifact.

The required sections are:

- `project`;
- `source_inputs`;
- `source_policy`;
- `output_mode`;
- `qa`;
- `advanced`.

Use `schemas/skill_config.schema.json` as the shape contract. If a field is unknown, keep it unknown or empty; do not invent file paths, dates, source roles, or exam rules.

## Preset Selection

Use the narrowest preset that can answer the user's request:

| User need | Preset |
| --- | --- |
| File roles and evidence limits only | `source_inventory_only` |
| Exam sections, question types, and answer rules | `exam_format_diagnosis` |
| Default lecture knowledge review | `knowledge_walkthrough_docx` |
| Explicit Excel workbook | `full_excel_workbook` |
| Paper-derived preparation priorities | `past_paper_prediction` |
| MCQ strategy and content drills | `mcq_prep` |
| Short-answer variants and mark schemas | `short_answer_prep` |
| Practical, graph, data, case, protocol, or calculation prep | `practical_data_problem_prep` |
| Scenario or project-style long answer planning | `project_scenario_long_answer` |
| Essay themes and coverage plans, without complete essays | `essay_theme_plan` |
| Complete Example Essay Word documents | `example_essay_docx` |
| Checks only | `audit_lint_only` or `github_ready_qa` |

Do not run a full workbook path when a narrower audit, inventory, or format diagnosis is sufficient.

## Plan Preview

Before execution, create or conceptually present the `WorkflowPlan`:

- selected preset;
- source classes required by that preset;
- actions to run;
- modules skipped and why;
- blockers;
- publish gate.

Use `scripts/plan_workflow.py` when a config file is available. Use `scripts/render_workflow_plan.py` when a markdown preview is useful.

## Readiness Gate

Run or conceptually apply `InputReadinessReport` before generation:

- `can_run=true` means the preset has its minimum source classes;
- `can_run=false` means the missing input blocks the requested conclusion;
- warnings can be carried forward if they do not support hidden factual claims.

Ask at most one clarification question only when the missing input blocks the requested output. Otherwise continue with supported conclusions and record the limitation.

## Output Boundary

Student-facing outputs may include the requested workbook, Example Essay DOCX files, direct explanations, or concise reports. Internal QA artifacts may be generated under an internal folder, but they must not be mixed into the student-facing output unless the user explicitly asks for an audit package.
