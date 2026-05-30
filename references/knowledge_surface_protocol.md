# Knowledge Surface Protocol

This protocol controls the last public-rendering layer for all student-facing outputs. It sits after evidence extraction, ontology construction, planning, and route-specific drafting.

The problem it prevents is not factual inaccuracy alone. It prevents the Skill from exposing planning scaffolds, source-route narration, AI process notes, or rigid bucket labels as if they were revision content.

```text
AtomicKnowledgeLedger -> PublicKnowledgeUnit -> KnowledgeSurfaceContract -> NonKnowledgeGate -> LabelDecision -> Student DOCX
```

## Core Rule

Student-facing output must contain knowledge only.

A public sentence, heading, bullet, table row, figure caption, or note is allowed only if it performs one of these functions:

- defines a term or boundary;
- explains a mechanism, pathway, process, method, assay, calculation, graph, data readout, diagnostic rule, or comparison;
- gives a source-backed example or experimental result and interprets what it shows;
- states a limitation, caveat, exception, or scope boundary that changes understanding;
- connects concepts in a way that improves biological, clinical, methodological, or quantitative understanding.

A public item is forbidden when its main function is to describe the Skill, the source route, the AI workflow, the exam-prediction workflow, the evidence audit, or how the student should use the document.

## KnowledgeSurfaceContract

Use this object before any public DOCX is written:

```yaml
KnowledgeSurfaceContract:
  contract_id:
  route:
  allowed_public_functions:
    - definition
    - mechanism
    - process
    - method_workflow
    - assay_readout
    - calculation
    - graph_data_rule
    - diagnostic_rule
    - comparison
    - example_interpretation
    - limitation_or_scope
    - synthesis
  forbidden_public_functions:
    - source_route_narration
    - ai_process_or_provenance
    - audit_trace
    - generic_study_advice
    - exam_meta_or_prediction_trace
    - rigid_template_bucket
    - evidence_justification_trace
    - decorative_transition
  label_policy:
    mode: semantic_sparse
  density_policy:
    mode: source_adaptive
  qa_status:
```

The contract is route-independent. `exam_prep_notes_docx`, `knowledge_walkthrough_docx`, `mcq_exam_prep`, `short_answer_exam_prep`, `long_answer_project_scenario_prep`, and `essay_exam_prep` all pass through it.

## Non-Knowledge Classes

### 1. Source-route narration

Reject wording whose main purpose is to report where a claim came from or how slides/pages were ordered.

Forbidden visible patterns include:

```text
This slide shows...
The first slide shows...
The second slide shows...
The slide says...
The slide mentions...
The notes say...
According to page...
PPT page...
English explanations extracted from...
```

Rewrite by deleting the source-route wrapper and keeping only the knowledge.

Bad:

```text
The second slide shows the opposite side of the body.
```

Good:

```text
The crossed extensor reflex activates contralateral extensors and inhibits contralateral flexors so the unstimulated limb supports body weight.
```

### 2. AI process or provenance

Reject public text that describes AI activity, prompt instructions, extraction method, or generation evidence.

Forbidden visible patterns include:

```text
AI generated this...
I extracted...
I used the image/text to...
Generated from ChatGPT...
This document was produced by...
Only knowledge points are included...
I did not include how-to-answer content...
```

Public notes must not state what the AI did or chose not to do. The output itself must simply be the knowledge.

### 3. Audit trace and evidence justification

Reject public source maps, coverage notes, confidence notes, quality caveats, ELM warnings, internal QA flags, run manifests, citation logs, source anchors, and statements explaining why the Skill trusted or rejected material.

Keep these only in internal QA or in an explicitly requested audit package.

### 4. Generic study advice and answer coaching

Reject public prose such as:

```text
How to use this document
How to answer
A strong answer should...
Use this module...
Recommended approach
Exam strategy
Integrated reasoning
```

If the sentence contains real knowledge, rewrite only the knowledge. If it is pure advice, delete it.

### 5. Rigid template buckets

The Skill must not mechanically render every point as:

```text
Definition:
Principle:
Mechanism:
Application:
Limitation:
Graph logic:
Interpretation:
```

These labels are allowed only when the label is genuinely needed for readability and the labelled block is the natural content type. They are not a required sequence.

Preferred public heading style is semantic and topic-specific:

```text
Beer-Lambert conversion from A440 to product concentration
Initial rate is the concentration slope at the start of the reaction
PCR-RFLP turns a SNP into a fragment-pattern difference
Ib feedback reverses sign between rest and walking
```

The reader should see the concept first, not the template bucket.

## LabelDecision

Every visible label must pass this decision:

```yaml
SurfaceLabelDecision:
  label:
  function:
  decision: keep | merge_into_heading | merge_into_sentence | delete
  reason:
```

Keep labels for equations, worked examples, tables, comparisons, diagnostic rules, and calculations when they prevent ambiguity. Delete or merge labels that merely expose the internal scaffold.

## Notes And Walkthrough Rendering

`exam_prep_notes_docx` and `knowledge_walkthrough_docx` should use compact knowledge modules.

Allowed public structure:

```text
Title
Course Knowledge Map
Lecture or Topic Title
[★★★ | ★★ | ★] Topic-specific knowledge heading
Connected explanatory prose
Optional equation, worked example, method workflow, comparison, or limitation block when useful
```

Forbidden public structure:

```text
How To Use This Document
What This Lecture Is About
What This Module Explains
The first slide shows...
The notes are organised by...
Definition / Principle / Limitation repeated for every point
Coverage note
Evidence used
AI process note
```

A `Course Knowledge Map` is allowed only when it is a knowledge map: topic boundaries, concept dependencies, and major knowledge blocks. It must not contain instructions about how the AI generated the notes, why evidence was selected, or what was intentionally omitted.

## Practical And Data Notes

For practical/data/problem material, preserve equations, units, workflows, and graph rules, but avoid turning every item into the same mini-template.

Bad:

```text
Definition: V0 is...
Calculation logic: ...
Interpretation: ...
```

Good:

```text
Initial rate, V0, is the product-formation rate at the start of the reaction. Measure the initial A440 slope, then convert absorbance per minute into concentration per minute using Beer-Lambert: rate = slope/(epsilon l). With a 0.25 A min^-1 slope, epsilon = 6500 M^-1 cm^-1 and l = 1 cm, V0 = 38.5 micromol l^-1 min^-1.
```

Use labelled blocks only for genuinely separate items such as `Equation`, `Worked example`, `Diagnostic pattern`, or `Control`.

## Example Essay Surface

Example Essays are not notes. They require continuous essay prose, adaptive length, citations/highlights where source class requires them, and a conclusion.

Use this internal budget object:

```yaml
EssayAdaptiveBudget:
  question:
  command_verb:
  lecture_scope:
    - single_concept
    - one_lecture
    - multi_lecture
    - whole_module
    - cross_module
  core_source_skeleton_words:
  mechanism_detail_target_ratio: 0.10-0.15
  extra_reading_target_ratio: 0.10-0.15
  estimated_total_word_range:
  conclusion_required: true
  compression_policy: expression_efficiency_not_fixed_count
```

Rules:

- Do not hard-code 500-1000 words.
- Word count follows question demand, lecture scope, amount of examinable source content, and required evidence.
- Add molecular, cellular, receptor, channel, pathway, morphogen, assay, circuit, gene, or method detail only when it sharpens a lecture/source mechanism slot.
- Add Extra Reading or academic-paper detail only when it is verified, source-anchored, question-relevant, and analytically interpreted.
- Treat 10-15% mechanism-detail and 10-15% Extra Reading as target bands, not padding quotas. If insufficient verified material exists, do not fabricate or inflate.
- The conclusion is mandatory unless the user explicitly asks for a fragment rather than a complete essay.
- The conclusion must synthesise the answer and should not introduce new evidence.

## Highlight Surface Rules For Essays

Highlighting is a source-bound rendering rule, not a style choice.

- Uploaded Extra Reading Books or matched textbook chapters: yellow highlight.
- Verified Citation / Extra Reading Papers: green highlight with parenthetical author-year citation.
- Lecture-slide cited original papers after resolution/reading: green highlight with parenthetical author-year citation.
- Verified classic experimental sources used as fallback: green highlight with parenthetical author-year citation.
- Ordinary lecture material: no highlight.

Fail the essay if:

- academic paper content is not green-highlighted;
- uploaded book/chapter Extra Reading content is not yellow-highlighted;
- green-highlighted content lacks a parenthetical author-year citation;
- highlighted content is broader than the source-derived phrase or clause;
- the highlight exists only to increase the Extra Reading ratio.

## Publish Gate

Before publishing any public DOCX, run this sequence:

```text
1. Surface function scan: every visible item must be knowledge-bearing.
2. Non-knowledge scan: reject source-route narration, AI process, audit trace, study advice, and exam-meta leakage.
3. Label-decision scan: delete or merge rigid template labels unless the label is semantically necessary.
4. Route-style scan: compact notes use black Arial, left alignment, compact spacing; essays use essay DOCX style.
5. Essay-specific scan: adaptive budget, conclusion, source-class highlights, citation colour, and word-count efficiency.
```

If any scan fails, rewrite the public surface rather than adding a disclaimer.
