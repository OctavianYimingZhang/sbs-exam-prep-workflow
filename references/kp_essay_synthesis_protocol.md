# KP Essay Synthesis Protocol

This protocol governs knowledge-point explanation prose for legacy workbook compatibility and internal prose linting. It is not full Example Essay Mode and not the default lecture-review DOCX route. Current public exam-prep outputs should use the lecture walkthrough DOCX and question-type DOCX add-ons.

Use `language_quality_contract.md` for shared prose-quality rules. This file adds workbook-specific constraints: no source tracing in explanation cells, no how-to-write language, and no page/slide narration.

## Core Separation

Internal source coverage and final student-facing prose are different products.

Internal coverage may preserve:

- slide/page order;
- page ranges;
- extracted slide text;
- OCR quality notes;
- raw bullet fragments;
- source anchors;
- coverage audit records;
- diagnostic flags.

The visible explanation cell must not describe that coverage. It must state the scientific argument directly.

Hard rule:

```text
Source coverage is satisfied by slide images, page ranges, coverage audit, and internal diagnostics. The explanation cell is not responsible for mentioning every page. Never preserve coverage by narrating page-by-page content in prose.
```

## Workbook Explanation Definition

The workbook explanation is:

- a concept-level paragraph, not a source trace;
- written for revision as a reusable essay paragraph fragment;
- normally 80-180 words;
- up to 240 words only for genuinely complex multi-mechanism KPs;
- direct academic English prose;
- factual only from target source evidence or verified sources;
- free of instructions to the student;
- free of page-by-page or slide-by-slide narration.

The paragraph itself is the output. Do not write commentary about how the student should write the paragraph.

## Required Paragraph Structure

Every KP synthesis should follow this structure unless the source material clearly requires a different order:

1. Topic sentence: state the scientific problem, principle, or argument.
2. Causal or mechanistic development: explain how actors, processes, compartments, signals, cells, or methods relate.
3. Named lecture examples: include only the most useful examples, not every extracted bullet.
4. Consequence or link-back: state why the mechanism matters for explanation, prediction, application, physiology, pathology, design, exam argument, or experimental interpretation.

Allowed source-order use:

```text
Use slide/page order to understand lecture logic, prerequisites, and transitions. Do not expose slide/page order as the prose structure.
```

## Domain Templates

Choose the best template by evidence in the target sources, not by benchmark identity.

### Neural / Control Systems

```text
behaviour or control problem -> circuit, sensory, or control mechanism -> functional or clinical consequence
```

Example logic: posture, gaze, reflexes, voluntary movement, sensory feedback, control hierarchy, lesion effects.

### Metabolism

```text
substrate, compartment, enzyme, or regulator -> flux or energetic state -> physiological consequence
```

Example logic: ATP/NADH balance, substrate routing, enzyme regulation, compartmentalisation, fed/fasted or stress state.

### Immune Response

```text
trigger, antigen, or damage signal -> cell, receptor, or cytokine interaction -> effector response -> disease, protection, diagnosis, or therapy implication
```

Example logic: PRR/PAMP/DAMP recognition, antigen presentation, cytokine networks, effector differentiation, immune pathology, vaccination or therapy.

### Plant / Agricultural Systems

```text
agricultural/environmental problem or trait -> plant mechanism, gene, hormone, physiology, or breeding tool -> evidence or named example -> crop or food-security consequence
```

Example logic: yield, climate stress, photosynthesis, flowering, hormones, genetic variation, breeding, transformation, crop resilience.

### Experimental / Data KPs

```text
question or problem -> method or evidence principle -> readout or inference -> limitation or consequence
```

Example logic: assay principle, graph interpretation, control, expected result, biological inference, limitation.

### Comparison KPs

```text
shared problem -> comparison axis -> contrast in mechanism or examples -> synthesis
```

Do not write all facts for one side followed by all facts for the other. Compare directly on the chosen axis.

## Mandatory KP Essay Synthesis Pass

Run this pass after Knowledge-point optimisation and before student-facing prose is written:

```yaml
KPEssaySynthesisPass:
  input:
    - KP title
    - source page range
    - slide images
    - extracted text where reliable
    - lecture/module order
    - exam format and question type
    - confidence flags
  steps:
    - use slide/page order only to infer lecture logic
    - compress raw extracted text into examinable claims
    - choose a paragraph archetype from the domain templates
    - draft direct student-facing prose
    - run a de-slide rewrite pass
    - run the essay-style linter or an equivalent banned-pattern check
    - write only the cleaned synthesis into the student-facing explanation section
  output:
    - clean explanation paragraph
    - diagnostics for omitted/uncertain/low-OCR evidence
```

## De-Slide Rewrite Pass

Before publishing student-facing prose, remove:

- page numbers used as prose structure;
- slide numbers used as prose structure;
- `first establishes`, `then develops`, `then closes`;
- `KP covers pages`;
- `slide sequence should be read as`;
- `remaining linked pages`;
- `central idea for this block`;
- `central examinable idea in this knowledge block`;
- `should be understood as`;
- `best written as`;
- `is mainly an argument about`;
- instructions such as `In an essay answer...`;
- any phrase that explains how to transform pages into a paragraph rather than providing the paragraph.

Rewrite by asking:

```text
If the page numbers disappeared, what scientific argument remains?
What is the mechanism, model, process, or operation?
Which named example genuinely improves the claim?
What consequence makes this examinable?
```

## Bad-To-Target Examples

Bad:

```text
Pages 25-27 should be read as one connected paragraph. Page 25 first establishes the operating problem. Page 26 then develops the degradation risk.
```

Target:

```text
Battery degradation is best framed as an interaction between electrode chemistry, ion transport and operating conditions rather than as a single failure mode. High current, repeated cycling and temperature stress can accelerate side reactions or structural change, reducing the active material available for reversible charge storage. The examinable argument is that performance loss is mechanistic: operating choices alter microscopic processes, and those processes accumulate into measurable capacity fade.
```

Bad:

```text
KP covers pages 15-24. The slide sequence should be read as an overview of measurement reliability, with remaining linked pages adding examples.
```

Target:

```text
Measurement reliability depends on separating systematic bias from random error. Bias shifts observations in a consistent direction, while random error widens the spread of repeated measurements, so calibration and replication solve different problems. This distinction matters because a precise instrument can still be wrong if it is miscalibrated, whereas an unbiased but noisy instrument may require more repeated observations before the underlying signal is clear.
```

Bad:

```text
The central idea for this block is reaction-rate control. In an essay answer, use these pages to explain the first part of the sequence and then add the later pages.
```

Target:

```text
Reaction-rate control links microscopic collision conditions to macroscopic yield, selectivity and safety. Temperature, concentration, catalysts and surface area alter the probability that particles collide with sufficient energy and the correct orientation, so changing a process condition changes both rate and sometimes product distribution. The examinable point is that rate is not a descriptive constant; it is a mechanistic consequence of controllable variables.
```

## Exam-Facing Prep Rule

`Exam-Facing Prep` must contain actual preparation products:

- predicted practice questions;
- answer operations;
- comparison axes;
- data/problem prompts;
- mark-producing schemas;
- MCQ discriminator axes;
- short-answer skeletons;
- method/readout/control prompts.

It must not say `Turn pages X-Y into one paragraph`, `use these pages`, or similar coverage-to-writing instructions.

## Factual Safety

Do not invent biological content to make prose smoother. If extracted text is insufficient, inspect available slide images or source evidence where possible. If the evidence still does not support a confident paragraph, write a conservative claim and flag low confidence internally rather than adding unsupported mechanisms, examples, dates, names, statistics, or citations.

Exemplars may guide style, paragraph density, and logic only. Do not copy exemplar factual claims or treat them as authority unless verified from the target source materials or reliable sources.

## Acceptance Criteria

The workflow passes this protocol if:

- concept-first synthesis quality is preserved across source sets;
- page-trace and module-overview anti-patterns no longer narrate pages/slides in the explanation column;
- at least 95% of KP explanation cells contain direct essay-style synthesis without banned phrases;
- explanation cells do not tell the student how to write;
- explanation cells provide the paragraph itself;
- prep cells contain practice questions, answer schemas, or exam operations, not `turn pages into a paragraph`;
- coverage remains preserved through page ranges, slide images, KP grouping, and audit/diagnostic outputs;
- full Example Essay generation remains opt-in only.
