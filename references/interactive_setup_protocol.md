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
| Source Inputs | List lecture slides, official notes, ordered course notes, papers, practical material, answers, feedback, and readings. |
| Output Mode | Choose exactly one main preset and whether an audit package is requested. |
| Essay Constraints | For complete essay work, capture topic, exact question, word limit, format, citation style, rubric, source base, figure/table/data needs, and AI-use policy where available. |
| Evidence Policy | Decide whether academic search and extra-reading enrichment are allowed. |
| QA Gates | Choose strictness for ontology, lineage, language, and blocking-flag checks. |
| Plan Preview | Show actions, skipped modules, blockers, and publish gates. |
| Run Status | Track current, completed, and blocked actions. |
| Outputs | Separate student-facing outputs from internal QA outputs. |

## SkillConfig Rules

Create a `SkillConfig` object when the run has more than one source role, any past-paper/exam-format analysis request, any Example Essay request, or any public artifact.

The required sections are:

- `project`;
- `source_inputs`;
- `source_policy`;
- `output_mode`;
- `qa`;
- `advanced`.

Use `schemas/skill_config.schema.json` as the shape contract. If a field is unknown, keep it unknown or empty; do not invent file paths, dates, source roles, or exam rules.

## Preset Selection

Use the mode selector and mode-to-preset mapping in `references/user_interaction_protocol.md` as the source of truth. This setup protocol should only instantiate the selected preset into `SkillConfig`, `WorkflowPlan`, and `InputReadinessReport`.

Do not generate a DOCX report when a narrower audit, inventory, or format diagnosis is sufficient. Do not use legacy Excel workbook paths as public output routes.

## Plan Preview

Before execution, create or conceptually present the `WorkflowPlan`:

- selected preset;
- source classes required by that preset;
- actions to run;
- modules skipped and why;
- blockers;
- publish gate.

For complete essay planning or assessed-style drafting, add:

- detailed essay-plan version;
- approval status;
- candidate sources still requiring verification;
- figure/table/data gates if requested.

Do not generate the complete final essay before the plan is approved unless the user explicitly requests direct generation.

Use `scripts/plan_workflow.py` when a config file is available. Use `scripts/render_workflow_plan.py` when a markdown preview is useful.

## Readiness Gate

Run or conceptually apply `InputReadinessReport` before generation:

- `can_run=true` means the preset has its minimum source classes;
- `can_run=false` means the missing input blocks the requested conclusion;
- warnings can be carried forward if they do not support hidden factual claims.

Ask at most one clarification question only when the missing input blocks the requested output. Otherwise continue with supported conclusions and record the limitation.

## Output Boundary

Student-facing outputs may include Academic Exam-Ready Notes in `Lecture_Knowledge_Walkthrough.docx`, the explicit lecture-first walkthrough, question-type DOCX add-on reports, Example Essay DOCX content, direct explanations, or concise reports. Internal QA artifacts may be generated under an internal folder, but they must not be mixed into the student-facing output unless the user explicitly asks for an audit package.
