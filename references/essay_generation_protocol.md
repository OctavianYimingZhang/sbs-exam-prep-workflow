# Essay Generation Protocol

Example Essay generation is a DOCX-first branch used only when the user explicitly asks for complete Example Essays, model essays, full essay-style answers, or complete essay documents. Workbook KP explanations and single essay-style paragraphs do not trigger this branch unless the user asks for full Example Essays.

The protocol applies across biological and non-biological science-style essays. The factual source base changes by subject; the writing discipline does not.

Use `language_quality_contract.md` as the source of truth for prose quality. This file defines Example Essay orchestration, source grounding, and planning.

## Core Principle

An Example Essay is not a longer summary of lecture slides. It is a controlled answer to a question:

```text
question demand -> relevant source scope -> lecture/source logic -> paragraph function -> concise evidence-backed argument
```

Every paragraph must earn its place by advancing the answer. Do not pad to reach a word count.

## Required Internal Pipeline

Run this sequence before drafting:

```yaml
ExampleEssayMode:
  question_analysis:
  source_scope_detection:
  lecture_or_material_reading:
  source_logic_reconstruction:
  citation_detection:
  citation_original_source_resolution_and_reading:
  classic_experiment_fallback_if_slide_citations_absent:
  extra_reading_book_or_academic_search:
  knowledge_inventory:
  paragraph_plan:
  language_compression_plan:
  exam_ready_refinement_pass:
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

## Language Compression Plan

Before drafting the final version, run a compression pass. Compression means removing repeated or low-value wording while preserving the academic mechanism.

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

## Exam-Ready Refinement Pass

After the compression pass, run a second pass focused on answer quality rather than length.

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

## Default KP Workbook Synthesis

Workbook KP explanations are not complete Example Essays, but they must follow the same low-level prose rules:

```text
claim -> mechanism/process/evidence -> consequence
```

Write the answer paragraph itself, not instructions about writing. Do not narrate slides or pages. Do not preserve coverage by page-by-page summary.

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

Fail safe by omitting uncertain material rather than inventing mechanisms, citations, mark schemes, dates, names, statistics, or lecturer preferences.

## Output Contract

When explicitly requested, generate:

```yaml
ExampleEssayOutput:
  requested_or_predicted_question:
  question_deconstruction:
  knowledge_inventory:
  paragraph_plan:
  language_compression_plan:
  extra_reading_insert:
  high_score_example_essay:
  paragraph_function_map:
  source_content_used:
  excluded_content:
  examiner_fit_checklist:
    - source_scope_covered:
    - examples_used_as_evidence:
    - causal_logic_clear:
    - comparison_explicit:
    - evidence_use_controlled:
    - extra_reading_controlled:
    - word_efficiency:
```

Primary file output:

```yaml
ExampleEssayDOCXOutput:
  output_folder: Example_Essays_DOCX/
  documents:
    - EE01_<short_safe_question_title>.docx
    - EE02_<short_safe_question_title>.docx
  user_facing_only:
    - requested final artefacts
  internal_qa_artifacts_not_returned_unless_requested:
    - example_essay_manifest.json
    - example_essay_source_audit.json
    - EE01_source_map.json
    - EE01_qa.json
    - citation_resolution_log.json
```

For Excel, never place a complete essay into one cell. Excel paragraph-row output is an optional audit export only when explicitly requested.

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
