# Essay Generation Protocol

Example Essay generation is a DOCX-first branch used when the user explicitly asks for essay preparation, complete Example Essays, model essays, full essay-style answers, or complete essay documents. KP explanations and single essay-style paragraphs do not trigger this branch unless the user asks for essay prep or full Example Essays.

The protocol applies across biological and non-biological science-style essays. The factual source base changes by subject; the writing discipline does not.

Use `language_quality_contract.md` as the source of truth for prose quality. This file defines Example Essay orchestration, source grounding, and planning.

## Core Principle

An Example Essay is not a longer summary of lecture slides. It is a controlled answer to a question:

```text
question demand -> relevant source scope -> lecture/source logic -> paragraph function -> concise evidence-backed argument
```

Every paragraph must earn its place by advancing the answer. Do not pad to reach a word count.

## Required Internal Pipeline

Run this orchestration sequence for complete Example Essay generation:

```yaml
ExampleEssayMode:
  question_analysis:
  source_scope_detection:
  lecture_or_material_reading:
  ppt_or_source_logic_reconstruction:
  citation_detection:
  citation_original_source_resolution_and_reading:
  classic_experiment_fallback_if_slide_citations_absent:
  extra_reading_scope_matching:
  knowledge_inventory:
  paragraph_plan:
  first_draft:
  citation_and_extra_reading_integration:
  compression_budget_estimate:
  expression_efficiency_compression_pass:
  accuracy_preservation_pass:
  analytic_argument_pass:
  micro_extra_reading_enhancement_pass:
  highlight_plan:
  source_to_run_mapping:
  high_score_example_essay:
  docx_generation:
  docx_format_linting:
  render_or_visual_qa:
  source_audit_json:
  examiner_fit_checklist:
```

The final user-facing answer should expose requested artefacts and keep internal helper files out, while the essay itself must visibly follow the internal plan.

Optional visual aids may be planned only after the essay or notes text is source-backed. Generated schematics are revision aids, not evidence, citations, official figures, or replacements for written analysis. Follow `visual_aid_generation_protocol.md`; skip the visual-aid layer when generation is unavailable or when the concept does not benefit from a schematic.

Do not:

- write from memory;
- write from a predicted theme or practice variant alone without verifying the supplied lecture/source scope;
- write from a past-paper stem without reading the relevant lecture/source material;
- copy citations printed in slides without resolving and reading the original source when source-derived content is used;
- skip citation discovery merely because the user did not provide a citation list;
- add extra reading without locating the relevant chapter, section, paper, DOI, PubMed record, publisher page, or textbook source;
- hide all source logic in diagnostics while outputting an ungrounded essay;
- produce several complete essays in one Word document;
- use benchmark/example content as factual content for a new source set.

## Source Grounding

Before planning or drafting, read the supplied lecture slides, official lecture notes, formal questions, practical materials, marking criteria, exemplars, extra reading recommendations, and recommended books relevant to the question.

Source priority:

1. Relevant lecture slides and official notes.
2. Formal question wording and official exam guidance.
3. Practical materials, mocks, answer keys, and exemplars for format and answer-style support.
4. Original sources cited by relevant lecture material, only after they are resolved and read.
5. Verified classic or landmark experiments found by academic search when relevant lecture slides contain no usable citations.
6. Uploaded extra-reading books, only matched chapters or sections.
7. Other peer-reviewed papers, textbooks, DOI/PubMed/publisher pages, or Google Scholar results when no official reading is supplied or citation resolution requires it.

If relevant lecture/source material cannot be identified or read, do not generate a polished essay. Emit a QA flag and ask for the missing material.

## Example And Exemplar Use

Examples from other essays, images, courses, or benchmark runs teach structure only:

- paragraph function;
- density;
- opening strategy;
- comparison strategy;
- citation placement;
- compression method;
- sector/system-level abstraction;
- answer organisation;
- DOCX layout.

They do not supply factual content, topic recurrence, citation authority, lecturer preference, or prediction evidence.

## Question Analysis

Classify the question before planning:

- describe;
- explain;
- compare/contrast;
- evaluate;
- mechanism;
- experimental evidence;
- scenario/application;
- data/problem;
- sector/system-level analysis;
- cross-topic synthesis.

Infer likely scope from the question and supplied evidence:

- one detailed knowledge point;
- one lecture or practical block;
- several lectures inside one module;
- a whole source set;
- a cross-module synthesis.

```yaml
EssayQuestionDeconstruction:
  question:
  command_verb:
  expected_scope:
  included_sources:
  excluded_sources:
  question_archetype:
  required_core_claims:
  required_mechanisms_or_processes:
  required_evidence_or_examples:
  useful_comparisons:
  optional_extra_reading:
  expected_answer_shape:
```

## Source Logic Reconstruction

Extract factual content and teaching/argument sequence separately.

For lecture-heavy biological material, common logic patterns include:

```text
biological problem -> molecular/cellular constraint -> mechanism -> evidence/example -> consequence
evidence/experiment -> mechanism tested -> interpretation -> limitation
```

For method, practical, or project material:

```text
problem -> method principle -> experimental design -> readout -> interpretation -> control -> limitation
```

For non-biological science or sector-level essays:

```text
sector/system problem -> theoretical frame -> examples as evidence -> implementation mechanism -> wider implication
```

Slide/source order informs the storyline, but paragraph order is determined by question command word and examiner expectation.

## PPT-Anchored Detail Control

Example Essays must be lecture-first and PPT/source-anchored. Extra Reading, recommended books, lecture-cited originals, and academic papers may sharpen only a mechanism, evidence point, comparison, limitation, or interpretation slot that is already present in the relevant lecture/source logic.

Do not add a named molecular, cellular, channel, receptor, pathway, assay, circuit, gene, material, equation, or method detail merely because it is true or academically impressive. A detail is admissible only if it passes all five tests:

1. PPT/source anchor: the relevant lecture/source contains the parent mechanism, model, evidence point, or comparison slot.
2. Question relevance: the detail helps answer the exact essay question, not a broader review topic.
3. Precision-only: the detail makes an existing claim more precise without changing the level, scope, or direction of the claim.
4. Efficiency: the detail increases examinable mechanism per word and does not create a catalogue, second argument, or review-style digression.
5. Accuracy: the final compressed wording preserves causal strength, scope qualifiers, lecture distinctions, and evidence boundaries.

Reject details that are:

- true but not anchored in the lecture/PPT/source logic;
- more detailed than the question or source level requires;
- a list of molecules, channels, receptors, genes, examples, or methods without analytic use;
- a new subtopic introduced by Extra Reading;
- a detail that requires a new explanatory sentence before it is intelligible.

Use a `DetailAdmissionMatrix` internally when adding or rejecting detail:

```yaml
DetailAdmissionMatrix:
  paragraph_id:
  ppt_core_claim:
  ppt_mechanism_slot:
  question_function:
    - thesis
    - mechanism
    - evidence
    - interpretation
    - limitation
    - synthesis
  candidate_detail:
  source_class:
    - lecture
    - recommended_book
    - lecture_cited_original_paper
    - verified_classic_source
    - rejected
  admission_decision:
    - keep
    - compress
    - reject
  reason:
  risk_flags:
    - no_ppt_anchor
    - true_but_unnecessary
    - review_article_drift
    - list_without_analysis
    - mechanism_level_shift
    - compression_risks_inaccuracy
    - citation_stack
    - extra_reading_replaces_ppt_logic
```

High detail is not automatically high quality. The standard is: PPT/source-anchored, citation-supported, analytically interpreted mechanism per word.

## Knowledge Inventory

Before writing, classify material:

```yaml
EssayKnowledgeInventory:
  must_use:
    - source-backed claims without which the answer is incomplete
  should_use_if_space:
    - useful mechanisms, examples, data points, comparisons, or caveats
  optional_extra_reading:
    - verified extensions that improve precision or sophistication
  exclude:
    - irrelevant details
    - repeated low-value case facts
    - unsupported claims
    - excessive background
    - content outside question scope
```

Prioritise:

```text
question-relevant core claims > source objectives/summaries > repeated mechanisms > named evidence/examples > background definitions > extra reading
```

## Paragraph Plan

Every complete Example Essay must be planned paragraph-by-paragraph.

```yaml
EssayParagraphPlan:
  paragraph_number:
  function: thesis | mechanism | comparison | example | evidence | application | limitation | synthesis
  core_claim:
  source_content_used:
  evidence_or_example_used:
  extra_reading_used:
  why_this_paragraph_is_needed:
  link_back_to_question:
```

Each body paragraph must contain:

- one clear claim;
- one mechanism, process, comparison axis, evidence operation, or implementation logic;
- one or two examples/evidence items where useful;
- a link back to the question.

Default paragraph logic:

```text
Claim -> mechanism/process/evidence -> scope or limitation -> consequence -> link back.
```

## Expression Efficiency And Study-Time Density

Run citation and Extra Reading integration before final compression. If the essay is compressed first and then enriched, density, paragraph function, and source balance can drift.

Compression is not a word-count operation. It is an exam-preparation efficiency operation: maximise useful examinable knowledge per word while preserving mechanism accuracy.

Before compressing, estimate the safe compression budget. Do not apply a requested percentage mechanically. A 30% reduction is valid only if the removable material is genuinely redundant after the source skeleton, evidence, citation-supported details, and analytic limitations are protected.

Use a `CompressionBudgetEstimate` internally:

```yaml
CompressionBudgetEstimate:
  current_word_count:
  requested_reduction:
    type: percent | words | unspecified
    value:
  protected_source_skeleton:
    - core source claim, mechanism, evidence, comparison, limitation, or synthesis item that cannot be deleted
  protected_academic_details:
    - named evidence, citation-supported mechanism detail, or examiner-relevant distinction that should be kept or compressed but not removed
  removable_redundancy:
    - repeated framing
    - duplicated source/evidence restatement
    - overlong transition
    - low-value background
    - repeated synthesis list
  safe_reduction_range:
    min:
    max:
  unsafe_threshold:
  decision:
    - compress_within_safe_range
    - partial_compression_only
    - reject_requested_reduction
  reason:
```

Compression targets must be content-derived. If a requested reduction would remove a protected item, use the largest safe reduction instead and record that the requested target exceeds the safe compression budget.

A sentence should stay only if it performs at least one of these functions:

- states the paragraph claim;
- explains a required mechanism, process, method, or control problem;
- gives evidence that changes the strength or scope of the claim;
- interprets what an experiment, example, dataset, or figure proves;
- states a limitation, contrast, or boundary condition;
- adds a verified named detail that sharpens a PPT/source-derived mechanism slot;
- links the paragraph back to the question.

Remove:

- repeated definitions;
- repeated claim restatements;
- repeated case descriptions;
- firm/example-level details that do not support the question;
- lecture-route or source-route narration;
- exam-guidance sentences that tell the student what to write instead of writing the answer;
- vague metacommentary such as `this essay will explore`;
- decorative transitions;
- unnecessary historical background;
- unsupported statistics;
- overlong citation stacks;
- examples that are not converted into a wider argument.

Keep:

- mechanisms;
- causal links;
- named evidence where it proves the point;
- analytical interpretation of what the evidence shows and what it does not show;
- necessary definitions;
- scope limitations;
- examiner-relevant contrasts;
- verified citations for non-obvious claims.

Do not compress by simply shortening every sentence. Compress by deciding what function each sentence performs.

Protected material may still be made more concise, but it must remain present. For example, a named interneuron set, citation-supported cell identity, experiment condition, or timing result can be compressed into a tighter clause when it is examiner-relevant; it must not be deleted merely to hit a percentage target.

## Accuracy-Preserving Compression

After compression, run an accuracy preservation pass. The compressed essay must preserve:

1. Causal strength: `supports`, `implicates`, `is consistent with`, and `contributes to` must not become `proves` unless the source proves causality.
2. Scope qualifiers: do not collapse specific phrases such as `core rhythm`, `normal locomotion`, `basic output`, `precision movement`, `clinical recovery`, `under these assay conditions`, or `in this model` into one broad claim.
3. Negative distinctions: `not necessary for generating the core rhythm` must not become `not necessary for locomotion`.
4. Model boundaries: a mechanism that adjusts, gates, entrains, stabilises, or modulates output must not be rewritten as the primary generator unless the source says so.
5. Evidence interpretation: experiments, examples, and figures must retain what they show and what they do not show.

Reject compressed wording when it changes the claim scope, removes a required qualifier, or turns a support/modulation claim into a generation/proof claim.

Also reject compressed drafts when the final answer has lost one of the protected source-skeleton items identified in the compression budget. Shorter wording is not acceptable if it reduces mechanism density, removes necessary evidence, or converts a discussion paragraph into a descriptive summary.

## Analytic Argument Pass

After the accuracy pass, run a pass focused on analytic value. A paragraph fails if it contains more than two consecutive descriptive sentences without an analytic sentence.

A valid analytic sentence must do at least one of the following:

- explain why the mechanism solves a control, causal, methodological, clinical, or sector-level problem;
- state what an experiment proves or fails to prove;
- compare two models, mechanisms, pathways, or methods;
- define the scope of a claim;
- link a molecular, cellular, circuit, method, or source detail to system-level function;
- explain why the detail matters for the essay question.

Use this pattern:

```text
description -> description -> analysis
```

Do not leave named components as a list. Rewrite list-like content into an answer function: which problem each component solves, what distinction it supports, or what consequence follows.

Reject and rewrite:

- lecture/source-route narration, such as sentences whose main function is to state what a lecture, chapter, source, or section introduces next;
- exam-guidance phrasing, such as telling the student what the final thesis should be;
- repeated negative framing where several sentences say only what the answer is not;
- broad importance claims that do not specify the mechanism, consequence, or limitation;
- examples or experiments that stop at description without interpretation;
- citation-derived claims that overstate support as single-cause proof.

For evidence-heavy material, each major experiment, dataset, case, or example must be reduced to its answer function:

```text
evidence -> mechanism tested -> interpretation -> limitation or scope
```

Use stronger causal verbs only when the verified source directly warrants them. Otherwise prefer calibrated verbs such as `supports`, `implicates`, `is consistent with`, `contributes to`, or `suggests`.

## Micro Extra Reading Enhancement Pass

Run this pass after the essay has a coherent draft and before final highlight planning, source-to-run mapping, and DOCX generation.

Purpose:

- do not rewrite the essay;
- do not add new paragraphs;
- add only short verified named details to unhighlighted sentences whose parent mechanism is explicit in the lecture/PPT/source logic;
- increase molecular, circuit, method, chemical, or pathway precision without changing the lecture-derived argument, level, scope, or exam function.

The correct question is not "Can extra reading add more content?". The correct question is:

```text
Is there an unhighlighted mechanism, evidence, or interpretation sentence whose parent mechanism is explicitly present in the PPT/source logic, and whose generic slot can be made more precise by one verified named detail without changing the level, scope, or exam function of the sentence?
```

Eligible sentence functions:

- mechanism;
- evidence;
- interpretation;
- application when it contains a mechanism or method readout.

Do not apply this pass to thesis, transition, broad synthesis, or conclusion sentences unless the sentence contains a specific generic mechanism slot whose precision is required by the question.

Detect generic slots such as:

```text
receptor
channel
transporter
enzyme isoform
kinase or phosphatase
transcription factor or partner
response element
morphogen or ligand
cofactor or allosteric ligand
chemical species or transport form
protein domain
cellular compartment
afferent, interneuron, projection, or circuit class
assay readout or experimental marker
pathway intermediate
```

Candidate insertion rules:

```yaml
MicroExtraReadingInsertion:
  original_sentence:
  original_phrase:
  inserted_phrase:
  parent_ppt_or_source_slot:
  question_function:
  source_class: recommended_book | citation_original_source | classic_experiment_source
  source_anchor:
  highlight_colour: yellow | green
  word_count_delta:
  claim_delta: precision_only
  qa_status: micro_detail_verified | rejected
```

Accept an insertion only when all conditions are true:

- the sentence already has a lecture or official-source anchor;
- the parent PPT/source mechanism slot is identified explicitly;
- the inserted phrase is supported directly by a verified source anchor;
- the inserted phrase is compact enough to remain a phrase or short clause inside the original sentence;
- the insertion names one concrete object, step, source, species, domain, compartment, readout, or module;
- the insertion preserves the grammar and argument direction of the original sentence;
- the addition improves causal precision, assay precision, or mechanistic specificity;
- the essay remains inside the Extra Reading density limit.

Use these low-risk insertion patterns:

```text
generic noun -> specific appositive
generic transport or pathway claim -> named chemical form or step
generic signal phrase -> named receptor, kinase, ligand, domain, or module
generic readout -> named assay marker, flux, compartment, or experimental endpoint
```

Highlight and source mapping are mechanical:

- uploaded recommended book or textbook chapter = yellow;
- verified lecture-cited original paper or verified classic source = green;
- ordinary lecture or official-source material = no highlight;
- exemplar-only or remembered detail = reject.

Reject an insertion when:

- no parent PPT/source slot exists;
- no exact source anchor exists;
- author-year, DOI, PubMed, publisher, chapter, or section verification is missing where required;
- the phrase requires a new explanatory sentence;
- the phrase is long enough to become a new explanation or second argument;
- it starts a new subtopic;
- it replaces lecture logic with external-source logic;
- it makes a stronger claim than the source supports;
- it duplicates a molecule, method, or named detail already nearby;
- it creates a molecular, channel, receptor, gene, pathway, method, or case catalogue without analytic use;
- it creates citation stacking;
- it turns a concise exam answer into a review-style answer.

Highlight span must be minimal. Highlight only the inserted phrase or short inserted clause. Do not highlight a whole lecture-derived sentence merely because one inserted term came from Extra Reading.

QA flags for this pass:

```text
micro_detail_verified
micro_detail_parent_slot_missing
micro_detail_rejected_unverified
micro_detail_insert_missing_source_anchor
micro_detail_too_expansive
micro_detail_claim_delta_not_precision_only
true_but_not_needed_detail
unnecessary_channel_catalogue
unnecessary_receptor_catalogue
descriptive_list_without_analysis
compression_changed_claim_scope
compression_removed_required_qualifier
compression_target_exceeds_safe_budget
protected_source_skeleton_removed
mechanical_compression_trace
highlight_span_too_broad
source_type_colour_mismatch
lecture_logic_replaced_by_extra_reading
academic_paper_author_year_unverified
recommended_book_section_not_found
```

## High-Quality Essay Language Rules

Use the following style discipline for every Example Essay:

1. Start with the answer. The first paragraph should define the problem or thesis, not announce that the essay will discuss a topic.
2. If there is a debate or competing model, state the dispute first, then introduce each model in logical order.
3. A paragraph should move from claim to evidence and then to implication. Do not list facts and leave the inference unstated.
4. Use examples as proof of a broader mechanism or sector/system pattern. Do not let examples become disconnected mini-case studies.
5. Make contrasts explicit. Avoid ambiguous `rather than` sentences unless both sides of the contrast are named precisely.
6. Prefer precise upper-level terms when a list is only illustrative, but keep the list when the listed mechanisms are examiner-relevant.
7. Avoid lecture-route narration and exam-guidance phrasing inside the answer.
8. End paragraphs with a consequence, limitation, or direct answer to the question.
9. End the essay with synthesis, not new evidence.

Strong paragraph shape:

```text
Rhythmic locomotion is centrally generated only in a restricted sense.
The key issue is what initiates repeated flexor-extensor alternation.
The reflex-chain model treats sensory reafference as the trigger for the next phase.
The central-pattern-generator model makes the stronger claim that spinal circuits can generate the core rhythm internally, while sensory input regulates its expression.
The evidence supports central timing but also limits the claim because balance, load regulation, and terrain adaptation still require feedback.
```

This pattern is transferable: define the claim, locate the alternative or limitation, use evidence, then state scope.

## Essay-Level Structure

Introduction:

- state the question's core problem;
- define only terms required for the answer;
- state the thesis;
- preview the organising logic, not a list of all facts.

Body paragraphs:

- each paragraph has one function;
- examples support the function;
- citations support non-obvious factual or theoretical claims;
- paragraphs are sequenced by logic, not by slide/page order.

Conclusion:

- answer the question directly;
- synthesise the main mechanisms or comparisons;
- do not add new examples or unsupported claims.

## Comparison Essays

Do not write disconnected blocks:

```text
Paragraph 1: all facts about A.
Paragraph 2: all facts about B.
Paragraph 3: unrelated comment.
```

Prefer comparison axes:

```text
Paragraph 1: shared problem and thesis.
Paragraph 2: axis 1, comparing both sides.
Paragraph 3: axis 2, comparing both sides.
Paragraph 4: evidence or limitation.
Paragraph 5: synthesis.
```

Each axis must be supported by target-source evidence.

## Sector/System-Level Essays

When a question asks for sector-level, system-level, or broader scientific significance:

- state the level of analysis explicitly;
- demote firms/cases/examples to evidence;
- replace excessive case detail with the shared mechanism;
- conclude each section by explaining what the example proves about the wider system.

Strong abstraction pattern:

```text
example detail -> operational mechanism -> wider sector/system implication
```

If the essay starts to read as separate case studies, rewrite the paragraph around the shared mechanism.

## Citation Discipline

Use citations minimally and sufficiently.

Cite:

- non-obvious factual claims;
- theory/framework definitions;
- mechanisms;
- experimental evidence;
- quantitative claims;
- sector-level generalisations;
- source-derived extra-reading additions.

Do not cite:

- obvious transitions;
- the same claim repeatedly;
- unsupported sources copied from another essay;
- a slide citation unless the original source has been resolved and read when source-derived content is used.

Avoid citation stacking. If several sources support the same general claim, keep the most directly relevant source(s). If evidence is insufficient, omit the claim or mark it uncertain in QA.

Match claim strength to source strength. A study, review, or textbook section may support, implicate, refine, or constrain a mechanism without proving it as the sole cause. Do not write causal certainty unless the resolved source directly supports that level of certainty.

### Citation Fallback When The User Supplies No Citation List

When the user asks for a complete Example Essay but does not provide citations:

1. Read the relevant lecture slides before searching.
2. Detect citations in slide text, notes, reference slides, footers, figure captions, and OCR/visual inspection of relevant image-only slides.
3. Resolve detected citations by DOI, PMID, author-year, title fragment, journal information, or publisher/PubMed/Google Scholar records.
4. Read the original source before using source-derived content. Green-highlight only the source-derived clause or sentence and include a verified author-year citation.
5. If no usable lecture-slide citation exists, perform targeted academic search for several classic experiments or landmark primary studies that directly test the lecture mechanism, model, method, or evidence claim.
6. Select classic experiments using the same standard inferred from lecture-cited sources: direct mechanistic relevance, primary evidence where possible, reliable academic locator, and verified author-year details.
7. Use no more classic-experiment detail than needed to support the lecture-grounded argument. The essay must remain controlled by lecture logic.

Never cite a source just because it is famous. It must support the exact paragraph claim and be verified from a reliable academic source.

## Extra Reading

Use extra reading only if it directly improves the answer to this exact question.

Allowed use:

- one mechanism deepener;
- one experimental support point;
- one comparison refinement;
- one modern application or method if directly relevant;
- one theoretical frame for a sector/system claim.

Extra reading must not:

- replace lecture/source logic;
- exceed roughly 10-15% of essay body words unless instructed;
- introduce unrelated mechanisms;
- contradict official sources without explaining the distinction;
- appear without verified author/year/source details.

If no supplied extra reading exists, perform targeted academic search only when it improves accuracy or citation quality. Prefer peer-reviewed papers, textbooks, DOI/PubMed/publisher pages, and official academic sources.

## Highlight And Source Mapping

For DOCX output:

- ordinary lecture/source content is not highlighted;
- uploaded extra-reading book content is yellow-highlighted;
- read original sources cited by lecture material are green-highlighted and include author-year citations;
- every highlighted run must map to a source anchor in the source map JSON.

Do not highlight content whose source has not been verified.

## Default KP Synthesis

KP explanations are not complete Example Essays, but they must follow the same low-level prose rules:

```text
claim -> mechanism/process/evidence -> consequence
```

Write the answer paragraph itself, not instructions about writing. Do not narrate slides or pages. Do not preserve coverage by page-by-page summary.

For `exam_prep_notes_docx`, use essay-ready paragraph blocks as an add-on layer only. Do not generate full Example Essays unless the user explicitly requests essay preparation, model essays, full essay-style answers, or complete essay documents.

## QA Flags

Add QA flags when needed:

- `essay_question_scope_uncertain`;
- `source_scope_uncertain`;
- `paragraph_plan_missing`;
- `source_logic_not_preserved`;
- `causal_chain_missing`;
- `comparison_axis_missing`;
- `sector_level_abstraction_missing`;
- `essay_exceeds_word_limit`;
- `example_used_as_fact`;
- `citation_original_unreadable`;
- `lecture_slide_citation_absent_classic_experiment_search_required`;
- `classic_experiment_source_unverified`;
- `classic_experiment_not_question_relevant`;
- `extra_reading_unverified`;
- `extra_reading_not_question_relevant`;
- `extra_reading_too_large`;
- `extra_reading_replaces_core_sources`;
- `recommended_reading_missing`;
- `unsupported_claim`;
- `citation_stack_or_overcitation`;
- `case_detail_overload`;
- `lecture_route_narration_present`;
- `exam_guidance_sentence_present`;
- `citation_strength_overclaim`;
- `slide_or_page_narration_present`.
- `ppt_anchor_missing`;
- `true_but_not_needed_detail`;
- `review_article_drift`;
- `unnecessary_channel_catalogue`;
- `unnecessary_receptor_catalogue`;
- `descriptive_list_without_analysis`;
- `compression_changed_claim_scope`;
- `compression_removed_required_qualifier`;
- `compression_target_exceeds_safe_budget`;
- `protected_source_skeleton_removed`;
- `mechanical_compression_trace`;
- `extra_reading_inserted_before_ppt_logic`;
- `extra_reading_replaces_lecture_logic`;
- `citation_added_without_paragraph_function`;
- `word_count_reduced_but_density_not_improved`.

Fail safe by omitting uncertain material rather than inventing mechanisms, citations, mark schemes, dates, names, statistics, or lecturer preferences.

## Output Contract

When explicitly requested, generate:

```yaml
ExampleEssayOutput:
  requested_or_predicted_question:
  question_deconstruction:
  knowledge_inventory:
  paragraph_plan:
  detail_admission_matrix:
  citation_and_extra_reading_integration:
  compression_budget_estimate:
  expression_efficiency_compression_pass:
  accuracy_preservation_pass:
  analytic_argument_pass:
  extra_reading_insert:
  high_score_example_essay:
  paragraph_function_map:
  source_content_used:
  excluded_content:
  examiner_fit_checklist:
    - source_scope_covered:
    - lecture_logic_preserved:
    - ppt_anchor_for_each_extra_detail:
    - no_true_but_unneeded_detail:
    - no_review_article_drift:
    - analytical_sentences_present:
    - protected_source_skeleton_preserved:
    - compression_preserves_claim_scope:
    - compression_inside_safe_budget:
    - compression_improves_expression_efficiency:
    - examples_used_as_evidence:
    - evidence_interpreted_not_listed:
    - causal_logic_clear:
    - comparison_explicit:
    - evidence_use_controlled:
    - citation_density_controlled:
    - extra_reading_controlled:
    - extra_reading_precision_layer_only:
```

Primary file output:

```yaml
ExampleEssayDOCXOutput:
  default_document: Essay_Module_Example_Essays.docx
  optional_separate_output_folder: Example_Essays_DOCX/
  documents:
    - Essay_Module_Example_Essays.docx
    - optional EE01_<short_safe_question_title>.docx
    - optional EE02_<short_safe_question_title>.docx
  user_facing_only:
    - requested final artefacts
  internal_qa_artifacts_not_returned_unless_requested:
    - example_essay_manifest.json
    - example_essay_source_audit.json
    - EE01_source_map.json
    - EE01_qa.json
    - citation_resolution_log.json
```

Never place a complete essay into one spreadsheet cell. Paragraph-row output is an optional audit export only when explicitly requested.

## Success Condition

The workflow passes if every Example Essay:

- answers the exact question;
- is traceable to read source material;
- compresses low-value repetition without losing required academic detail;
- uses examples as evidence for a broader claim;
- interprets evidence through mechanism, scope, and limitation;
- handles citations conservatively;
- separates source-grounded content from extra-reading enrichment;
- follows the required DOCX output contract.

It fails if it lists facts without reconstructing the argument, uses benchmark/example content as fact, or writes a generic essay from general knowledge.
