# Long-Answer Example Protocol

Use this protocol when the exam uses non-essay, paragraph-style, project/scenario-based long answers. The output should read as a high-score experimental, practical, or scenario argument, not as a broad essay.

Trigger only when exam-format parsing or the user's request shows project, scenario, method-design, readout-interpretation, research-proposal, data/problem, or control/limitation structure.

## A. Source Digestion Before Writing

Before planning or drafting:

- read the relevant lecture/practical/source pages in source order;
- inspect rendered images when diagrams, structures, gels, spectra, tables, graphs, or handwritten exemplars matter;
- preserve source logic before segmenting: what problem is introduced, which method or mechanism follows, what readout it produces, and what limitation or control is required;
- use exemplars only for answer structure, paragraph logic, density, and wording style;
- ignore student annotations as factual course content unless the user explicitly asks to use them as notes;
- do not use exemplar subject claims as facts unless verified from official course material or reliable academic sources.

For method-heavy project exams, separate:

```text
method principle -> scenario application -> expected readout -> interpretation -> limitation/control
```

Do not transfer method families, systems, techniques, case studies, or recurrence claims from an example unless the target sources contain them.

## B. Knowledge Inventory

Construct this inventory before writing:

```yaml
LongAnswerKnowledgeInventory:
  must_use_core:
    - source points directly required by the question
  should_use_if_space:
    - supporting source points that improve precision
  method_or_process_principle:
    - examinable principle of each method/process
  scenario_application:
    - how the method/process applies to the given case
  readout_and_interpretation:
    - what the output would show and how it answers the question
  controls_or_limitations:
    - caveats, controls, alternatives, or weaknesses
  cross_source_links:
    - legitimate links to other source blocks in the same target set
  verified_extra_reading:
    - compact refinement only
  exclude:
    - true but non-useful facts for this question
```

Prioritise content that directly answers the command verb. Exclude methods or details that are true but not justified by the scenario.

## C. Pattern Inference

Test, do not assume:

- one lecturer gives one question;
- one module gives one question;
- one lecture gives one question;
- one knowledge point gives one question;
- cross-module synthesis;
- method-design slots;
- data/readout-interpretation slots;
- comparison-choice slots;
- scenario/problem slots;
- limitation/control slots.

Do not write by lecturer or source block in isolated sections unless the question itself is split that way.

## D. Paragraph Planning

Plan every long answer before drafting:

```yaml
LongAnswerParagraphPlan:
  paragraph_no:
  question_part:
  paragraph_function:
    - strategy_framing
    - core_mechanism_or_process
    - method_principle
    - method_application
    - readout_interpretation
    - comparison_choice
    - limitation_control
    - extra_reading_refinement
    - concluding_integration
  claim_or_goal:
  source_content_used:
  scenario_facts_used:
  method_or_mechanism:
  expected_readout:
  interpretation:
  control_or_limitation:
  extra_reading_use:
  excluded_content:
  word_budget:
```

Follow question parts and mark weighting. Higher-mark parts need more explanation, readout interpretation, and controls.

## E. Required Answer Logic

Default logic:

```text
question goal -> source principle -> scenario-specific application -> expected evidence/readout -> interpretation -> limitation/control
```

Every sentence must do one of these jobs:

- answer the command verb;
- justify method choice;
- connect source knowledge to the scenario;
- interpret a readout;
- add a necessary caveat or control;
- compare alternatives when the question requires a choice.

Do not write generic topic summaries, unconnected method lists, or broad essay introductions.

## F. Compact Academic Language

Useful sentence functions:

Purpose framing:

- `The central problem is to determine whether...`
- `The first step is to establish...`

Scenario anchoring:

- `Given that the question specifies..., the answer should focus on...`
- `This method is appropriate here because...`

Principle-to-application:

- `[Method] works by [principle], so in this scenario it can test...`

Readout interpretation:

- `A change in [signal/readout] would indicate...`
- `If the hypothesis is correct, the expected result is...`

Contrast:

- `This approach is preferable to [alternative] because...`
- `This alone would not prove..., so it should be combined with...`

Limitation/control:

- `The main limitation is...`
- `A suitable control would be...`
- `This should be checked because...`

Avoid decorative openings, repeated vague phrases, and padding. A word limit is a maximum, not a target.

## G. Extra Reading

Extra reading must be a compact refinement, not a second answer.

Source hierarchy:

1. recommended reading explicitly listed in lecture slides, handouts, or guidance;
2. books recommended by the lecturer or course handbook;
3. papers named in lecture slides;
4. peer-reviewed reviews or primary papers from PubMed, Google Scholar, DOI, or publisher pages;
5. standard textbooks.

If recommended reading is not present in uploaded material, ask whether the user has a recommended reading list. If the user says no, unknown, or gives no usable list, use verified academic papers or textbooks only when needed.

Extra reading may appear only as:

- one short paragraph;
- two to four integrated sentences;
- one named method example;
- one method-limitation clarification;
- one directly relevant modern/application context.

Reject unrelated detail, unverified citations, multiple extra-reading paragraphs, or any external point that changes the source-grounded answer.

## H. Transferable Long-Answer Operations

Apply these operation types only when exam-format parsing confirms scenario, project, method-design, readout-interpretation, or control/limitation structure:

- design a strategy;
- choose and justify methods;
- assess quality, state, performance, or validity;
- quantify a relationship or parameter;
- interpret an intervention or mutation/effect;
- determine an interaction, interface, pathway, structure, or causal relation;
- compare methods by suitability;
- quantify activity, performance, or specificity;
- explain a mechanism under scenario constraints;
- identify in vivo, clinical, environmental, engineering, or practical caveats.

For every operation, include:

- source principle;
- scenario-specific choice;
- expected readout;
- interpretation;
- limitation/control.

## I. QA Flags

Add or use these flags when relevant:

- `long_answer_project_scope_uncertain`;
- `paragraph_plan_missing`;
- `method_principle_missing`;
- `scenario_fact_not_used`;
- `expected_readout_missing`;
- `interpretation_missing`;
- `control_or_limitation_missing`;
- `generic_essay_written_for_project_question`;
- `old_regime_used_as_current_blueprint`;
- `extra_reading_unverified`;
- `example_used_as_fact`.

Fail safe by omitting uncertain mechanisms, citations, or lecturer preferences rather than inventing them.
