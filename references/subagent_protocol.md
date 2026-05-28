# Subagent Protocol

Use subagents when available for large multi-source exam-analysis jobs. Keep tasks independent and bounded.

## Recommended Roles

- `source-inventory agent`: inventories files, extracts text, classifies roles, and reports extraction gaps.
- `target-grouper agent`: normalizes target group keys, detects years, detects exam regimes, and blocks cross-source content pooling.
- `lecture-map agent`: splits lectures/modules and builds a knowledge-point map with slide anchors.
- `past-paper-pattern agent`: classifies paper formats, separates direct prediction evidence from coverage evidence, maps questions to lectures, and detects blueprint stability.
- `question-archetype-mapper agent`: extracts task verb, input format, cognitive operation, expected output, mark-scheme structure, and slot grammar.
- `mcq-distractor-analyser agent`: creates discriminator axes, distractor families, contrast pairs, formula traps, and exception lists.
- `short-answer-schema-planner agent`: creates bounded answer variants, highlighted keywords, and Example Answer logic.
- `coverage-closure agent`: maps every KP into compatible archetype slots and labels tested, partially tested, fresh, or saturated variants.
- `question-output agent`: drafts MCQ Point Cards, short-answer reports, long-answer/project/scenario reports, or essay module packs for a specific question type.
- `docx-output agent`: builds or reviews the student-facing walkthrough or question-type DOCX layout.
- `ExampleContributionAgent`: extracts observed source pattern, generic Skill contribution, transferable rule, future-source diagnostic questions, non-transferable content, affected workflows, anti-patterns prevented, and validation checks from any external example.
- `RegressionAgent`: runs benchmark fixtures separately and reports both fixture pass/fail and generic contribution pass/fail against `cross_subject_regression_protocol.md`. It must explain what reusable workflow rule each benchmark validates.
- `docx-verifier agent`: reviews generated DOCX reports for formatting, readability, missing anchors, and unsupported claims.

Essay-specific roles when `essay_exam_prep` or complete essay drafting is active:

- `question-and-rubric agent`: extracts command verb, required scope, excluded scope, examiner expectation, and off-topic risks.
- `literature-retrieval agent`: finds required readings, seminal papers, recent papers, reviews, and candidate sources with DOI/PMID/URL status.
- `mechanism-theory agent`: maps mechanisms, models, source support, evidence strength, and limitations to essay sections.
- `evidence-appraisal agent`: calibrates claim strength and allowed verbs for each major source-backed claim.
- `citation agent`: verifies metadata, citation placement, source-to-claim fit, in-text citations, and reference-list entries.
- `figure-table-data agent`: checks figure reuse permission, generated schematic scope, academic table value, and data-analysis requirements.
- `critical-thinking agent`: checks analytic/descriptive balance, discussion quality, limitation use, and model comparison.

## Delegation Rules

- Do not give the same source group to multiple agents unless independent validation is needed.
- Do not ask a subagent to invent content; require source anchors and uncertainty labels.
- Give each agent a clear output schema and prohibit file edits unless the agent is explicitly assigned a write task.
- Keep DOCX generation in one owner to avoid conflicting writes.

## Useful Parallel Split

For a large source set:

1. Run source inventory locally or in one subagent.
2. Run target grouping and regime split before any cross-paper comparison.
3. In parallel, assign lecture mapping to one agent and past-paper pattern/archetype analysis to another.
4. After both return, run coverage closure and question-type outputs locally or split by MCQ/short-answer/essay.
5. Build the DOCX walkthrough and requested add-on reports locally.
6. Use one verifier agent only if time and tools allow.

## Required Verification

Before accepting subagent output:

- check that source paths exist;
- check that claims have anchors or are labelled uncertain;
- check that all comparisons are within the same `target_group_key` or compatible target group;
- check that old-regime papers are not used as current-regime blueprint evidence;
- check that archetype and slot grammar claims are separated from KP hotness claims;
- check that old/non-comparable papers were not used as direct essay predictions;
- check that the output matches the requested question type.
- check that visual source material preserves aspect ratio and remains readable when included;
- check that the main walkthrough preserves first-to-last lecture order.
- check that every external example is labelled with transferable contribution and non-transferable content;
- check that benchmark content has not been used as target factual or prediction evidence;
- check that a benchmark lesson is applied only after structural trigger evidence is found in target sources;
- check that subagent outputs distinguish fixture pass/fail from generic contribution pass/fail.
- for essay roles, check that candidate sources are not treated as verified citations until metadata and claim relevance are confirmed.
