# Input Processing Protocol

## FileRole Enum

Classify every file before analysis:

- `lecture_slide`
- `lecture_note`
- `annotated_lecture_slide`
- `formal_past_paper`
- `practice_paper`
- `mock_exam`
- `answer_key`
- `exemplar_answer`
- `exemplar_image`
- `marking_criteria`
- `essay_guidance`
- `extra_reading_book`
- `extra_reading_chapter`
- `citation_original_source`
- `citation_reference_list`
- `docx_format_reference`
- `source_policy`
- `output_protocol`
- `helper_script`
- `unsupported_binary`
- `unknown`

Each file record must include:

- file path;
- normalized `unit_key`;
- unit code;
- unit name;
- year if detectable;
- exam regime if detectable;
- source trust level;
- extraction status;
- allowed evidence use.

Student handwritten annotations on slides may be used as interpretation hints, but must not be treated as authoritative course facts unless supported by slide text, official notes, or reliable sources.

## Source Trust Levels

- `official_course`: lecture slides, official notes, official past papers, official marking criteria, official exam guidance.
- `course_adjacent`: lecturer-provided practice, mocks, answer keys, exemplars, tutorial material.
- `student_or_unknown`: student notes, downloaded material with unclear provenance, unclear file origin.
- `external_verified`: peer-reviewed, textbook, DOI/PubMed/publisher/official sources verified during the run.
- `unsupported`: unreadable or unsupported content.

## Evidence Use

- `factual_course_content`
- `formal_prediction_evidence`
- `coverage_evidence_only`
- `answer_style_only`
- `format_rule`
- `extra_reading`
- `lecture_slide_core`
- `lecture_slide_citation_original`
- `docx_format_reference`
- `excluded`

## AnalysisContext

Every source must also be classified by `AnalysisContext` before it is used downstream.

```yaml
AnalysisContext:
  target_unit_current_regime:
    meaning: same unit, current formal evidence; allowed for blueprint and prediction
  target_unit_old_or_different_regime:
    meaning: same unit but old/different format; allowed for concept coverage and answer schema only
  target_unit_auxiliary:
    meaning: practice/mock/tutorial/answer key from same unit; allowed for coverage and style depending on role
  cross_unit_example:
    meaning: other unit material; transferable workflow logic only
  style_exemplar:
    meaning: exemplar answer/image; style/structure/density only unless factual claims are verified
  layout_exemplar:
    meaning: visual formatting example only
  benchmark_fixture:
    meaning: regression test case only
  unsupported_or_unreadable:
    meaning: do not use for factual or predictive claims
```

Hard rule:

```text
Only `target_unit_current_regime` may directly control current blueprint prediction.
Only target-unit lecture slides, official notes, and verified official materials may directly control factual content.
Cross-unit examples must be converted into transferable workflow contributions, not content evidence.
```

## AllowedUseMatrix

| Analysis Context | Factual content | Prediction blueprint | Coverage | Style | Layout | Regression |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `target_unit_current_regime` | yes | yes | yes | yes | yes | no |
| `target_unit_old_or_different_regime` | yes if lecture/official | no unless comparability is proven | yes | limited | no | no |
| `target_unit_auxiliary` | limited | no unless official says representative | yes | yes | no | no |
| `cross_unit_example` | no | no | no | principle only | possible | no |
| `style_exemplar` | no unless verified | no | no | yes | no | no |
| `layout_exemplar` | no | no | no | no | yes | no |
| `benchmark_fixture` | no | no | no | no | no | yes |
| `unsupported_or_unreadable` | no | no | no | no | no | no |

## UnitExampleContribution Schema

Every non-target Unit example used by a protocol or benchmark must be represented as a contribution object:

```yaml
UnitExampleContribution:
  source_unit:
  source_materials:
    - lecture_slides
    - lecture_notes
    - formal_past_papers
    - practice_materials
    - marking_guidance
    - exemplar_answers
    - handwritten_or_image_examples
  observed_unit_pattern:
  generic_skill_contribution:
  transferable_rule:
  future_unit_diagnostic_questions:
    - question
  non_transferable_content:
    - topic/content/lecturer/year detail that must not be reused
  affected_workflows:
    - source_inventory
    - unit_grouping_regime_split
    - question_type_gate
    - exam_format_diagnosis
    - lecture_segmentation
    - knowledge_point_optimisation
    - archetype_mapping
    - past_paper_statistics
    - pattern_detection
    - question_type_outputs
    - example_essay_mode
    - long_answer_project_mode
    - extra_reading_and_exemplars
    - excel_generation
    - qa
    - cross_subject_regression
  anti_patterns_prevented:
    - pooling content across units
  validation_checks:
    - check
```

## Unit Key And Regime Split

All question-pattern inference must be unit-internal. Normalize every filename before comparison:

1. remove year/date tokens;
2. remove terms such as `mock`, `practice`, `with answers`, `answer key`, `May 29`, `combined`, `HCI copy`, and version suffixes;
3. collapse whitespace and punctuation;
4. retain the normalized course/unit name as `unit_key`.

Examples:

- `Chemistry for Bioscientists 2`
- `Membrane Excitability`
- `Clinical Drug Development`
- `Cell Membrane Structure and Function`
- `BIOL21332 Motor Systems`

Never use content from one `unit_key` to predict the content of another unit. Cross-unit examples may be used only as UnitExampleContribution records that teach reusable workflow logic, output structure, QA checks, or evidence-handling discipline.

Within the same unit, split formal papers into `exam_regime` groups when any of these change materially:

- section structure;
- answer-all vs answer-one/choose-one rule;
- timing or submission mode;
- mark weights;
- MCQ/short-answer/essay/case-study balance;
- data/figure/calculation requirements.

Old-regime papers may support concept coverage and possible slot fillers, but they must not be averaged into current-regime blueprint or archetype recurrence.

## Extraction Rules

- PDF: extract page-by-page text; record image count and warn that diagram/image text may need visual inspection.
- PPTX: extract slide XML text and notes XML when possible; record that diagrams and embedded images may not be text-extracted.
- DOCX: extract paragraphs and table text.
- TXT/Markdown/YAML/Python: read as text.
- Images: mark as image evidence; inspect manually or with OCR when it affects the answer.
- Image exemplars: classify as `exemplar_image` when context indicates handwritten essays, model answers, example answers, or essay drafts. Evidence use is `answer_style_only`; status must include visual-inspection limits. Do not OCR repeatedly by default.
- A user-uploaded textbook, book chapter, monograph, or long PDF supplied as additional reading must be classified as `extra_reading_book` unless it is clearly a lecture slide or past paper.
- A standalone chapter or chapter extract supplied as additional reading must be classified as `extra_reading_chapter`.
- A PDF or paper resolved from a citation on a lecture slide must be classified as `citation_original_source`.
- A bibliography/reference-list file supplied to resolve slide citations may be classified as `citation_reference_list`.
- A user-uploaded formatting PDF or screenshot must be classified as `docx_format_reference` and used only for layout/style, not biological content.
- Essay style examples must be classified as `style_exemplar` or `exemplar_answer` and used only for paragraph structure, density, and tone unless factual claims are independently verified from target-unit materials.
- Unsupported files: never infer hidden content.

### Extra Reading Book Extraction

For Extra Reading Books:

- extract table of contents if available;
- extract chapter headings;
- extract section headings;
- index searchable keywords;
- map chapters to lecture KPs using lecture terms, gene/protein/pathway names, diseases, methods, model organisms, and essay question terms;
- read only relevant chapters/sections before inserting yellow-highlighted content into Example Essays.

### Lecture-Slide Citation Extraction

For lecture-slide citations:

- extract citations from slide text, notes, reference slides, footers, and figure captions;
- if citations appear only inside slide images, perform targeted OCR or visual inspection on relevant slides;
- parse author-year, DOI, PMID, title fragments, journal names, and reference-list entries;
- classify resolved/read source files as `citation_original_source`;
- do not use source-derived content until the cited original source has been resolved and read.

## ExamFormat Fields

For each formal paper or guidance source, parse:

- unit_code;
- year;
- duration;
- sections;
- answer_all_or_answer_one;
- question_count_by_section;
- mark_weight_by_section;
- page_limit;
- word_limit;
- character_limit;
- figure_rule;
- citation_rule;
- calculator_rule;
- answer_book_or_blackboard;
- formatting_penalty;
- late_penalty.

Different year constraints directly change answer strategy; do not merge years without recording differences.

## KnowledgePoint Schema

```yaml
KnowledgePoint:
  kp_id:
  lecture_id:
  module_id:
  lecturer:
  title:
  concept_type: mechanism | pathway | experiment | disease | comparison | definition | method | figure | model_system | controversy_or_limitation
  source_anchor:
    file:
    slide_or_page_range:
  examinability: high | medium | low
  likely_question_types: []
  prerequisite_kps: []
  linked_kps: []
  essay_style_paragraph:
  mcq_statement_candidates: []
  short_answer_possible_questions: []
  essay_question_candidates: []
  compatible_archetypes: []
  essay_function:
    - thesis_support
    - mechanism_paragraph
    - comparison_axis
    - example_evidence
    - cross_module_link
    - optional_extra_detail
  mechanism_chain:
    condition:
    regulator_or_sensor:
    molecular_action:
    output_change:
    biological_consequence:
  lecturer_emphasis:
    learning_objective: true/false
    summary_slide: true/false
    repeated_example: true/false
    named_as_key_point: true/false
  essay_priority: must_use | useful | optional | exclude
  paragraph_fit:
    possible_topic_sentence:
    possible_link_back_to_question:
  task_dimensions:
    factual:
    mechanistic:
    structural:
    quantitative:
    comparative:
```

Do not split by every slide. Split by examinable causal unit. A valid KP should work as an MCQ concept, a short-answer mark cluster, an essay paragraph, or one component of an essay plan.

For essay-capable KPs, do not treat all slide facts equally. Prioritise the facts that can form a causal paragraph:

```text
condition or biological problem -> regulator/sensor/molecular feature -> molecular action -> output change -> biological consequence
```

## Lecture-Order Coverage

For student-facing visual workbooks, analysis must proceed from the first slide/page to the last slide/page in source order.

Do not:

- analyse only high-yield slides;
- skip middle lecture sections without a QA flag;
- reorder KPs by predicted importance in the main student-facing workbook;
- merge several unrelated mechanisms into one huge KP;
- split one mechanism/evidence unit into isolated slide fragments.

Allowed:

- group several consecutive slides/pages into one KP when they form one mechanism, process chain, experimental-evidence block, data-operation block, or essay paragraph unit;
- mark a block low examinability, but still preserve its position;
- place detailed evidence in diagnostics or an evidence workbook while keeping the student sheet clean.
