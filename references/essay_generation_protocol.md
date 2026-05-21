# Essay Generation Protocol

Example Essay generation is a first-class branch of the workflow. It is used only when the user explicitly asks for complete Example Essays, model essays, full essay-style answers, or complete essay documents. Requests for workbook KP explanations or single essay-style paragraphs do not by themselves trigger DOCX-first Example Essay Mode.

Default Excel-first behaviour is unchanged for prediction workbooks. Predicted practice questions and essay-style KP explanations appear by default; full Example Essays are generated only on request.

When Example Essay Mode is explicitly requested, the final output is DOCX-first: one standalone Word document per complete essay. Use `example_essay_docx_output_protocol.md`.

## Default KP Workbook Synthesis

Default KP workbook explanations are not full Example Essays, but they must obey the same low-level writing discipline:

```text
claim -> mechanism -> evidence/example -> consequence
```

For each visible workbook explanation cell:

- write the paragraph itself, not instructions about how to write it;
- start with the concept, biological problem, or argument;
- explain the causal mechanism or comparison axis;
- include only the most useful named lecture examples or evidence;
- end with a consequence, interpretation, or exam-relevant link-back;
- do not summarise slides or pages;
- do not use isolated fact lists;
- do not use generic textbook introductions;
- do not use instructions masquerading as explanation, such as `In an essay answer...` or `use these pages`;
- do not preserve coverage by narrating page order.

Use `kp_essay_synthesis_protocol.md` as the operative protocol for default workbook KP explanations. This default pass does not trigger full Example Essay Mode.

## Unit Examples As Essay-Writing Contribution Sources

Unit examples used in this protocol are contribution and regression sources, not content templates for future units. They teach essay-writing operations such as paragraph planning, causal explanation, comparison-axis design, evidence placement, exemplar handling, and extra-reading discipline.

Do not transfer biological content, named molecules, named organisms, lecturer recurrence, or topic recurrence from one unit example into another target unit unless the target unit's own supplied sources contain that content.

Mechanism-heavy essay benchmark principle:

```text
When target lecture and paper evidence require causal biological explanation plus experimental support, each essay KP should combine:
mechanism -> evidence/experiment -> biological consequence.
```

Comparison essay benchmark principle:

```text
When a question asks compare or contrast, paragraph structure should use shared comparison axes. Each body paragraph compares both sides on one axis. Do not write disconnected topic blocks.
```

Exemplar style principle:

```text
Exemplars teach opening strategy, paragraph density, causal phrasing, comparison strategy, and link-back sentences. They do not supply factual content unless independently verified from target-unit lecture material or reliable academic sources.
```

## A. Read Sources First

Before planning or drafting, read the supplied lecture slides, relevant lecture notes, official guidance, formal past-paper stems, marking criteria, and exemplar pages/images.

Hard rule:

```text
No Example Essay may be written from predicted questions alone. The relevant lecture slides must be read first. If relevant lecture slides cannot be identified or read, do not generate a polished essay; emit a QA flag and ask for the required lecture slides.
```

For image-based exemplars:

- use them only for answer structure, paragraph logic, density, comparison strategy, and academic style;
- do not treat biological claims inside handwritten exemplars as factual authority unless verified from slides or reliable academic sources;
- ignore student Chinese annotations unless the user explicitly asks to use them;
- record `visual_inspection_required` if OCR was not performed or handwriting is ambiguous.

## B. Example Essay Mode Pipeline

Run this sequence before producing any essay:

```yaml
ExampleEssayMode:
  question_analysis:
  lecture_slide_scope_detection:
  lecture_slide_reading:
  lecture_logic_reconstruction:
  citation_detection_from_relevant_lecture_slides:
  citation_original_source_resolution_and_reading:
  extra_reading_book_chapter_matching:
  extra_reading_chapter_reading:
  lecturer_intent_analysis:
  knowledge_inventory:
  paragraph_plan:
  highlight_plan:
  source_to_run_mapping:
  high_score_example_essay:
  docx_generation:
  docx_format_linting:
  render_or_visual_qa:
  source_audit_json:
  examiner_fit_checklist:
```

The final answer may expose only the parts the user requested, but the essay must visibly follow the internal plan.

Do not:

- write from memory;
- write from a past-paper question without reading slides;
- use citations copied from slides without reading the original cited source;
- add Extra Reading material without finding the relevant uploaded book chapter or section;
- hide all source logic in diagnostics while outputting an ungrounded essay;
- create one Excel sheet containing all essays as the primary deliverable;
- produce multiple complete essays in one Word document.

## C. Extract Lecture Logic

For every lecture/module relevant to the question, extract:

- lecture title;
- lecturer name;
- learning objectives;
- module order;
- slide sequence;
- repeated mechanisms;
- summary or take-home messages;
- worked examples;
- recommended reading;
- comparison axes;
- named proteins, pathways, genes, molecules, experiments, or model organisms.

Do not merely extract facts. Infer the teaching sequence:

```text
biological problem -> molecular architecture or constraint -> mechanism -> named example -> consequence -> comparison or synthesis
```

Slide order informs the lecture storyline, but paragraph order is determined by the question command word and examiner expectation.

## D. Lecture Knowledge Compiler

For every lecture/module, compile a knowledge inventory before writing:

```yaml
LectureKnowledgeInventory:
  lecture_number:
  lecture_title:
  lecturer:
  module_block:
  central_question:
  slide_order_logic:
  must_write_knowledge:
    - mechanism:
      molecules_or_genes:
      biological_stage_or_context:
      organism_or_model:
      experimental_evidence:
      phenotype_or_consequence:
      why_exam_relevant:
  conditional_knowledge:
    - use_when:
      knowledge:
      reason:
  optional_extra_reading_candidates:
    - source:
      author_year:
      claim_or_extension:
      where_it_could_fit:
      verification_status:
  excluded_or_low_value_content:
    - content:
      why_excluded:
  essay_transition_phrases:
    - from_previous_topic:
      to_next_topic:
      logical_bridge:
```

The Developmental Biology benchmark demonstrates this transferable mechanism-heavy essay rule:

```text
A useful essay knowledge point = one mechanism + one experimental/evidence basis + one developmental consequence.
```

The Genome Maintenance and Regulation benchmark demonstrates this transferable regulatory/comparison essay rule:

```text
A useful essay knowledge point = one regulatory or maintenance problem + one molecular constraint + one mechanism + one named lecture example + one biological consequence.
```

## E. Module Storyline Graph

Build a storyline graph for every module. Use it to preserve the lecturer's logic, not as a rigid essay order.

Genome benchmark contribution example (regression-only content):

```text
prokaryotic global regulation
-> sigma factors, CRP/catabolite repression, two-component systems, SOS
-> RNA-level prokaryotic control by termination, attenuation, riboswitches
-> eukaryotic transcription initiation by GTFs and specific TFs
-> chromatin/nucleosome constraints and histone modification
-> developmental gradients and transcription cascades where relevant
-> DNA replication in prokaryotes
-> DNA replication in eukaryotes and cell-cycle licensing
-> protein synthesis: prokaryotic initiation, eukaryotic initiation, global and specific translational control
-> RNA processing, alternative splicing, turnover, surveillance, RNAi
-> non-coding RNA, transposons, organellar gene expression
```

Use this Genome storyline only to learn module-boundary extraction and lecture-logic preservation. Do not transfer Genome molecular content into another target unit.

Developmental Biology benchmark contribution example (regression-only content):

```text
cleavage and early cell-cycle control
-> fate maps, potency, commitment, determination
-> asymmetric determinants and induction
-> lateral inhibition
-> morphogens and serial signalling
-> Drosophila segmentation: maternal gradients -> gap genes -> pair-rule genes -> segment-polarity genes
-> segment identity: Hox genes, GOF/LOF evidence, posterior prevalence, chromatin maintenance
-> vertebrate segmentation: somite clock, wavefront, Notch/FGF/RA
-> axis formation and gastrulation
-> developmental principles in stem cells and disease
-> plant developmental parallels when relevant
```

Use this Developmental Biology storyline only to learn mechanism-heavy causal ordering and evidence placement. Do not transfer Developmental Biology content into another target unit.

## F. Knowledge Inventory

Before essay writing, classify content:

```yaml
EssayKnowledgeInventory:
  must_use_lecture_content:
    - content directly required by the question and central to slides/objectives
  supportive_lecture_content:
    - useful but not essential detail
  cross_module_content:
    - relevant content from another lecture/module in the same unit
  extra_reading_candidates:
    - source-backed material outside slides
  excluded_content:
    - facts omitted because irrelevant, too detailed, unsupported, or outside scope
```

Prioritise:

```text
learning objectives and summaries > repeated mechanisms > named lecture examples > background definitions > extra reading
```

## G. Question Analysis

Classify the essay question before planning:

- describe;
- explain;
- compare/contrast;
- evaluate;
- mechanism;
- experimental evidence;
- scenario/application;
- cross-module synthesis.

Infer likely scope:

- one detailed KP inside a lecture;
- one lecture;
- several lectures by one lecturer;
- one module;
- several modules;
- whole-unit integration.

Do not infer lecturer preference from one question alone unless labelled low confidence.

```yaml
EssayQuestionDeconstruction:
  question:
  command_verb:
  expected_scope:
  included_lectures:
  excluded_lectures:
  likely_lecturer_or_module:
  question_archetype:
  required_core_mechanisms:
  required_experimental_evidence:
  useful_comparisons:
  optional_extra_reading:
  paragraph_plan:
    - paragraph_number:
      paragraph_function:
      core_claim:
      lecture_knowledge_used:
      evidence_used:
      extra_reading_used:
      why_this_paragraph_is_needed:
      what_is_excluded:
```

## H. Lecturer-Intent Analysis

Use lecturer name, module title, repeated slide wording, learning objectives, formal past-paper patterns, and question wording to infer examiner expectation.

Test whether the lecturer tends to ask for:

- one detailed mechanism;
- compare/contrast between systems;
- a lecture-specific example;
- module-level synthesis;
- experimental evidence;
- disease/application;
- regulatory principle across examples.

Do not assume one lecturer always sets one question.

```yaml
LecturerIntentModel:
  likely_lecturer_or_module:
  evidence:
  contradicted_evidence:
  question_style:
  expected_answer_shape:
  likely_required_experiments:
  likely_required_named_examples:
  likely_extra_reading_tolerance: low | medium | high
  confidence:
```

## I. Paragraph Plan

Every Example Essay must be planned paragraph-by-paragraph before drafting.

```yaml
EssayParagraphPlan:
  paragraph_number:
  function: thesis | mechanism | comparison | example | evidence | extra_reading_insert | synthesis
  core_claim:
  lecture_content_used:
  cross_module_link:
  extra_reading_used:
  why_this_paragraph_is_needed:
  link_back_to_question:
```

Each body paragraph must contain:

- one clear claim;
- one causal mechanism chain;
- one or two named examples if relevant;
- one sentence linking back to the question.

Default causal writing pattern:

```text
condition / signal / cellular constraint
-> sensor / regulator / molecular feature
-> molecular action
-> output change in transcription / translation / replication / repair / expression
-> biological consequence
```

Default paragraph logic:

```text
Claim -> mechanism -> evidence/example -> consequence -> link back to question.
```

Avoid:

- slide-by-slide summaries;
- isolated fact lists;
- generic textbook introductions;
- disconnected prokaryote/eukaryote blocks in comparison essays;
- long historical background;
- padding to reach a word count.

## J. Comparison Essay Structure

For comparison essays, do not use this weak structure:

```text
Paragraph 1: all prokaryote facts.
Paragraph 2: all eukaryote facts.
Paragraph 3: unrelated example.
```

Prefer:

```text
Paragraph 1: shared biological problem and thesis.
Paragraph 2: first comparison axis, comparing both systems directly.
Paragraph 3: second comparison axis, with named examples.
Paragraph 4: extra-reading or cross-module refinement only if useful.
Paragraph 5: synthesis.
```

Comparison-axis categories demonstrated by the Genome benchmark; transfer an axis only when the target unit's own evidence supports it:

- cellular compartmentalisation;
- transcription-translation coupling versus separation;
- genome architecture;
- chromatin/nucleosome constraint;
- origin selection;
- regulatory speed;
- energy cost;
- cell-cycle control;
- environmental responsiveness;
- global versus specific regulation;
- direct molecular sensing versus signalling cascades;
- mRNA selection and translation-initiation control versus transcriptional control.

## K. Exemplar-Derived Style Rules

Handwritten/example essays teach style, not factual authority.

Imitate these strong features:

- start with a broad biological problem, then narrow to the precise contrast;
- state the biological context early;
- use topic sentences that make an argument;
- explain mechanisms as causal sequences;
- compare systems using shared axes;
- show why a difference exists, not just what differs;
- use named molecular examples as evidence for a broader claim;
- place experimental or mechanistic evidence immediately after the claim it supports;
- convert phenotype or mechanism descriptions into inference: `This shows that...`;
- end paragraphs by returning to the question;
- conclude by synthesising the contrast rather than introducing new facts.

Do not copy weak exemplar features:

- vague openings such as `this essay explores`;
- repeated informal transitions such as `what's more`;
- unsupported statistics;
- unverified biological claims;
- excessive background;
- Chinese annotations unless explicitly requested.

## L. Extra Reading Insert Plan

Extra reading source priority:

1. official recommended reading listed in lecture slides, Canvas reading list, course notes, or lecturer guidance;
2. textbook or book chapter used by the unit if explicitly supplied;
3. if no official book/reading is supplied, ask whether the unit has a recommended book or reading list;
4. if unavailable, use peer-reviewed reviews, primary papers, textbooks, PubMed, Google Scholar, DOI pages, or publisher pages.

Verify author surname, year, source type, and the exact lecture claim being supported before use.

Extra reading may be used only as:

- one short enrichment paragraph;
- one precise sentence inside a mechanism paragraph;
- one comparison point that sharpens the lecture argument;
- one evidence-based example that strengthens the lecture mechanism.

Extra reading must not:

- replace lecture content;
- exceed roughly 10-15% of the essay;
- introduce an unrelated mechanism;
- create a new topic that cannot be explained within the word limit;
- contradict slides without explaining the distinction;
- appear without verified author surname and year.

Internal insertion test:

```text
Does this extra-reading point directly improve the answer to this exact essay question?
Does it extend the lecture logic rather than distract from it?
Can it be stated accurately in one or two sentences?
```

If any answer is no, omit it.

Allowed use types:

```yaml
ExtraReadingUseType:
  mechanism_deepener:
    purpose: explains a lecture mechanism at slightly higher molecular resolution
  experimental_support:
    purpose: adds one strong experiment or assay supporting the lecture claim
  conservation_or_comparison:
    purpose: connects the lecture mechanism to another organism or context
  modern_extension:
    purpose: adds a recent method/application only if directly relevant
```

## M. Must Use / Can Use / Do Not Use

For every essay question:

```yaml
KnowledgeUseDecision:
  must_use:
    - lecture-core facts without which the answer is incomplete
  should_use_if_space:
    - useful experiments, examples, or contrasts
  optional_extra_reading:
    - one verified extension that improves sophistication
  do_not_use:
    - unrelated lecture material
    - unsupported student notes
    - excessive background
    - unverified citations
    - details outside the question scope
```

The aim is not to reach 1000 words. The aim is to answer efficiently with all relevant unit content.

## N. Genome Essay-Quality Contribution Benchmark

When the Genome benchmark fixture is supplied, the workflow must use it to validate generic Example Essay Mode behaviour:

- extract BIOL21101 lecture/module structure from the deck title, unit code, slide titles, and learning objectives;
- preserve first-to-last lecture order;
- identify lecturer/module boundaries;
- distinguish transcription regulation, chromatin regulation, replication, mutation/repair, protein synthesis, RNA processing/turnover/interference, non-coding RNA, transposons, and organellar gene expression;
- produce essay-style knowledge paragraphs, not slide summaries;
- use exemplar images only for style and paragraph logic;
- ignore Chinese annotations in images;
- use additional reading only when verified and directly useful.

These questions and molecular details are regression assertions only. They must not become default content or prediction evidence for another unit.

Benchmark questions:

1. `Contrast prokaryotic and eukaryotic responses to environmental signals.`
2. `Contrast DNA replication initiation between humans and E. coli.`
3. `Explain how eukaryotic translation initiation is regulated.`
4. `Explain how chromatin structure contributes to regulation of transcription.`

Regression-only Genome logic checks:

- Environmental-response comparison should compare direct prokaryotic transcriptional control and coupled transcription-translation with eukaryotic compartmentalisation, signalling cascades, mRNA selection, and translation-initiation control. Lecture examples may include CRP/catabolite repression, OmpC/OmpF/EnvZ/OmpR/micF, trp attenuation, mTOR/4E-BP/eIF4E, and AAP-mediated Arg-2 control if verified from slides.
- Replication initiation comparison should compare E. coli OriC/Dam/SeqA/DnaA/DnaB/DnaG/DNA polymerase III logic with eukaryotic ORC/Cdc6/Cdt1/MCM licensing, CDK/DDK activation, chromatin-dependent origin selection, replication timing, and polymerase specialisation where slide-supported.
- Translation initiation essays should distinguish scanning/AUG selection, eIF2 activity, eIF4E/4E-BP, mTOR signalling, uORFs, and mRNA-specific repression when relevant.
- Chromatin transcription essays should explain nucleosome constraint, histone modification, chromatin remodelling, FACT, locus control regions, insulators/barriers, and transcription factories only when within question scope.

## O. Developmental Biology Essay-Quality Contribution Benchmark

When the Developmental Biology benchmark fixture is supplied, the workflow must use it to validate mechanism-evidence-consequence essay construction, experimental evidence placement, and Section A/B separation. The Drosophila, Hox, segmentation, and vertebrate examples below are non-transferable content outside this regression context.

Test A: `Explain how Drosophila segmentation is established and refined during embryogenesis.`

Expected order:

1. segmentation as an early AP patterning problem;
2. syncytial blastoderm context;
3. maternal determinants, including Bicoid, Nanos, and Hunchback;
4. Bicoid as maternal anterior morphogen with maternal-effect evidence;
5. gap genes converting gradients into broad domains through activation/repression and cross-regulation;
6. pair-rule genes converting broad domains into periodic parasegmental stripes, including stripe-specific enhancers such as even-skipped stripe 2 if appropriate;
7. segment-polarity genes stabilising parasegment boundaries and anterior/posterior compartments;
8. conclusion linking transient parasegments to later segmental patterning.

Hard checks:

- do not say segment-polarity genes directly convert parasegments into true segments;
- do not say Hox genes create the segments;
- do not omit experimental evidence;
- do not treat Bicoid as the only AP determinant;
- include Hunchback's maternal and zygotic sources when relevant;
- include Nanos repression of maternal hunchback translation when relevant.

Test B: `Discuss how Hox genes regulate segment identity, using GOF and LOF evidence.`

Hard checks:

- do not say Hox genes are segmentation genes;
- do not imply all homeobox genes are Hox genes;
- do not imply all homeotic genes are homeobox genes;
- do not say Ubx merely cooperates with Antp in T3; Ubx rewrites/represses anterior Hox programmes and specifies T3/haltere identity;
- if using `C1-C3`, call them cephalic/head segments;
- explain posterior prevalence as posterior Hox dominance over anterior Hox function through repression/co-regulation of downstream targets.

Test C: `Compare Drosophila and vertebrate segmentation.`

Expected logic:

- Drosophila: simultaneous subdivision of existing space; maternal gradients; gap/pair-rule/segment-polarity hierarchy.
- Vertebrates: sequential somite budding; segmentation clock; Notch/Hairy oscillation; FGF8/RA wavefront; Eph/Ephrin and N-cadherin for physical boundary formation when slide-supported.
- Similar gene families may appear in different mechanistic contexts.
- Do not present vertebrate segmentation as a direct copy of Drosophila segmentation.

## P. Output Contract For Example Essays

When explicitly requested, output:

```yaml
ExampleEssayOutput:
  predicted_or_requested_question:
  question_deconstruction:
  lecturer_intent_analysis:
  knowledge_inventory:
  paragraph_plan:
  extra_reading_insert:
  high_score_example_essay:
  paragraph_function_map:
  lecture_knowledge_used:
  excluded_content:
  examiner_fit_checklist:
    - lecture_objectives_covered:
    - named_examples_used:
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
  manifest: example_essay_manifest.json
  source_audit: example_essay_source_audit.json
  per_essay_source_maps:
    - EE01_source_map.json
  per_essay_qa:
    - EE01_qa.json
  optional_zip: Example_Essays_DOCX.zip
```

Every DOCX must use A4, 2.5 cm margins on all sides, Arial 10 pt body, 1.5 line spacing, 0 pt paragraph spacing before/after, justified body text, centered title, and left-aligned subtitles/headings.

For Excel, never place the whole essay into one cell. Excel paragraph-row output is an optional audit export only when explicitly requested, not the primary Example Essay deliverable.

## P2. DOCX-First Example Essay Mode

When Example Essay Mode is explicitly requested, the final output must be standalone Word documents, not Excel essay rows.

For each essay, run this internal sequence:

1. Question Analysis.
2. Lecture Slide Scope Detection.
3. Lecture Slide Reading.
4. Lecture Logic Reconstruction.
5. Citation Detection from relevant lecture slides.
6. Citation Original Source Resolution and Reading.
7. Extra Reading Book Chapter Matching.
8. Extra Reading Chapter Reading.
9. Paragraph Plan.
10. Highlight Plan.
11. Draft Essay.
12. Source-to-run Mapping.
13. DOCX Generation.
14. DOCX Format Linting.
15. Render / visual QA.
16. Source Audit JSON.

The final essay must visibly follow the lecture's biological logic.

Lecture logic means:

- the essay begins from the biological problem or principle established by the lecture;
- body paragraphs follow the mechanism / evidence / consequence sequence taught by the lecture;
- named examples are those emphasised in the lecture;
- experimental evidence is placed where the lecture uses it to support a claim;
- conclusions synthesise the lecture argument rather than adding unrelated external material.

Do not write a generic essay from general knowledge.

Every body paragraph must have:

- at least one lecture-slide anchor;
- one clear claim;
- mechanism or evidence development;
- a link back to the essay question.

Extra Reading may contribute only 10-15% of total essay words and must be highlighted yellow.

Citation-original-source material must include an in-text citation and be highlighted green.

Before generating a Word document, the essay text must pass content checks:

1. Lecture-source check: every main claim is traceable to lecture slides or official course material, and every paragraph has lecture anchors.
2. Lecture-logic check: essay order reflects lecture logic unless the question requires comparison/evaluation reordering; if reordered, the source audit records why.
3. Citation check: all green source claims are based on read citation originals and contain in-text citation.
4. Extra Reading check: relevant chapter found, 10-15% yellow-highlighted content, no unrelated external content.
5. Essay style check: no slide-by-slide narration, no bullet list as essay body, no generic textbook introduction, no unsupported claims, no overuse of external reading.

Default direct-chat summary after DOCX generation:

```text
Generated:
- Example_Essays_DOCX/EE01_<title>.docx
- Example_Essays_DOCX/example_essay_manifest.json
- Example_Essays_DOCX/example_essay_source_audit.json

QA:
- DOCX format lint: pass/fail
- lecture grounding: pass/fail
- citation-source status: resolved/unresolved/not supplied
- extra-reading status: used/not supplied/chapter not found
```

## Q. QA Flags

Add QA flags when needed:

- `essay_question_scope_uncertain`;
- `lecturer_intent_low_confidence`;
- `paragraph_plan_missing`;
- `lecture_logic_not_preserved`;
- `causal_chain_missing`;
- `comparison_axis_missing`;
- `essay_exceeds_word_limit`;
- `example_used_as_fact`;
- `extra_reading_unverified`;
- `extra_reading_not_question_relevant`;
- `extra_reading_too_large`;
- `extra_reading_replaces_lecture_content`;
- `extra_reading_not_integrated`;
- `extra_reading_overused`;
- `recommended_reading_missing`;
- `unsupported_mechanism_claim`.

Fail safe by omitting uncertain material rather than inventing mechanisms, citations, mark schemes, or lecturer preferences.

## R. Success Condition

The workflow passes if Example Essays can explain:

- what the shared biological problem is;
- why different systems solve it differently;
- which molecular mechanisms prove the point;
- how each paragraph advances the question;
- why any extra-reading point was included.

It fails if it lists lecture facts without reconstructing the lecture's biological logic.
