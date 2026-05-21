# Evidence Policy

## Source Priority

Use sources in this order:

1. exact lecture slides supplied by the user;
2. official course notes, handouts, practice materials, and exam guidance supplied by the user;
3. exact formal past papers supplied by the user;
4. marking criteria, exemplar answers, and essay tutorials supplied by the user;
5. official university or publisher material;
6. peer-reviewed papers, reviews, textbooks, PubMed, Google Scholar, DOI/publisher pages.

Do not use social media, influencer content, Q&A/content platforms, generic web summaries, or unproven traditional medicine claims.

## Example Essay Evidence Classes

```yaml
EvidenceUse:
  lecture_slide_core:
    meaning: relevant lecture slide content
    highlight: none
    allowed_use: primary essay factual content and answer logic

  extra_reading_book:
    meaning: uploaded textbook/book/chapter material supplied by the user for enrichment
    highlight: yellow
    allowed_use: 10-15% of Example Essay body if relevant chapter/section is found

  lecture_slide_citation_original:
    meaning: original paper/book/theory cited on relevant lecture slides and read by the Skill
    highlight: green
    allowed_use: brief evidence or mechanism refinement with author-year in-text citation

  docx_format_reference:
    meaning: user-supplied PDF/image showing desired Word layout, highlighting, captions, or citation style
    highlight: none
    allowed_use: formatting and style only, not biological content
```

Hard rules:

```text
Lecture slides control the answer logic.
Extra Reading Books may refine the answer but must not displace the lecture sequence.
A citation printed on a slide is not enough. The cited original source must be resolved and read before any content from that source is inserted into the essay.
Do not copy author-year citations from slides into the essay unless the cited source has been resolved and the relevant claim verified.
If a cited source cannot be read, omit source-derived details and flag the unresolved citation.
If Extra Reading Books are uploaded, locate the relevant chapter/section before using them. Do not cite or highlight a whole book vaguely.
Formatting reference PDFs are layout/style evidence only and must not supply biological claims.
```

## Unit Example Evidence Use

Unit-specific examples are not reusable factual evidence for other units. Classify every example source into one of these source-use classes before it can influence a workflow:

- `unit_content_evidence_only`: target-unit lecture slides, official notes, formal papers, or guidance that may support factual content for that same target unit.
- `unit_regression_example`: named benchmark material used to test whether the Skill behaves correctly on a known fixture.
- `generic_workflow_contribution`: a non-target unit example distilled into a transferable workflow rule, output pattern, QA check, or evidence-handling discipline.
- `style_only_exemplar`: exemplar answer, essay draft, handwritten example, or image used only for wording, structure, density, answer organisation, and paragraph logic.
- `non_transferable_content`: unit topics, named systems, lecturer-specific preferences, exact year recurrence, or biological details that must not be reused outside the source unit unless independently present in the target unit's own sources.

Hard rule:

```text
Do not use a Unit example as content evidence for another Unit.
A Unit example may only contribute workflow logic, output style, archetype structure, QA checks, or evidence-handling discipline.
```

If a workflow applies a lesson learned from a benchmark unit, record the structural trigger from the target unit evidence, not the benchmark unit name alone. For example, record `current paper contains mini-essay plus data/problem sections`, not `Plant Biology-like`.

## ExtraReadingVerifier

- Use only peer-reviewed reviews, primary papers, textbooks, official course-recommended readings, PubMed/Google Scholar/DOI/publisher pages.
- Verify author surname and year before using in-text citations.
- Never copy citations from exemplars without independent verification.
- If unverified, place under `Needs verification` and do not insert into essays.

Extra Reading source priority:

1. official recommended reading listed in lecture slides, Canvas reading list, course notes, or lecturer guidance;
2. textbook or book chapter used by the unit if explicitly supplied;
3. papers, reviews, datasets, methods, or book chapters explicitly named in the lecture slides;
4. if no official book/reading is supplied, ask whether the user has a recommended book or reading list;
5. if unavailable, use peer-reviewed reviews, primary papers, textbooks, PubMed, Google Scholar, DOI pages, or publisher pages.

Extra reading may be inserted into essays only as:

- one short enrichment paragraph;
- one precise sentence inside a mechanism paragraph;
- one comparison point that sharpens the lecture argument;
- one evidence-based example that strengthens the lecture mechanism.

It must not replace lecture content, exceed 15% of the essay, introduce an unrelated mechanism, contradict slides without explanation, or appear without verified source anchoring. In explicit Example Essay Mode, uploaded Extra Reading Book content should be 10-15% of body words when a relevant chapter/section is found, and those words must be yellow-highlighted.

For non-essay long-answer/project answers, extra reading should be one compact refinement only. It may support a named method example, clarify a limitation, justify a technique choice, or add directly relevant method context. It must not become a second answer.

## Exemplar Distillation

Use exemplar answers for:

- answer structure;
- paragraph grammar;
- comparison strategy;
- density and tone;
- strong vs weak answer pattern detection.

Do not use exemplar biological claims as factual authority unless verified from lectures or reliable sources.

For handwritten/image exemplars:

- classify them as `exemplar_image` when possible;
- use them for essay structure, paragraph logic, density, comparison strategy, and academic phrasing only;
- ignore Chinese annotations unless the user explicitly asks to use them;
- treat student Chinese annotations as non-course evidence by default;
- mark `visual_inspection_required` when handwriting or image quality limits extraction;
- never use image exemplar content as factual evidence unless verified from lecture slides, official notes, or reliable academic sources.

## Hard Negatives

Do not:

- pool content prediction evidence across different units;
- pool old and new exam regimes as if they were one statistical distribution;
- treat topic frequency as sufficient evidence when archetype/slot grammar contradicts it;
- infer lecture deck years from citation/reference years embedded in slide text;
- silently resolve conflicts between current lecture guidance and formal past-paper format;
- invent exact graph values from image-only figures or weak OCR;
- invent missing Paper 1, Section A, answer-key, mark-scheme, or official-answer content;
- invent an exact exam-regime transition year when files are missing between regimes;
- treat every past-paper question as essay;
- let Section A contaminate essay prediction;
- use short-answer papers as direct essay prediction evidence;
- use exemplar answers as factual authority;
- use a Unit example as content prediction for another Unit;
- write a Unit-specific instruction outside an explicit regression context;
- apply a Unit example without a matching target-unit evidence condition;
- insert unverified citations;
- insert extra reading that is not directly relevant to the exact essay question;
- let extra reading replace lecture logic;
- use more than one focused extra-reading insert unless the user explicitly requests more;
- overfill essays to reach word count;
- put full essays into single unreadable cells;
- hide source evidence in diagnostics or evidence workbooks;
- expose evidence columns in the student-facing single-sheet workbook unless the user explicitly asks for an evidence workbook;
- present predictions as official exam questions;
- apply SBS essay rubric to short-answer/MCQ answers;
- edit, rename, delete, or overwrite source files.

## Essay QA Flags

Use these flags when applicable:

- `essay_question_scope_uncertain`
- `lecturer_intent_low_confidence`
- `paragraph_plan_missing`
- `lecture_logic_not_preserved`
- `causal_chain_missing`
- `comparison_axis_missing`
- `essay_exceeds_word_limit`
- `example_used_as_fact`
- `extra_reading_unverified`
- `extra_reading_not_question_relevant`
- `extra_reading_too_large`
- `extra_reading_replaces_lecture_content`
- `extra_reading_not_integrated`
- `extra_reading_overused`
- `recommended_reading_missing`
- `unsupported_mechanism_claim`
- `unit_example_used_as_content_prediction`
- `unit_example_missing_transferable_contribution`
- `unit_example_non_transferable_content_not_marked`
- `cross_unit_content_leakage`
- `unit_specific_instruction_outside_regression_context`
- `example_claim_used_without_verification`
- `regime_example_applied_without_format_match`
- `question_type_example_applied_without_question_type_match`
- `citation_detected_on_slide`
- `citation_original_resolved`
- `citation_original_unreadable`
- `citation_original_used_without_reading`
- `green_highlight_missing_citation`
- `green_highlight_missing_source_anchor`
- `extra_reading_book_supplied`
- `extra_reading_chapter_found`
- `extra_reading_chapter_not_found`
- `extra_reading_used_without_chapter_anchor`
- `extra_reading_ratio_below_10_percent`
- `extra_reading_ratio_above_15_percent`
- `yellow_highlight_missing_source_anchor`
- `essay_paragraph_missing_lecture_anchor`
- `essay_not_tightly_lecture_grounded`
- `docx_format_lint_failed`
