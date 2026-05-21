# Cross-Subject Regression Protocol

This file contains benchmark fixtures used only to test generic Skill behaviour. The named Units below must never trigger production logic. Each benchmark contributes UnitExampleContribution records and pass/fail tests.

Cross-subject regression does not ask whether the Skill can simply redo known Units. It asks whether those Units collectively improve the general workflow for future Units.

Hard rule:

```text
Target Unit evidence = factual content + direct prediction evidence.
Same Unit old/different-regime evidence = coverage/schema evidence only unless comparability is proven.
Cross Unit examples = transferable workflow lessons only.
Style/layout exemplars = wording, structure, density, formatting, and answer organisation only.
Benchmark fixtures = tests only; never production rules.
```

## UnitExampleContribution Schema

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
    - kp_essay_synthesis_lint
    - qa
    - cross_subject_regression
  anti_patterns_prevented:
    - pooling content across units
  validation_checks:
    - check
```

When a generated workbook is supplied to the regression checker, run `scripts/essay_style_linter.py` and include failures in the regression result. Regression should validate final workbook language quality, not only source availability, unit separation, and exam-regime logic.

When an Example Essay DOCX directory is supplied to the regression checker, validate:

- each Example Essay is a separate `.docx`;
- `example_essay_manifest.json` exists;
- `example_essay_source_audit.json` exists;
- no generated Example Essay exists only as an Excel row;
- DOCX format lint passes for A4, 2.5 cm margins, Arial 10 pt body, 1.5 line spacing, 0 pt paragraph spacing, justified body, centered title, and left-aligned subtitles/headings;
- yellow-highlighted runs map to uploaded Extra Reading Book chapter/section anchors;
- green-highlighted runs map to read lecture-slide citation originals and include author-year in-text citation;
- every body paragraph has lecture-slide anchors.

## Unit Example Contribution Matrix

### Motor Systems Contribution

```yaml
source_unit: Motor Systems
source_materials:
  - lecture_slides
  - formal_past_papers
  - benchmark_fixture
observed_unit_pattern:
  - older papers contain short-answer/problem-style answer-all evidence
  - recent papers use answer-one essay/problem-essay style
  - lecture content must be preserved visually in source order
  - final workbook works best when slide images, explanation, and predicted practice prompts are horizontally aligned
generic_skill_contribution:
  - teaches exam-regime split when older papers are structurally different from recent formal papers
  - teaches that old papers may support concept coverage but must not drive current essay blueprint
  - teaches visual workbook alignment: locator -> original slide image -> student explanation -> exam-facing prediction
  - teaches that application/disease/scenario/circuit topics can be treated as rotating slots inside recurring examiner operations
transferable_rule:
  - For any future Unit, first compare answer rules, section structure, timing, mark weights, and question family across years.
  - If older papers are short-answer/problem-style but recent papers are answer-one essay/problem-essay, use older papers only for coverage and concept-bank evidence.
  - Keep student-facing visual output slide-aligned and source-order-preserving.
  - Treat disease/application/scenario examples as slot fillers, not as proof that the exact topic will recur.
future_unit_diagnostic_questions:
  - Did the answer rule change from answer-all to answer-one?
  - Did the dominant question type change?
  - Are old papers useful for coverage but unsafe for current blueprint prediction?
  - Does the Unit need visual slide-image alignment to make explanation usable?
non_transferable_content:
  - MND/ALS
  - Brain Machine Interface
  - C9orf72
  - basal ganglia / Parkinson's
  - superior colliculus
  - vestibular scenario
  - any Motor-specific lecture topic recurrence
affected_workflows:
  - unit_grouping_regime_split
  - exam_format_diagnosis
  - archetype_mapping
  - past_paper_statistics
  - pattern_detection
  - question_type_outputs
  - excel_generation
  - cross_subject_regression
anti_patterns_prevented:
  - using old short-answer papers as direct current essay blueprint
  - treating topic recurrence as more important than exam-format comparability
  - outputting a non-visual evidence-heavy workbook instead of the requested visual student workbook
validation_checks:
  - old and current regimes are labelled separately
  - current-regime predictions cite current-regime evidence only
  - workbook image blocks preserve aspect ratio and lecture order
```

### Developmental Biology Contribution

```yaml
source_unit: Principles of Developmental Biology
source_materials:
  - lecture_slides
  - formal_past_papers
  - handwritten_or_image_examples
observed_unit_pattern:
  - current papers have Section A short conceptual prompts and Section B major essay prompts
  - old papers have different Section A answer-all structure
  - high-quality answers require mechanism + experimental evidence + developmental consequence
  - many topics require GOF/LOF reasoning, model-system comparison, and evidence-based inference
generic_skill_contribution:
  - teaches that KP segmentation should be by examinable causal unit, not slide count
  - teaches the general KP pattern: mechanism + evidence + consequence
  - teaches Section A and Section B separation inside the same Unit
  - teaches that old formal papers may still provide short-answer schemas without controlling current blueprint
  - teaches evidence-based essay planning rather than topic-list prediction
transferable_rule:
  - For any future mechanism-heavy Unit, build KPs around mechanism + evidence + consequence.
  - If a paper has multiple sections with different answer styles, produce separate prep logic for each section.
  - If older papers use answer-all short questions but recent papers use essay or major-answer format, use older papers only for coverage and mark-schema insight.
  - When questions ask for gene/function/pathway logic, identify whether the examiner operation is evidence interpretation, causal mechanism, comparison, or experimental inference.
future_unit_diagnostic_questions:
  - Does the Unit require experimental evidence to support mechanism claims?
  - Are short conceptual prompts and major essay prompts mixed in the current paper?
  - Are older papers structurally different from current papers?
  - Should a KP be split because it contains several mechanisms, or merged because one mechanism spans several slides?
non_transferable_content:
  - Bicoid
  - Hox
  - Drosophila segmentation
  - somite clock
  - phyllotaxy
  - plant embryo regulators
  - any Developmental Biology topic as content prediction for another Unit
affected_workflows:
  - unit_grouping_regime_split
  - question_type_gate
  - exam_format_diagnosis
  - knowledge_point_optimisation
  - archetype_mapping
  - question_type_outputs
  - example_essay_mode
  - cross_subject_regression
anti_patterns_prevented:
  - splitting one mechanism/evidence unit into isolated slide fragments
  - merging a whole topic area into one huge KP
  - treating Section A and Section B as the same question type
  - using old-regime answer-all questions as current blueprint evidence
validation_checks:
  - Section A and Section B outputs are distinguished
  - mechanism-heavy KPs contain mechanism, evidence, and consequence
  - old-regime questions are labelled coverage/schema only
```

### Plant Biology Contribution

```yaml
source_unit: Plants for the Future
source_materials:
  - lecture_slides
  - formal_past_papers
observed_unit_pattern:
  - current papers are mixed-format
  - Section A is mini-essay
  - Section B is problem/data interpretation
  - problem questions require graph reading, mutant/transgenic phenotype inference, field-trial design, and mechanism-to-application reasoning
  - embedded figures may require visual inspection before exact values can be claimed
generic_skill_contribution:
  - teaches that mixed-format Units must not be forced into pure essay mode
  - teaches how to route data/problem questions separately from mini-essay prompts
  - teaches data-operation archetype extraction: graph reading, phenotype inference, experimental recommendation, limitation, and conclusion control
  - teaches visual workbook adaptation where the far-right area changes by question type
  - teaches that image-only graph values must not be invented from weak extraction
transferable_rule:
  - For any future Unit with a data/problem section, build data-operation archetypes rather than essay-only predictions.
  - For any mixed-format Unit, keep one student-facing workbook but adapt the prediction area per question type.
  - If figures, graphs, or tables are image-only, flag visual inspection before claiming exact values.
  - Treat exam-only gene names, variables, or case details as exam contexts unless lecture evidence confirms them.
future_unit_diagnostic_questions:
  - Does the current paper contain both essay and data/problem sections?
  - Does one section require interpretation of figures, graphs, tables, mutants, or experimental conditions?
  - Are exact data values visible in extracted text, or only in images?
  - Should the far-right workbook area show data-operation logic instead of essay prompts?
non_transferable_content:
  - ABA
  - GA
  - FLC
  - golden rice
  - barley domestication genes
  - leaf angle
  - crop-density examples
  - any Plant-specific topic recurrence
affected_workflows:
  - question_type_gate
  - exam_format_diagnosis
  - archetype_mapping
  - question_type_outputs
  - excel_generation
  - qa
  - cross_subject_regression
anti_patterns_prevented:
  - treating a mixed mini-essay + data/problem Unit as pure essay
  - outputting only topic names without data-operation logic
  - inventing graph values from image-only figures
  - applying one year's word limit to later years without evidence
validation_checks:
  - data/problem outputs include input, operation, inference, limitation, and follow-up
  - image-only values are flagged before use
  - mini-essay and problem/data prompts are separate
```

### Immunology Contribution

```yaml
source_unit: Immunology
source_materials:
  - lecture_slides
  - formal_past_papers
observed_unit_pattern:
  - old papers are answer-all concise short-answer papers
  - recent papers shift toward essay / Section B answer-one structure
  - current/latest paper may contain Section A answer-all plus Section B answer-one
  - good KPs are immune process chains, not isolated vocabulary
  - questions often use pathogen scenario, clinical application, cell-type comparison, or defect-to-phenotype reasoning
generic_skill_contribution:
  - teaches regime-shift handling when old short-answer papers and current essay/Section B papers coexist
  - teaches process-chain KP segmentation
  - teaches scenario-slot analysis where context may rotate while operation stays stable
  - teaches missing-paper QA when a referenced section is absent
  - teaches that old short-answer papers can support concise mark schemas without controlling current essay blueprint
transferable_rule:
  - For any future Unit with old concise answer-all papers and newer essay/Section B papers, separate evidence by regime.
  - Build KPs as process chains: stimulus/input -> actors -> signals/receptors -> location -> mechanism -> outcome -> application.
  - Use old papers for definitions, diagrams, examples, and mark schemas only if the current paper structure differs.
  - If the formal paper references missing sections or files, add a QA flag and do not invent missing stems.
future_unit_diagnostic_questions:
  - Is there a gap between old short-answer format and recent essay/major-answer format?
  - Do KPs need to be process chains rather than isolated terms?
  - Do questions rotate scenario contexts while preserving the same examiner operation?
  - Is any referenced paper section missing from the supplied sources?
non_transferable_content:
  - antibodies
  - MHC
  - TCR
  - germinal centre
  - pathogen-specific immune content
  - clinical immunology examples
  - any Immunology-specific topic recurrence
affected_workflows:
  - unit_grouping_regime_split
  - question_type_gate
  - exam_format_diagnosis
  - knowledge_point_optimisation
  - past_paper_statistics
  - pattern_detection
  - question_type_outputs
  - qa
  - cross_subject_regression
anti_patterns_prevented:
  - pooling old short-answer papers with current essay blueprint
  - outputting isolated vocabulary instead of process-chain explanations
  - inventing missing Paper 1 or Section A content
  - inventing the exact transition year between regimes
validation_checks:
  - old short-answer papers are not current blueprint evidence when format differs
  - process-chain KPs include input, actors, mechanism, outcome, and application
  - missing formal paper sections produce QA flags
```

### Genome Maintenance and Regulation Contribution

```yaml
source_unit: Genome Maintenance and Regulation
source_materials:
  - lecture_slides
  - handwritten_or_image_examples
observed_unit_pattern:
  - large lecture deck requires lecture-order preservation and module-boundary detection
  - Example Essay Mode requires lecture-logic extraction before drafting
  - comparison essays work best when organised by shared comparison axes, not by separate organism/topic blocks
  - handwritten example essays should teach style, paragraph logic, density, and comparison strategy only
  - extra reading must be verified and tightly integrated
generic_skill_contribution:
  - teaches Example Essay Mode as a separate branch from default prediction output
  - teaches lecture storyline extraction: biological problem -> molecular constraint -> mechanism -> named example -> consequence -> comparison/synthesis
  - teaches comparison-axis essay planning
  - teaches style-only exemplar use
  - teaches controlled extra-reading insertion
transferable_rule:
  - For any future essay-writing request, detect question scope, extract lecture logic, build a paragraph plan, then draft.
  - For comparison essays, organise paragraphs by comparison axes rather than writing one block per system.
  - Use exemplars for answer structure and academic style only; never use exemplar biological claims as factual authority unless independently verified.
  - Use at most one compact verified extra-reading insert unless the user explicitly asks for more.
future_unit_diagnostic_questions:
  - Is the user asking for Example Essay Mode or only predicted practice questions?
  - Does the essay require comparison axes?
  - Are exemplar answers factual sources or style-only evidence?
  - Is extra reading directly relevant to the exact question, verified, and short enough to integrate?
non_transferable_content:
  - CRP/catabolite repression
  - EnvZ/OmpR
  - trp attenuation
  - ORC/Cdc6/Cdt1/MCM
  - eIF2/eIF4E/mTOR
  - chromatin examples
  - any Genome-specific molecular topic recurrence
affected_workflows:
  - lecture_segmentation
  - knowledge_point_optimisation
  - example_essay_mode
  - extra_reading_and_exemplars
  - qa
  - cross_subject_regression
anti_patterns_prevented:
  - writing Example Essays as slide summaries
  - organising comparison essays as disconnected topic blocks
  - copying exemplar claims as facts
  - overusing or inventing extra reading
validation_checks:
  - full Example Essays require explicit user request
  - paragraph plan exists before drafting
  - exemplar content is style-only unless verified
```

### BIOL21111 Proteins Contribution

```yaml
source_unit: BIOL21111 Proteins
source_materials:
  - lecture_slides
  - formal_past_papers
  - handwritten_or_image_examples
observed_unit_pattern:
  - recent papers use answer-one project/scenario long-answer format
  - different biological protein systems rotate across years
  - examiner operations recur: purification, characterisation, folding, affinity, mutation, interface, structural determination, readout interpretation, controls
  - old papers may support method/concept coverage but do not control current answer style
  - high-scoring answers are compact experimental arguments, not broad essays
generic_skill_contribution:
  - teaches long-answer project/scenario routing as distinct from essay routing
  - teaches operation-over-content prediction: recurrent examiner operations matter more than repeated biological systems
  - teaches method-driven paragraph planning by question part and mark weight
  - teaches mandatory answer logic: question goal -> lecture principle -> scenario application -> expected readout -> interpretation -> limitation/control
  - teaches that method lists without readout interpretation are insufficient
transferable_rule:
  - For any future method-heavy Unit, detect whether the current formal regime is project/scenario long-answer rather than essay.
  - If the exam rotates systems but reuses operations, predict operation slots, not repeated system names.
  - Structure model answers by question parts, mark weights, method principles, readouts, interpretation, and controls.
  - Use older different-format papers only for method/concept coverage.
future_unit_diagnostic_questions:
  - Does the paper introduce a scenario/system and ask the student to design or justify methods?
  - Are biological examples rotating while examiner operations recur?
  - Does the question require expected readouts and interpretation?
  - Would a broad essay fail because the required answer is a compact experimental argument?
non_transferable_content:
  - HdeA
  - Protein A/G
  - Ept/Hi
  - specific protein examples
  - exact BIOL21111 operation recurrence as content prediction for another Unit
affected_workflows:
  - question_type_gate
  - exam_format_diagnosis
  - knowledge_point_optimisation
  - archetype_mapping
  - pattern_detection
  - question_type_outputs
  - long_answer_project_mode
  - extra_reading_and_exemplars
  - excel_generation
  - qa
  - cross_subject_regression
anti_patterns_prevented:
  - writing a generic essay for a project/scenario question
  - predicting repeated protein systems instead of recurrent examiner operations
  - listing methods without explaining readouts and interpretation
  - using old papers as current-regime blueprint
validation_checks:
  - long-answer project mode triggers from method-design evidence
  - answer plans include method principle, scenario application, readout, interpretation, and control
  - old/different-format papers are coverage only
```

## CrossUnitRegressionReport Schema

Regression output must contain both unit-specific and generic-contribution results.

```yaml
CrossUnitRegressionReport:
  unit_specific_results:
    - unit_key:
      pass_fail:
      failures:
  generic_contribution_results:
    - source_unit:
      contribution_tested:
      transferable_rule:
      future_unit_applicability:
      non_transferable_content_checked:
      pass_fail:
      failures:
  global_failures:
    - cross_unit_content_leakage
    - unit_specific_instruction_outside_regression_context
    - missing_transfer_rule
    - missing_non_transferable_content
```

## Regression Pass/Fail Rules

The Skill fails if:

- production logic branches on a benchmark Unit name instead of evidence conditions;
- benchmark content appears in another Unit's factual content or prediction evidence;
- a Unit benchmark lacks generic contribution metadata;
- a Unit benchmark lacks non-transferable content;
- old/different-regime formal papers are used as current blueprint evidence without comparability proof;
- exemplar images are used as factual evidence without verification;
- mixed data/problem formats are handled as pure essays;
- project/scenario long-answer exams are handled as generic essays;
- slide/page images are distorted or missing without placeholders in visual workbook output.

The Skill passes only if:

- each benchmark Unit has unit-specific pass/fail checks;
- each benchmark Unit also validates a transferable rule for future Units;
- all non-transferable content is explicitly blocked from cross-unit transfer;
- question-type routing is evidence-driven;
- Excel output adapts by detected format, not Unit name;
- QA flags expose uncertainty and evidence limitations.
