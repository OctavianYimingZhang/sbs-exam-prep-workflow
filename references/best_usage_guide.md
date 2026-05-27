# Best Usage Guide

This guide describes the source pack and run mode that give the Skill the strongest evidence base.

## Best Source Pack

For the strongest result, provide:

- lecture slides or official notes;
- formal past papers from the relevant exam regime;
- answer keys, mark schemes, or official guidance when available;
- practical, data, graph, protocol, case, or calculation materials when those question types are possible;
- essay or long-answer prompts if complete essay or long-answer output is requested;
- extra reading recommendations, books, papers, DOI records, PubMed records, publisher pages, or textbook chapters;
- any user weak areas, time budget, and preferred output depth.

Missing sources do not automatically stop the run. They stop only the conclusions that require them.

## Choosing The Correct Preset

Start from the requested artifact and choose the minimum valid route. The authoritative mode and preset table is in `references/user_interaction_protocol.md`; this guide only explains how to prepare the strongest source pack and how to run planning helpers.

## Strategy Rules

The exam strategy controls the output strategy:

- lecture-review default: lecture-first Word walkthrough with conceptual modules;
- essay or problem-essay: module-level Example Essays, adaptation maps, paragraph banks, and source-boundary checks;
- MCQ: student-facing Point Cards only by default, with traps folded into the card rather than exposed as separate audit tables;
- short answer: module logic, highlighted keywords, and natural Example Answers rather than visible mark-schema tables;
- data/problem/practical/scenario/project long answer: question analysis, answer order, reusable method/readout/interpretation/control/limitation blocks, Example Answer, and adaptation rules;
- mixed format: one walkthrough foundation may be used, but each add-on report keeps its own question-type route.

## Evidence Rules

Use lecture and official notes for factual course logic. Use formal papers for exam structure and archetypes. Use practical and answer materials for operations and answer style. Use external readings only after verification. Use examples and feedback as transferable style or workflow evidence unless the same factual claim is independently verified from target sources.

## Planning Commands

Create a plan:

```bash
python scripts/plan_workflow.py --config path/to/skill_config.json --output internal_qa/workflow_plan.json
```

Check readiness:

```bash
python scripts/input_readiness_check.py --config path/to/skill_config.json --output internal_qa/input_readiness.json
```

Render a plan preview:

```bash
python scripts/render_workflow_plan.py --plan internal_qa/workflow_plan.json --output internal_qa/workflow_plan.md
```

Use these helpers to make the run auditable. Do not publish helper JSON, rendered previews, manifests, lineage files, or source maps into the student-facing output unless an audit package was requested.
