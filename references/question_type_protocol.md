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
- `practical_protocol`
- `spotter_image`
- `numerical_problem`
- `case_study`
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
  target_group_key:
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
- `calculation`: formula, measurement convention, order of magnitude.
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

Internal `MCQ_HighFrequency` fields may include:

- Lecture;
- Knowledge point;
- Why high frequency;
- Likely MCQ statement;
- Correct answer / truth value if knowable;
- Common trap;
- Source slide/page;
- Confidence.

The default student-facing MCQ report is a Point Card report only. Convert the internal map into `MCQStudentPointCard` objects:

```yaml
MCQStudentPointCard:
  priority: 必备 | 重点 | 补充
  point: string
  knowledge_explanation: string
  how_exam_tests_it: string
  common_traps: []
  must_remember: string
```

Do not include practice questions, answer keys, contrast tables, separate trap banks, source anchors, confidence, evidence, examiner-operation labels, or discriminator-axis labels in the default MCQ high-yield report. Fold wrong-option logic into `common_traps`.

If no answer key exists, do not invent official answers. Mark answers as `inferred_from_lecture`.

If a visible MCQ regime includes negative marking, multiple-response marking, or statement-level scoring, extract an `MCQScoringPolicy`:

```yaml
MCQScoringPolicy:
  mode: single_best | multiple_true_false | statement_judgement
  option_count:
  correct_value:
  wrong_value:
  unanswered_value:
  positive_ev_threshold:
  action_rule:
```

If unanswered answers score zero, correct answers score `c`, and wrong answers lose `d`, the internal positive expected-value threshold is:

```text
p > d / (c + d)
```

This policy supports answer strategy. It must not be used to invent official answers.

Internal MCQ analysis may contain:

- term-pair contrast table;
- formula flashcards;
- wrong-option diagnosis;
- one-sentence rules;
- exception list;
- `NOT / incorrect` scan habits.

Do not output `X will be tested` when the stronger claim is `X is a likely discriminator boundary`.

## Short-Answer Mark-Point Generator

For short-answer questions, predict `question archetype -> mark-producing answer schema`, not only topic labels.

Do not generate unbounded lists of possible questions. Generate bounded variants from:

```text
archetype + slot grammar + source-linked KP + mark scale
```

Short-answer extraction schema:

```yaml
ShortAnswerPattern:
  target_group_key:
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

For high-reuse families, a variant record should include:

```yaml
ShortAnswerVariant:
  family_id:
  kp_id:
  variant_type: define | list | compare | explain_mechanism | draw_label | calculate | interpret_graph | design_experiment
  likely_stem_template:
  required_mark_points:
  concise_exam_answer:
  reference_expansion:
  allowed_examples:
  source_anchor:
  confidence: High | Medium | Low
```

Internally, generate two answer layers when useful:

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

Generate mark-length skeletons only when the user explicitly asks for length variants or when a visible prompt requires them:

- 2-mark version: one-line definition or two named points.
- 4-mark version: definition plus two to three linked explanatory points.
- 6-mark version: mechanism with causal sequence and named examples.
- 8/10-mark version: full schema including comparison, diagram, data interpretation, or scenario conclusion.

Do not claim exact official mark allocation unless an official mark scheme is present.

The default student-facing short-answer report must be simplified into module logic plus point cards:

```yaml
ShortAnswerModuleSection:
  module_name: string
  module_core_logic: string
  high_yield_points: []
  point_cards: list[ShortAnswerPointCard]

ShortAnswerPointCard:
  priority: 必备 | 重点 | 补充
  point: string
  common_question_form: string
  exam_explanation_with_highlighted_keywords: string
  example_answer: string
```

Do not show mark-producing schema, required terms, optional examples, reference expansion, common omissions, task verb, confidence, evidence, or source anchor as separate student-facing fields. Bold required terms inside the explanation. Put the scoring logic into a natural `example_answer`.

## Practical / Data / Problem Outputs

Route practical protocols, problem papers, case studies, numerical assessments, spotters, graphs, figures, and worked solutions through `practical_data_problem_protocol.md`.

Practical/data/problem extraction schema:

```yaml
ProblemOperationPattern:
  target_group_key:
  exam_regime:
  year:
  question_no:
  input_type: graph | table | figure | image | protocol | case | calculation | structure | sequence | method_comparison
  required_operation:
  expected_inference:
  answer_schema: []
  controls_or_limitations: []
  follow_up_action:
  answer_key_alignment:
    provenance: official | lecturer | paper_with_answer | student | generated | unknown
    reusable_rationale:
    non_authoritative_content: []
```

Preparation output must be operation-first:

```text
input -> operation -> inference -> limitation/control -> follow-up
```

Do not output only topic names for problem/data/practical exams. If an answer key exists, extract answer logic and traps; do not treat it as independent factual authority unless verified against lecture or practical material.

## Long-Answer Project / Scenario Outputs

Use `long_answer_project` when the formal paper is non-essay but requires paragraph-style project, scenario, method-design, or research-proposal answers. This is separate from ordinary essay theory.

Long-answer project extraction schema:

```yaml
LongAnswerProjectPattern:
  target_group_key:
  exam_regime:
  year:
  question_no:
  project_context:
  named_systems_or_examples: []
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

Method-driven long-answer project archetypes:

Apply these archetypes only when exam-format parsing confirms scenario, project, method-design, readout-interpretation, or control/limitation structure. Do not transfer subject-specific systems, techniques, or recurrence claims unless supplied in the target sources.

- design purification strategy;
- choose and justify characterisation methods;
- assess folding, secondary, tertiary, or quaternary structure;
- quantify binding affinity or dimerisation affinity;
- interpret mutation effect;
- determine interaction interface;
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

When the surface system or case rotates but the operation remains stable, prepare a reusable `MethodBlock` library:

```yaml
MethodBlock:
  method_family:
  principle:
  when_to_use:
  expected_readout:
  interpretation_logic:
  required_control:
  main_limitation:
  compatible_question_parts:
  source_anchor:
```

When a user explicitly asks for a model answer or Example Essay for a project/scenario exam, route to `long_answer_example_protocol.md` and generate a `High-score example long answer`, not a generic essay. The answer must be structured by question parts, mark weights, method logic, readouts, interpretation, and controls.

Do not let old short-answer or coverage-only papers control the current long-answer project blueprint. They may support concept coverage only unless exam-format parsing proves the same regime.

## Essay / Problem-Essay Outputs

For essay and problem-essay prediction, the default prediction object is a theme-level scope, not an exact question stem. Generate a full Example Essay only when the user explicitly asks for an Example Essay, model essay, essay-style answer, essay paragraph, or similar.

Theme-level prediction means:

- predict the likely examinable theme or theme family;
- state the lecture scope that supports it;
- state whether the scope is roughly one lecture with one main theme, one lecture with two separable themes, two adjacent lectures forming one theme, or a cross-lecture synthesis;
- state the examiner operation likely to be rewarded, such as explain mechanism, compare pathways, evaluate evidence, interpret experiment, or apply to disease/scenario;
- provide optional practice angles only as practice variants, not as predicted official wording.

If a recent formal paper has an answer-one essay section with several broad options, infer option slots and theme families. Keep short-answer or fill-blank sections separate: repeated Section A terms can support factual coverage, but they must not inflate essay-theme prediction unless the same lecture block also fits Section B wording and lecture centrality.

Essay/problem-essay theme schema:

```yaml
EssayThemePrediction:
  target_group_key:
  exam_regime:
  theme_id:
  theme_title:
  lecture_scope:
    scope_type: one_lecture_one_theme | one_lecture_two_themes | two_lectures_one_theme | cross_lecture_synthesis | uncertain
    lecture_titles_or_blocks: []
    source_anchor_pages_or_slides: []
  core_examiner_operation:
  why_examinable:
    - formal_paper_pattern
    - lecture_centrality
    - learning_objective_or_summary
    - mechanism_or_evidence_density
    - coverage_gap_or_rotation_slot
  compatible_kps: []
  possible_practice_angles: []
  not_claimed:
    - exact_exam_wording
    - guaranteed_question
    - lecturer_identity_trigger
  confidence: High | Medium | Low
```

Use `Predicted essay theme` only inside the chat-only exam-analysis brief or an explicit audit/selection note. If a practice stem is useful, label it `Practice variant from predicted theme`.

For answer-one essay sections with several options, add an `EssayCoveragePlan`. The aim is to prepare enough lecture blocks for at least one high-quality answer, not to claim exact future titles or force equal-depth preparation for every source block unless requested.

When Essay Exam Prep or Example Essay Mode is triggered, follow `essay_generation_protocol.md` and package the student-facing result as `Essay_Module_Example_Essays.docx` unless the user explicitly asks for separate essay files.

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

Every essay paragraph must have internal planning metadata:

- paragraph number;
- paragraph text;
- function;
- source anchor;
- K/C/U/A/R contribution;
- why included;
- what was excluded.

Do not write slide-by-slide summaries. Each paragraph must serve the question command verb.

For the default essay-prep DOCX add-on, include module-level Example Essays, adaptation maps, and paragraph banks. Do not create a prediction workbook or put complete essays into spreadsheet rows.

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
