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

## Example Learning Rule

Examples are not templates to copy. Every example must first be analysed into an `ExampleReviewRecord`; only the stripped, generic, condition-based lesson may be promoted into protocols, schemas, scripts, or regression fixtures.

No example-derived rule may enter production unless it has:

- what worked;
- why it worked;
- what failed, or the explicit statement `no failure observed`;
- why it failed, or the explicit statement `not applicable because no failure was observed`;
- non-transferable content;
- one transferable principle;
- one anti-overfit rule;
- a destination;
- one validation check;
- one regression fixture or fixture update.

## ExampleReviewRecord

Every reusable lesson must be stored conceptually as:

```yaml
ExampleReviewRecord:
  example_id:
  source_role:
  example_scope:
  what_worked:
  why_it_worked:
  what_failed:
  why_it_failed:
  transferable_principle:
  non_transferable_content:
  anti_overfit_rule:
  affected_protocols:
  affected_scripts:
  validation_check:
  regression_fixture:
  promotion_status: candidate | accepted | rejected | blocked
  confidence: high | medium | low
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
2. Write one review record per example, including what worked and what failed.
3. Strip target-specific content, names, dates, citations, question stems, headings, and topic details into `non_transferable_content`.
4. Convert only the remaining condition into a transferable principle.
5. Assign the rule to the relevant protocol, schema, script, linter, or regression fixture.
6. Add a validation check that can fail future outputs.
7. Run the rule-promotion gate before treating the lesson as production behavior.

## Example Learning Pipeline

```text
example_inventory
-> example_review_ledger
-> transferable_rule_synthesis
-> rule_promotion_gate
-> example_transfer_linter
-> regression_fixture_update
```

## Rule Promotion Gate

Before promotion, the Skill must:

1. Identify the source feature or output failure the example demonstrates.
2. State whether the example is good, bad, or mixed.
3. Explain why the example worked or failed.
4. Remove source-specific content.
5. Rewrite the lesson as a generic condition-based rule.
6. Add a positive regression.
7. Add a negative regression.
8. Add a linter or schema check where practical.
9. Confirm the promoted rule does not contain the example identity.

Fail the gate if the rule says or implies:

- copy this structure;
- make future output like this example;
- preserve the same module list;
- use the same topic labels;
- transfer target-specific content;
- turn a benchmark fixture into general production logic.

## No Direct Example-To-Skill Rule

Production rules must not contain the example's course name, lecturer name, target title, module-specific topic name, named drug, named gene, named organism, exact heading, fixture ID, or target-specific required module list.

Example-specific checks may live in regression fixtures. Production linters and schemas must operate on generic source features such as:

- official definitions;
- contrast pairs;
- criteria, features, stages, or classes lists;
- named teaching examples;
- `Why X?` source blocks;
- diagrams, tables, equations, graphs, workflows, and calculations;
- method workflows;
- graph or data interpretation operations.

## Generalised Coverage Rule From Examples

When examples expose missing lecture-note density, the transferable rule is not the example's topic list. The general rule is that each source heading, official definition, contrast pair, criteria list, named example, diagram, equation, graph, calculation, method workflow, and summary point must be captured as an atomic knowledge item before exam overlay changes priority, order, or density.

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
