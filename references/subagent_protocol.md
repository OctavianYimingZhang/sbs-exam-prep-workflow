# Subagent Protocol

Use subagents when available for large multi-source exam-analysis jobs. Keep tasks independent and bounded.

## Recommended Roles

- `source-inventory agent`: inventories files, extracts text, classifies roles, and reports extraction gaps.
- `unit-grouper agent`: normalizes unit keys, detects years, detects exam regimes, and blocks cross-unit content pooling.
- `lecture-map agent`: splits lectures/modules and builds a knowledge-point map with slide anchors.
- `past-paper-pattern agent`: classifies paper formats, separates direct prediction evidence from coverage evidence, maps questions to lectures, and detects blueprint stability.
- `question-archetype-mapper agent`: extracts task verb, input format, cognitive operation, expected output, mark-scheme structure, and slot grammar.
- `mcq-distractor-analyser agent`: creates discriminator axes, distractor families, contrast pairs, formula traps, and exception lists.
- `short-answer-schema-planner agent`: creates mark-producing answer schemas and 2/4/6/8-mark skeletons.
- `coverage-closure agent`: maps every unit KP into compatible archetype slots and labels tested, partially tested, fresh, or saturated variants.
- `question-output agent`: drafts MCQ discriminator maps, short-answer schemas, or essay practice-question predictions for a specific question type.
- `visual-workbook agent`: builds or reviews the single-sheet student-facing visual workbook layout.
- `UnitExampleContributionAgent`: extracts observed unit pattern, generic Skill contribution, transferable rule, future-unit diagnostic questions, non-transferable content, affected workflows, anti-patterns prevented, and validation checks from any non-target unit example.
- `CrossUnitRegressionAgent`: runs benchmark units as separate regression fixtures and reports both unit-specific pass/fail and generic contribution pass/fail against `cross_subject_regression_protocol.md`. It must explain what reusable workflow rule each unit validates.
- `spreadsheet-verifier agent`: reviews the generated workbook for readability, sheet completeness, clipping, missing anchors, and unsupported claims.

## Delegation Rules

- Do not give the same source group to multiple agents unless independent validation is needed.
- Do not ask a subagent to invent content; require source anchors and uncertainty labels.
- Give each agent a clear output schema and prohibit file edits unless the agent is explicitly assigned a write task.
- Keep workbook generation in one owner to avoid conflicting writes.

## Useful Parallel Split

For a large unit:

1. Run source inventory locally or in one subagent.
2. Run unit grouping and regime split before any cross-paper comparison.
3. In parallel, assign lecture mapping to one agent and past-paper pattern/archetype analysis to another.
4. After both return, run coverage closure and question-type outputs locally or split by MCQ/short-answer/essay.
5. Build the workbook locally.
6. Use one verifier agent only if time and tools allow.

## Required Verification

Before accepting subagent output:

- check that source paths exist;
- check that claims have anchors or are labelled uncertain;
- check that all comparisons are within the same `unit_key`;
- check that old-regime papers are not used as current-regime blueprint evidence;
- check that archetype and slot grammar claims are separated from KP hotness claims;
- check that old/non-comparable papers were not used as direct essay predictions;
- check that the output matches the requested question type.
- check that slide/page images preserve aspect ratio and remain readable;
- check that the main visual workbook preserves first-to-last lecture order.
- check that every Unit-specific example is labelled with transferable contribution and non-transferable content;
- check that benchmark content has not been used as target-unit factual or prediction evidence;
- check that a benchmark lesson is applied only after structural trigger evidence is found in the target unit;
- check that subagent outputs distinguish unit-specific fixture pass/fail from generic contribution pass/fail.
