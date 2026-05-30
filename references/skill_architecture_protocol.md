# Skill Architecture And Improvement Traceability Protocol

This protocol controls how the Skill package is structured and how user-requested improvements become durable behaviour. It exists because this Skill has been improved across many example-driven conversations; each improvement must now land in a named layer, have a validation gate, and avoid becoming an example-specific production trigger.

```text
UserImprovementRequest
-> ImprovementIntent
-> SkillArchitectureLayer
-> DestinationFile
-> ValidationGate
-> SkillImprovementLedger
-> ReleaseGate
```

## Architecture Layers

The Skill package has seven public-maintained layers.

| Layer | Primary files | Responsibility | Must not do |
|---|---|---|---|
| Router | `SKILL.md`, `references/user_interaction_protocol.md` | detect trigger, choose route, state hard output boundaries | contain long route-specific manuals |
| Source/evidence | `references/input_processing_protocol.md`, `references/evidence_policy.md`, `schemas/analysis_context.schema.json` | classify sources, roles, regimes, trust, extraction quality | let examples or old-regime papers become factual authority |
| Knowledge graph | `ontology/ontology.json`, `references/operational_ontology_protocol.md`, atomic-ledger schemas | convert source fragments into supported knowledge objects | treat topic proximity as evidence support |
| Route protocols | exam-prep notes, walkthrough, question-type, essay, practical/data, long-answer protocols | define output-mode logic | borrow another route's generation style |
| Public surface | `references/knowledge_surface_protocol.md`, `schemas/knowledge_surface_contract.schema.json`, DOCX generators/linters | render only knowledge-bearing student-facing text | expose process, audit, source-route, AI-provenance or rigid template scaffolds |
| Scientific precision | `references/scientific_precision_protocol.md`, language and citation linters | protect entity categories, alias handling, evidence ladders, mechanism-per-detail logic | add named detail that only decorates the answer |
| Improvement governance | this protocol, `governance/skill_improvement_ledger.json`, architecture validator | verify that every improvement has a destination and gate | rely on conversation memory or untracked manual intent |

## AnalysisContext

Every non-trivial run should classify each source into an `AnalysisContext` before planning:

```yaml
AnalysisContext:
  target_unit_current_regime:
  target_unit_old_or_different_regime:
  target_unit_auxiliary:
  cross_unit_example:
  style_exemplar:
  layout_exemplar:
  benchmark_fixture:
  unsupported_or_unreadable:
```

Only `target_unit_current_regime` material can control current blueprint prediction. Target-unit lectures and official notes control factual course content. Old/different-regime material may support coverage or schema only unless comparability is established. Cross-unit examples and benchmark fixtures teach workflow, QA and layout only.

## UnitExampleContribution

Unit examples must be represented as `UnitExampleContribution`, not as production triggers.

```yaml
UnitExampleContribution:
  source_unit:
  source_materials:
  observed_unit_pattern:
  generic_skill_contribution:
  transferable_rule:
  future_unit_diagnostic_questions:
  non_transferable_content:
  affected_workflows:
  anti_patterns_prevented:
  validation_checks:
```

A contribution is valid only if a future run can apply it by checking source structure, question type, format, regime and output need. It is invalid if it requires recognising the original unit name or reusing the original unit's factual topics.

## ImprovementImplementationLedger

Every substantial user-requested improvement must be recorded in the improvement ledger with:

```yaml
ImprovementImplementationRecord:
  improvement_id:
  source_summary:
  user_purpose:
  architectural_layer:
  implemented_files:
  validation_gates:
  status:
  remaining_gaps:
  next_action:
```

Status values:

- `implemented`: destination files and validation gates exist.
- `implemented_with_gap`: core rule exists but one route, compact bundle, fixture or validator still needs work.
- `deferred`: intentionally not implemented; reason must be explicit.
- `replaced_by_later_rule`: superseded by a later user requirement.

No improvement is considered complete only because `SKILL.md` mentions it. A complete improvement needs protocol placement, schema or script support when practical, and at least one QA or regression gate.

## Completeness Rules

### Route-level completeness

A route-level improvement is complete only when all are true:

1. Router selects the route by evidence/request features.
2. Workflow plan includes the needed modules.
3. Protocol defines source roles and output rules.
4. Generator or rendering rule can enforce the surface.
5. Linter, schema or regression can fail a known bad output.

### Output-surface completeness

A student-facing output improvement is complete only when all are true:

1. The forbidden public text is listed.
2. The allowed replacement form is listed.
3. Generator avoids the forbidden text by construction where possible.
4. Linter catches the forbidden text if it appears.
5. Helper artifacts stay outside the public folder.

### Example-learning completeness

An example-derived improvement is complete only when all are true:

1. Example-specific content is marked non-transferable.
2. Transferable condition is stated generically.
3. A future-unit diagnostic question exists.
4. Validation gate checks metadata or behaviour.
5. Regression reports both fixture status and generic-contribution status.

### Scientific-precision completeness

A scientific writing improvement is complete only when all are true:

1. Entity categories are protected.
2. Aliases are collapsed before writing.
3. Evidence is written as an evidence ladder when several evidence streams support one mechanism.
4. Named detail explains its function.
5. Claim strength is calibrated to the source.

## Structural Audit Procedure

When asked to audit all previous Skill improvements:

1. Read the uploaded conversation summaries first.
2. Convert each user purpose into an improvement record.
3. Check current repo files for the destination layer and validation gate.
4. Mark unresolved gaps in `governance/skill_improvement_ledger.json`.
5. Patch architecture-level gaps before changing prose-only wording.
6. Update health commands when a new validator is added.

## Hard Failures

Fail architecture QA when:

- a required architecture file is missing;
- a ledger record has no implemented file;
- an implemented file path does not exist;
- a validation command references a missing script;
- `UnitExampleContribution`, `AnalysisContext`, `KnowledgeSurfaceContract`, `EssayAdaptiveBudget`, or `ScientificPrecisionGate` is absent from the package;
- an improvement is marked complete but has no validation gate;
- a production protocol says or implies `if [unit name], do X` outside a regression fixture.
