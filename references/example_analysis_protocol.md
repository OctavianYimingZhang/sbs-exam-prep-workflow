# Example Analysis Protocol

This protocol defines how the Skill learns from examples without turning examples into content triggers.

Examples include:

- user-uploaded model essays;
- screenshots of writing advice;
- ChatGPT shared conversations;
- handwritten or annotated answers;
- non-biological science essays;
- existing generated workbooks or DOCX essays;
- benchmark fixtures;
- answer keys and reasoned solutions;
- formative feedback and marking criteria.

## Core Rule

Examples can teach structure, language, diagnosis, and QA. They cannot supply factual claims, predicted topics, lecturer preferences, citations, or source-set identity.

## ExampleContribution Record

Every reusable lesson should be stored conceptually as:

```yaml
ExampleContribution:
  example_id:
  source_type:
  observed_problem:
  transferable_rule:
  structural_trigger:
  applies_to:
  non_transferable_content:
  affected_protocols:
  validation_check:
  confidence: High | Medium | Low
```

## LanguageDelta Record

Language-only improvements should be stored as:

```yaml
LanguageDelta:
  delta_id:
  bad_pattern:
  improved_pattern:
  reasoning:
  applies_to:
  linter_signal:
  severity: high | medium | low
```

## Analysis Steps

1. Classify the example source and trust boundary.
2. Extract the writing or workflow failure without copying factual content.
3. Convert the failure into a transferable rule.
4. Assign the rule to the relevant protocol or linter.
5. Add a validation check that can fail future outputs.
6. Record non-transferable content explicitly.

## Language Delta Scope

Scan external essays, formative feedback, answer-style exemplars, reasoned answer keys, and generated outputs for language deltas.

Do not derive language deltas from formal past-paper pages, formal papers with answer appendices, lecture slides, practical protocols, reading lists, or marking criteria. Those sources can teach format, method, evidence role, or assessment structure, but page numbers and question instructions from them are not student-answer prose.

## Common Transferable Lessons

- Compress repetition without removing mechanism.
- Open paragraphs with claim or problem.
- Explain examples as evidence for a broader argument.
- Convert evidence-heavy examples into evidence, mechanism, interpretation, and limitation.
- Remove lecture-route narration and exam-guidance phrasing from final essay prose.
- Calibrate citation strength so support or implication is not written as single-cause proof.
- State the debate before comparing models.
- Separate old-regime evidence from current-regime prediction.
- Treat answer keys as answer-schema evidence, not independent factual authority.
- Treat practical protocols as method/readout/control evidence.
- Use formative feedback as writing and marking guidance, not prediction evidence.

## Hard Negatives

Do not:

- infer a target topic because an example used that topic;
- copy a citation from an example;
- write source-set-specific course names into production logic;
- merge official answers, student answers, and generated answers into one trust class;
- treat a model answer as proof that the same question will recur.
