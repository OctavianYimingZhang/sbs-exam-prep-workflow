# Past Paper Prediction Protocol

Past-paper analysis is not a guessing workflow. It is a constrained preparation-allocation workflow:

```text
past papers -> current exam regime -> question-level records -> archetype registry -> slot grammar -> KP compatibility -> confidence band -> prep artifact
```

The prediction target is a question family and preparation action, not exact future wording.

## Theoretical Model

Each question should be encoded as a record:

```text
q = (topic, subtopic, format, command verb, representation, marks, source block)
```

Then group questions by family:

```text
fixed examiner operation + replaceable slot grammar + reusable mark-scheme skeleton
```

For internal ranking, use separate explainable metrics:

```text
InternalScore =
  2.0 * BlueprintFit
+ 2.0 * ArchetypeReuse
+ 1.5 * MarkSchemeReuse
+ 1.0 * KPRecurrence
+ 1.0 * Recency
+ 1.0 * LectureCentrality
+ 0.8 * CoverageGap
+ 0.7 * AssessmentEase
- 1.2 * SaturationPenalty
- 2.0 * RegimeMismatchPenalty
```

Do not expose fake precision to students. For small paper sets, output confidence bands:

- `High`: stable current regime, repeated archetype, compatible lecture centrality, no recent contradiction.
- `Medium`: recurring family or KP, but question form or regime fit is uncertain.
- `Low`: plausible fresh coverage, weak past-paper evidence, or old-regime support only.

Student-facing priority should consider expected value, not just frequency:

```text
priority = probability_band * mark_value * student_weakness * transferability / prep_time
```

When student weakness or prep time is unknown, omit those terms and state that the ranking is evidence-only.

## Question-Level Extraction

Past papers must be converted into `PastPaperQuestion` records before statistical or archetype inference.

Required fields:

```yaml
PastPaperQuestion:
  source_file:
  target_group_key:
  year:
  paper_id:
  section:
  question_no:
  subquestion_no:
  raw_stem:
  marks:
  answer_rule:
  question_type:
  command_verbs: []
  input_format:
  negative_marking:
    present:
    correct_value:
    wrong_value:
    unanswered_value:
  candidate_options:
    count:
    option_texts: []
  extracted_confidence:
  review_flag:
```

If extraction is weak, emit `review_flag` rather than inventing missing sections, marks, options, answers, or diagrams.

## Question-Type Targets

| Question type | Correct prediction object | Incorrect prediction object |
| --- | --- | --- |
| MCQ | concept discriminators, traps, calculation/recognition modes, scoring policy | exact option text or official answer without answer key |
| Fill blank | term bank, cloze variants, exact wording anchors from source | hidden official blanks not visible in sources |
| Short answer | bounded question-family variants and mark-producing schemas | all possible questions |
| Long-answer project/problem | transferable method/readout/control blocks | exact rotating scenario |
| Essay/problem essay | lecture block, command verb, argument skeleton, evidence bank | exact title or guaranteed stem |

## MCQ Scoring Policy

For MCQ regimes, extract scoring rules when visible:

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

If unanswered value is zero, correct value is `c`, and wrong penalty magnitude is `d`, the internal expected-value threshold is:

```text
p > d / (c + d)
```

Examples:

- 4-option single-best with `+1` and `-1/3`: threshold `0.25`.
- Statement marking with `+1/3` for correct true and `-1` for wrong true: threshold `0.75`.

Do not output official answer values unless the paper or answer key states them.

## Short-Answer Variant Space

Short-answer preparation should generate bounded variants, not infinite questions:

```text
archetype + slot grammar + lecture KP + mark scale -> ShortAnswerVariant
```

Variant types:

- define;
- list;
- compare;
- explain mechanism;
- draw/label;
- calculate;
- interpret graph;
- design experiment.

Each variant must have a source-linked KP, required mark points, concise exam answer, reference expansion, allowed examples, and confidence band.

## Long-Answer Method Blocks

For scenario/project/problem long answers, prepare reusable method blocks:

```text
question goal -> method choice -> readout -> interpretation -> control -> limitation
```

The biological, chemical, clinical, engineering, or data scenario may rotate. The stable object is the operation.

Method blocks should record:

- method family;
- principle;
- when to use;
- expected readout;
- interpretation logic;
- required control;
- main limitation;
- compatible question parts;
- source anchor.

## Essay Coverage Plan

For essay sections with several options where the student answers one, optimise coverage rather than pretending exact titles can be known.

Use:

```yaml
EssayCoveragePlan:
  lecture_scope_type: one_lecture_one_theme | one_lecture_two_themes | two_lectures_one_theme | cross_lecture_synthesis | uncertain
  likely_command_verbs: []
  argument_skeleton:
  paragraph_claims: []
  evidence_bank: []
  diagram_bank: []
  comparison_axes: []
  limitations: []
  coverage_role: core | backup | optional
  confidence: High | Medium | Low
```

If a section presents several essay options and the student answers one, prepare enough lecture blocks to make at least one high-quality answer likely. Do not force equal-depth preparation for every possible block unless the user asks for exhaustive coverage.

## Lecturer Style

Lecturer or source-block style is a weak auxiliary variable.

It cannot raise confidence above `Medium` unless all conditions are met:

1. same current exam regime;
2. repeated over at least two formal papers;
3. aligned with lecture objectives, summaries, or central lecture blocks;
4. not contradicted by recent papers.

Never infer lecturer preference from one question alone unless labelled `Low`.

## Hard Failures

Fail or rewrite prediction output when it contains:

- `this exact question will appear`;
- `guaranteed`;
- precise probabilities from a small paper set, such as `72.4%`;
- lecturer preference inferred from one question without a `Low` label;
- external example content used as target prediction;
- old-regime paper controlling current-regime blueprint;
- short-answer variants with no source-linked KP;
- MCQ answer claimed official without an answer key;
- essay stem presented as official instead of a practice variant;
- generated `all possible questions` without bounded slot grammar.
