# Student-Facing Output Policy

The Skill may use source anchors, evidence claims, confidence bands, examiner-operation labels, recurrence, lecture centrality, scoring logic, and source coverage internally. Student-facing outputs must not expose that audit reasoning unless the user explicitly asks for an audit package.

Student-facing exam-prep outputs must be rewritten as directly usable revision content:

```text
internal reasoning: evidence -> operation -> priority -> output type
student output: priority -> point -> explanation -> exam-use answer or walkthrough
```

## Forbidden Visible Fields

Do not show these fields in ordinary student-facing reports:

- source anchor;
- evidence rationale;
- confidence;
- recurrence count;
- lecture centrality;
- regime match;
- why high-yield;
- examiner operation;
- discriminator axis;
- task verb;
- reference expansion;
- common omissions;
- evidence limit;
- past-paper year mapping;
- prediction score.

Canonical forbidden field IDs:

```text
source_anchor
confidence
evidence
examiner_operation
discriminator_axis
practice_mcq
answer_key
contrast_table
separate_trap_bank
mark_producing_schema
reference_expansion
```

These may appear only in internal QA, an explicit audit package, or a separate evidence workbook requested by the user.

## Allowed Priority Labels

Use only these visible priority labels when priority is useful:

- `必备`;
- `重点`;
- `补充`.

Do not explain why a point is `必备` by exposing recurrence, confidence, or source-scoring logic. Convert the reason into useful content: what to know, how it is tested, and what trap to avoid.

## MCQ Student Contract

MCQ reports are point-card reports. They must not contain practice questions, answer keys, contrast tables, or a separate trap bank by default.

Visible MCQ Point Card:

```yaml
MCQStudentPointCard:
  priority: 必备 | 重点 | 补充
  point: string
  knowledge_explanation: string
  how_exam_tests_it: string
  common_traps: list[string]
  must_remember: string
```

Forbidden by default:

- practice MCQ;
- answer key;
- contrast table;
- separate trap bank;
- source anchor;
- confidence;
- evidence;
- examiner operation;
- discriminator axis.

If the user explicitly asks for practice questions, generate a separate practice pack rather than adding them into the MCQ high-yield report.

## Short-Answer Student Contract

Short-answer reports have two levels:

- module-level logic, so the student understands how related points connect;
- point-level cards, so the student can write a direct answer.

Visible module section:

```yaml
ShortAnswerModuleSection:
  module_name: string
  module_core_logic: string
  high_yield_points: list[string]
  point_cards: list[ShortAnswerPointCard]
```

Visible point card:

```yaml
ShortAnswerPointCard:
  priority: 必备 | 重点 | 补充
  point: string
  common_question_form: string
  exam_explanation_with_highlighted_keywords: string
  example_answer: string
```

Do not display these as separate fields:

- mark-producing schema;
- required terms;
- optional examples;
- reference expansion;
- common omissions;
- task verb;
- confidence;
- source anchor.

Required terms should be bolded inside the explanation. Mark logic should be absorbed into the `Example Answer` as a natural paragraph, not exposed as a scoring table. Do not split the student answer mechanically into 2/4/6/8-mark versions unless the user specifically asks for that format.

## Long-Answer Student Contract

Long-answer outputs are exam-response playbooks, not general study coaching.

Visible structure:

```yaml
LongAnswerStudentItem:
  topic: string
  core_exam_problem: string
  likely_question_forms: list[string]
  answer_order: list[string]
  reusable_answer_blocks:
    mechanism_block: string
    method_or_readout_block: string
    interpretation_block: string
    control_or_limitation_block: string
  example_answer: string
  adaptation_rules: list[string]
  must_include: list[string]
  avoid_overwriting: list[string]
```

Do not show evidence, source, confidence, recurrence, or why the operation is likely.

## Essay Student Contract

Essay outputs are module-level packs only when the user explicitly asks for essay preparation or complete Example Essays.

Visible structure:

```yaml
EssayModulePack:
  module_name: string
  essay_title: string
  core_thesis: string
  full_example_essay: string
  adaptation_map: list[string]
  key_paragraph_bank: list[string]
  essential_terms: list[string]
  likely_stem_variants: list[string]
```

The useful student-facing pair is:

```text
Full Example Essay + how to adapt it to specific essay questions
```

Do not generate Essay Module Packs as the default lecture-review product.
