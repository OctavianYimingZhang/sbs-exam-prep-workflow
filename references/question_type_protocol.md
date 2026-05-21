# Question Type Protocol

## QuestionType Enum

Classify before prediction:

- `mcq_single_best`
- `mcq_multiple_true_false`
- `mcq_statement_judgement`
- `fill_blank`
- `short_answer_define`
- `short_answer_list`
- `short_answer_explain`
- `short_answer_compare`
- `short_answer_experiment`
- `data_problem`
- `essay_theory`
- `essay_compare_contrast`
- `essay_experimental_design`
- `essay_scenario`
- `essay_disease_mechanism`
- `long_answer_project`
- `mixed_or_uncertain`

Never apply SBS K/C/U/A/R to MCQ, fill-blank, short-answer, or problem-based questions. Apply K/C/U/A/R only to essay-based theory answers.

## MCQ Statement-Level Map

For MCQ-heavy exams, predict discriminator axes and distractor families, not long model answers and not exact stems.

MCQ extraction schema:

```yaml
MCQPattern:
  unit_key:
  exam_regime:
  year:
  question_no:
  question_mode: definition | classification | mechanism | calculation | exception_not | graph_figure | application
  correct_concept:
  discriminator:
  distractor_families: []
  trap:
  compatible_kps: []
  source_question:
```

MCQ pattern categories:

- `definition`: terms likely to be confused.
- `classification`: category boundaries.
- `mechanism`: causal direction and sequence.
- `calculation`: formula, units, order of magnitude.
- `exception_not`: common incorrect statements.
- `graph_figure`: curve shape, graph reading, diagram logic.
- `application`: correct explanation in a new scenario.

For MCQ-heavy exams, create a statement/discriminator map:

- likely true statements;
- likely false/distractor statements;
- common contrast pairs;
- numbers/locations/names likely to be tested;
- mechanism-order traps;
- definition traps;
- exceptions;
- lecture-only wording that should be memorised.
- one-sentence rule;
- wrong-option diagnosis.

Required `MCQ_HighFrequency` fields:

- Lecture;
- Knowledge point;
- Why high frequency;
- Likely MCQ statement;
- Correct answer / truth value if knowable;
- Common trap;
- Source slide/page;
- Confidence.

If no answer key exists, do not invent official answers. Mark answers as `inferred_from_lecture`.

MCQ preparation output should be:

- term-pair contrast table;
- formula flashcards;
- wrong-option diagnosis;
- one-sentence rules;
- exception list;
- `NOT / incorrect` scan habits.

Do not output `X will be tested` when the stronger claim is `X is a likely discriminator boundary`.

## Short-Answer Mark-Point Generator

For short-answer questions, predict `question archetype -> mark-producing answer schema`, not only topic labels.

Short-answer extraction schema:

```yaml
ShortAnswerPattern:
  unit_key:
  exam_regime:
  year:
  question_no:
  marks:
  stem_type:
  task_verbs: []
  input_format:
  primary_kp:
  supporting_kps: []
  operation: []
  answer_schema: []
  archetype_id:
```

Short-answer prediction output must say how a KP can be asked. For example:

- explain variability between cases;
- compare/rank alternatives;
- calculate or interpret a parameter;
- draw/label a structure;
- list named examples;
- build a stepwise causal chain.

Generate two answer layers:

1. `Exam Answer`
   - concise student-style answer;
   - directly answers the question;
   - uses lecture wording where possible;
   - English only.

2. `Reference Expansion`
   - more acceptable points than required;
   - alternative acceptable examples;
   - extra detail if useful;
   - source anchors.

If marks are visible, infer minimum scoring points from marks and wording, but do not claim exact official allocation unless a mark scheme exists. If wording says `list three`, provide at least three core answers plus additional acceptable examples. If the answer is not found in supplied lecture slides/notes, explicitly flag `Not found in supplied lecture material.`

Extra reading may appear only under `Optional extra-reading refinement` unless lecture content is insufficient.

Generate mark-length skeletons where relevant:

- 2-mark version: one-line definition or two named points.
- 4-mark version: definition plus two to three linked explanatory points.
- 6-mark version: mechanism with causal sequence and named examples.
- 8/10-mark version: full schema including comparison, diagram, data interpretation, or scenario conclusion.

Do not claim exact official mark allocation unless an official mark scheme is present.

## Long-Answer Project / Scenario Outputs

Use `long_answer_project` when the formal paper is non-essay but requires paragraph-style project, scenario, method-design, or research-proposal answers. This is separate from ordinary essay theory.

Long-answer project extraction schema:

```yaml
LongAnswerProjectPattern:
  unit_key:
  exam_regime:
  year:
  question_no:
  project_context:
  named_proteins_or_systems: []
  question_parts:
    - part_label:
      mark_weight:
      command_verbs: []
      required_operation:
      likely_lecture_blocks: []
      output_expected:
  core_archetype:
  slot_grammar:
  required_answer_mode:
  cross_module_links: []
```

Method-driven long-answer project archetypes learned from the BIOL21111 benchmark:

Apply these archetypes to future units only when exam-format parsing confirms scenario, project, method-design, readout-interpretation, or control/limitation structure. Do not transfer protein-specific systems, techniques, or recurrence claims unless supplied in the new unit's sources.

- design purification strategy;
- choose and justify characterisation methods;
- assess folding, secondary, tertiary, or quaternary structure;
- quantify binding affinity or dimerisation affinity;
- interpret mutation effect;
- determine protein-protein interface;
- determine atomic or high-resolution structure;
- compare structural biology methods;
- quantify enzyme activity or substrate specificity;
- explain chaperone or folding mechanism;
- identify in vivo or biotechnological caveats.

For each long-answer archetype, require:

- lecture principle;
- scenario-specific method choice;
- expected readout;
- interpretation;
- limitation/control.

When a user explicitly asks for a model answer or Example Essay for a project/scenario unit, route to `long_answer_example_protocol.md` and generate a `High-score example long answer`, not a generic essay. The answer must be structured by question parts, mark weights, method logic, readouts, interpretation, and controls.

Do not let old short-answer or coverage-only papers control the current long-answer project blueprint. They may support concept coverage only unless exam-format parsing proves the same regime.

## Essay Outputs

For each predicted essay, output predicted practice questions by default. Generate a full Example Essay only when the user explicitly asks for an Example Essay, model essay, essay-style answer, essay paragraph, or similar.

When Example Essay Mode is triggered, follow `essay_generation_protocol.md`.

If the exam-format gate classifies the target as `long_answer_project`, follow `long_answer_example_protocol.md` instead of the essay-generation protocol.

For every essay output, require:

- Question deconstruction;
- Lecture anchors;
- Knowledge inventory;
- Lecturer-intent analysis;
- Paragraph plan;
- Extra-reading insertion decision;
- High-score example essay when explicitly requested;
- Paragraph function map;
- Figure plan;
- Extra reading;
- Exclusion list;
- K/C/U/A/R self-check.

Use K/C/U/A/R only for essay-based theory answers.

Every essay paragraph must be split into separate Excel rows:

- paragraph number;
- paragraph text;
- function;
- source anchor;
- K/C/U/A/R contribution;
- why included;
- what was excluded.

Do not write slide-by-slide summaries. Each paragraph must serve the question command verb.

For the default student-facing visual workbook, include predicted essay practice questions only. Do not include full example essays unless the user explicitly requests examples.

The essay must be built from paragraph functions, not from slide order alone. Slide order informs lecture logic; paragraph order is determined by the command word, expected scope, and lecturer intent.

If the question has a 1000-word maximum and no minimum, maximise relevance per word. Do not pad. Omit background that does not answer the question.

Required essay paragraph pattern:

```text
Claim -> mechanism -> evidence/example -> biological consequence -> link back to question.
```

Required output structure for direct-chat Example Essays:

```text
Question Analysis
Paragraph Plan
Extra Reading Insert
Example Essay
Examiner-Fit Checklist
```
