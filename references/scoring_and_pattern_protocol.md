# Scoring And Pattern Protocol

## Core Model

The primary prediction object is not a repeated topic. It is:

```text
fixed examiner operation + replaceable knowledge slots + reusable mark-scheme skeleton
```

Use three layers:

1. `Exam blueprint`: section structure, required/optional questions, marks, timing, question-type balance, data/figure/calculation/case-study frequency, and fixed Q-slot themes.
2. `Question archetype`: task verb + input format + cognitive operation + expected output + mark-scheme structure.
3. `Slot grammar`: replaceable variables within an archetype, such as molecule set, functional group, disease/drug/channel example, graph parameter, circuit component, assay, figure type, or calculation value.

The workflow must ask:

- Is the target exam blueprint stable?
- Which archetypes are reused?
- Which variables rotate inside those archetypes?
- Which untested or partly tested KPs can fill the same slots?
- What preparation action follows?

KP posterior/hotness is auxiliary and must not override a stronger archetype/regime signal.

## Target-Internal Comparison Rule

Only compare papers within the same normalized `target_group_key` or compatible source group. Do not use MCQ, short-answer, or content patterns from one source group to predict another source group's content.

Allowed external-example use:

- identifying a generic question-writing structure;
- borrowing an Excel layout or annotation style;
- learning how a good short-answer/MCQ explanation is phrased.

Forbidden external-example use:

- pooling KP frequency;
- claiming a topic is high-yield because it appears in an external example;
- importing another source set's distractor bank as content prediction.

## Example Contribution Transfer

External examples may transfer only operation grammar, workflow discipline, output layout logic, or QA checks. They may not transfer content, lecturer assumptions, repeated topics, or direct prediction evidence into a target source set.

Allowed example transfer:

```text
This benchmark shows that when data figures recur, predict graph-reading operation + mechanism inference + limitation.
```

Forbidden example transfer:

```text
Because one benchmark used a specific molecule, crop, disease, pathway, company, theory, or case study, a new source set should expect that same content.
```

Transferable archetypes must record the condition under which the lesson may be reused:

```yaml
TransferableArchetypePattern:
  source_example_id:
  observed_operation:
  slot_grammar:
  evidence_condition_required:
  output_action:
  forbidden_content_transfer:
```

## Exam-Regime Split

Within a target source group, split papers into separate regimes when exam format changes. Examples of regime-breaking changes include:

- MCQ + short-note becomes short-answer + case-study;
- answer-all becomes answer-one;
- closed-book timed paper becomes take-home essay;
- mark distribution or section weights change substantially.

Old-regime papers may support concept-pool coverage, but they must receive `RegimeMismatchPenalty` for current-regime predictions.

## Coverage Closure

Do not list only repeated KPs. Build an all-examinable matrix:

```text
past-paper archetypes -> slot grammar -> lecture/syllabus KP inventory -> compatible KP-slot pairs -> tested / partially tested / fresh / saturated
```

Each KP must be labelled across five task dimensions:

- `factual`: definition, list, name, identify;
- `mechanistic`: pathway, causal explanation, sequence;
- `structural`: draw, label, topology, molecular/circuit structure;
- `quantitative`: calculate, graph, table interpretation, measurement conventions;
- `comparative`: compare, rank, contrast, choose best.

This matrix is how the Skill expands from seen questions to all plausible examinable variants.

## Paper Comparability

Use:

- `formal_high`: recent formal paper with same or very similar format.
- `formal_medium`: formal paper with same target group but older or materially different constraints.
- `formal_low`: formal paper with different question style; useful for coverage only unless configured otherwise.
- `auxiliary_practice`: practice paper, mock, quiz, answer key, tutorial, exemplar, or problem sheet.
- `excluded`: wrong target group, inaccessible, unsupported, duplicate, or not relevant.

Formal past papers drive retention and examiner-pattern inference. Practice materials support coverage and answer style only unless explicitly configured.

## Primary And Secondary Knowledge Points

For every question:

```yaml
QuestionKnowledgeMapping:
  question_id:
  primary_kp_id:
  secondary_kp_ids: []
  mapping_confidence: High | Medium | Low
  evidence:
  review_queue_reason:
```

Use one primary KP for frequency/retention statistics. Use secondary KPs for answer planning, not to inflate statistics.

## Separate Metrics

Do not collapse these into one opaque score:

- Hotness: how often tested.
- Retention: how many formal years it appears in.
- Recency: whether it appears in recent papers.
- Lecture centrality: learning objectives, summaries, repeated diagrams, key experiments, lecturer emphasis.
- Question-shape fit: suitability for MCQ, short answer, essay, scenario, experiment, disease, comparison.
- Lecturer/module slot fit: whether the KP fits detected lecturer/module/question slots.

PredictionScore may be used only as explainable ranking aid:

- BlueprintFit;
- ArchetypeReuse;
- MarkSchemeReuse;
- KPRecurrence;
- Recency;
- CoverageGap;
- LectureCentrality;
- AssessmentEase;
- SaturationPenalty;
- RegimeMismatchPenalty.

A conceptual ranking formula is allowed:

```text
Score =
  BlueprintFit
+ ArchetypeReuse
+ MarkSchemeReuse
+ KPRecurrence
+ Recency
+ CoverageGap
+ LectureCentrality
+ AssessmentEase
- SaturationPenalty
- RegimeMismatchPenalty
```

For small paper sets, do not report precise numeric probabilities such as `72.4%`. Use confidence bands:

- `High confidence`: archetype likely, exact instantiation uncertain.
- `Medium confidence`: KP family likely, question form uncertain.
- `Low confidence`: possible fresh coverage, evidence weak.

## LecturerModuleSlotDetector

Test, do not assume:

1. one lecturer -> one question;
2. one module block -> one question;
3. one lecture -> one question;
4. one detailed knowledge point -> one question;
5. cross-lecture synthesis;
6. disease/application slot;
7. experiment/design slot;
8. scenario slot;
9. figure-required slot.

Output:

```yaml
SlotPatternResult:
  pattern_type:
  supporting_years: []
  contradicted_years: []
  mapped_questions: []
  confidence:
  consequence_for_prediction:
```

For essay writing, add:

```yaml
EssayLecturerIntentResult:
  likely_lecturer:
  evidence_for_lecturer: []
  contradicted_evidence: []
  likely_scope: one_kp | one_lecture | one_module | several_lectures_same_lecturer | cross_module | whole_source_set
  expected_answer_shape:
    - mechanism_detail
    - compare_contrast
    - examples_as_evidence
    - experimental_evidence
    - application_or_disease
    - synthesis
  required_lecture_examples: []
  likely_extra_reading_tolerance: low | medium | high
  confidence: High | Medium | Low
```

Do not infer lecturer preference from one question alone unless labelled `Low` confidence. Combine learning objectives, repeated examples, formal past-paper patterns, module boundaries, and question wording.

For Example Essay Mode, lecturer intent controls paragraph planning. It does not override source accuracy or question wording.

## LongAnswerProjectSlotDetector

For non-essay long-answer/project exams, test whether the current formal regime uses a project/scenario structure instead of a broad essay structure.

The detector must identify:

1. current formal regime versus old coverage-only regime;
2. whether the paper uses one or more project choices;
3. whether each project is split into weighted parts;
4. whether the biological system rotates while examiner operations recur;
5. whether purification, binding/affinity, structural determination, mutation/rational-design, folding/chaperone, enzyme activity, and biophysical-characterisation operations recur.

Output:

```yaml
LongAnswerSlotPatternResult:
  pattern_type:
  supporting_years: []
  contradicted_years: []
  mapped_questions: []
  recurrent_operations: []
  rotated_slots: []
  confidence: High | Medium | Low
  consequence_for_answer_generation:
```

When the recent formal regime is project/scenario-based, older short-answer, take-home, or different-format papers may inform the concept pool only. They must not control current answer style, paragraph structure, or predicted project-question structure.

For method-driven project/scenario papers, consequence for answer generation should normally be:

```text
Generate a compact experimental argument: question goal -> lecture method principle -> scenario-specific application -> expected readout -> interpretation -> limitation/control.
```

Do not write separate lecturer blocks unless the question itself asks for that structure. Recent project/scenario questions may combine several lecturers' material inside one answer.

## Archetype Registry Schema

```yaml
QuestionArchetype:
  archetype_id:
  target_group_key:
  exam_regime:
  question_family: mcq | short_answer | essay | case_study | data_problem | long_answer_project
  task_verbs: []
  input_format:
  cognitive_operation:
  expected_output:
  mark_scheme_structure:
  compatible_kp_families: []
  slots: []
  derived_from_external_example:
  transferable_rule:
  non_transferable_content: []
  format_match_required:
  seen_in:
    - source_group:
      year:
      question_no:
  saturation: fresh | partially_tested | saturated | unknown
  confidence: High | Medium | Low
```

An archetype can be stronger evidence than a repeated isolated KP when the operation, slot grammar, and answer skeleton recur with rotated examples.

## Review Queue

Place mappings or predictions into QA/review when:

- OCR or parsing is weak;
- source mapping is ambiguous;
- one question could map to multiple primary KPs;
- a formal paper has changed format;
- lecturer ownership is unclear;
- lecturer intent is inferred from weak evidence;
- an essay paragraph plan is missing or does not preserve lecture logic;
- a long-answer project paragraph plan is missing;
- a long-answer project answer lacks method principle, scenario application, readout, interpretation, or control/limitation;
- a project/scenario answer has been written as a generic essay;
- a comparison essay lacks shared comparison axes;
- an answer is not found in supplied lecture material;
- a citation is unverified;
- prediction confidence is low.
