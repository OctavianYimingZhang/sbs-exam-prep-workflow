# Example Essay DOCX Output Protocol

## Trigger

Use this protocol when Essay Exam Prep or Example Essay Mode is explicitly requested by the user, such as `essay preparation`, `Example Essay`, `model essay`, `full essay-style answer`, or an equivalent request for complete essay answers/documents.

Do not trigger this DOCX protocol for MCQ, short-answer, long-answer/project/scenario, prediction-only, or ordinary lecture-walkthrough requests.

The normal default lecture-review workflow is `knowledge_walkthrough_docx`. Essay prep is a DOCX add-on built on top of the lecture walkthrough unless the user explicitly opts out.

## Primary Output

Default essay-prep output is one module-level Word document:

- `Essay_Module_Example_Essays.docx`

It should contain the selected examinable modules, one or more full Example Essays where support is sufficient, adaptation maps, and reusable paragraph banks.

If the user explicitly asks for separate essay files, each Example Essay may instead be exported as one standalone `.docx` file.

If separate essay files are requested and N Example Essays are generated, produce N Word documents:

- `EE01_<short_safe_question_title>.docx`
- `EE02_<short_safe_question_title>.docx`
- `EE03_<short_safe_question_title>.docx`

Also produce:

- internal QA artefacts for validation, such as `example_essay_manifest.json`, `example_essay_source_audit.json`, source maps, QA JSON, and citation-resolution logs.

Do not place a complete essay into one Excel cell. Do not create an Excel workbook as the ordinary essay-prep output. Excel paragraph-row output is allowed only as an internal or explicitly requested audit artefact.

Final user-facing output may include the requested final artefacts, such as `Essay_Module_Example_Essays.docx`, separate Example Essay DOCX files, or another explicitly requested final format. Do not return or package helper JSON, source maps, manifests, source-audit files, render previews, or citation-resolution logs unless the user explicitly asks for an audit package.

## Word Document Formatting

Apply these settings to every generated DOCX. Leave all other Word settings at their defaults unless the user specifies otherwise.

Page:

- Top margin: 2.5 cm.
- Bottom margin: 2.5 cm.
- Left margin: 2.5 cm.
- Right margin: 2.5 cm.

Font:

- Arial.
- Font size: Word default unless the user specifies a size.
- Title: Arial, bold allowed, centered.
- Subtitle / section heading: Arial, bold allowed, left aligned.
- Body: Arial.

Paragraph:

- Line spacing: 1.5.
- Body alignment: justified.
- Title alignment: centered.
- Subtitle / section heading alignment: left.
- No empty spacer paragraphs.

Structure:

- Title paragraph.
- Optional subtitle paragraph containing the essay question.
- Numbered section headings if useful, matching the reference style:
  - `1 Introduction`
  - `2 Main mechanism / argument`
  - `2.1 Subsection`
  - `3 Evaluation / synthesis`
  - `4 Conclusion`
- Body paragraphs written as continuous essay prose.
- Figure captions only if figures are explicitly included or requested.

## Essay Language Contract

Every generated essay must pass the shared prose-quality rules in `language_quality_contract.md` and the orchestration checks in `essay_generation_protocol.md`.

Required paragraph logic:

```text
claim -> mechanism/process/evidence -> scope or limitation -> consequence -> link back
```

Language rules:

- Start with the answer, not with generic metacommentary.
- Compress repeated or low-value detail without deleting required academic mechanisms.
- Remove lecture-route narration and exam-guidance phrasing from the essay body.
- Use examples as evidence for a broader claim, not as disconnected case descriptions.
- Convert evidence-heavy examples into `evidence -> mechanism -> interpretation -> limitation`.
- Make contrasts explicit and non-ambiguous.
- Keep citations minimal and sufficient; support theory, mechanisms, data, experiments, or non-obvious generalisations.
- Calibrate citation strength; do not write support, association, or mechanistic plausibility as sole-cause proof.
- Do not cite-stack.
- Omit unsupported claims rather than inventing citations.
- Conclude by synthesis, not by adding new content.

## Highlighting Rules

Use Word highlight, not font colour.

Highlight mapping:

- Extra Reading Books content: yellow highlight.
- Lecture-slide citation original-source content: green highlight.
- Verified classic-experiment fallback content: green highlight.

Implementation mapping:

- Extra Reading Books: `WD_COLOR_INDEX.YELLOW`
- Cited original papers / theories / experiments from lecture-slide citations, plus verified classic-experiment fallback sources: `WD_COLOR_INDEX.BRIGHT_GREEN`

Rules:

- Yellow highlight is applied only to content derived from Extra Reading Books or chapters uploaded by the user.
- Green highlight is applied only to content derived from original citation sources identified from lecture slides and then read or verified, or from verified classic-experiment fallback sources used because lecture slides contained no usable citations.
- If a sentence uses a lecture-slide cited original source, include an author-year in-text citation and highlight the full cited-source-derived clause or sentence green, including the citation.
- If a sentence uses Extra Reading Books, highlight the extra-reading-derived phrase or sentence yellow.
- If a paragraph contains both lecture content and extra-reading content, highlight only the extra-reading portion yellow.
- If a paragraph contains both lecture content and cited-original-paper content, highlight only the cited-original-paper portion green.
- Do not highlight ordinary lecture-slide content.
- If content could belong to both Extra Reading and cited original-source categories, prefer the more specific mapping:
  - source from lecture-slide cited original paper = green;
  - source from uploaded Extra Reading Book = yellow.
- Do not use green highlight for citations copied from secondary sources unless the original cited source was read.
- Do not use yellow highlight for generic textbook knowledge unless it came from the uploaded Extra Reading material.

## Highlight Relevance Gate

Highlighting does not justify inclusion. A yellow or green phrase may appear only if the sentence also passes the PPT/source-anchor and question-relevance gate.

Reject highlighted content when:

- it is accurate but not needed for the essay question;
- it creates a molecular, channel, receptor, gene, pathway, method, case, or example list not present in the PPT/source logic;
- it increases Extra Reading ratio by replacing rather than sharpening lecture-derived claims;
- it makes revision harder without improving answer precision;
- it has no paragraph function beyond raising citation or Extra Reading density.

## Micro-Detail Highlighting

When the Micro Extra Reading Enhancement Pass inserts a short named detail into an otherwise lecture-derived sentence, the DOCX must preserve the source boundary at run level.

Rules:

- highlight only the inserted phrase or shortest source-derived clause;
- do not highlight the full sentence if most of the sentence is lecture-derived synthesis;
- yellow is valid only for an inserted phrase from an uploaded recommended book or matched textbook chapter/section;
- green is valid only for an inserted phrase from a verified lecture-cited original source or verified classic/academic source;
- ordinary lecture-derived precision receives no highlight;
- unverified remembered details and exemplar-only details are rejected, not highlighted.

Micro-detail insertions must remain short in function, not by a fixed word count. The addition should read as a phrase or short clause inside the original sentence. If the detail needs a new explanatory sentence, introduces a second argument, or dominates the lecture-derived sentence, it is not a micro-detail insertion and must go through normal paragraph planning.

Each micro-detail run in the source map should record:

```yaml
micro_detail_insert: true
original_phrase:
inserted_phrase:
parent_ppt_or_source_slot:
question_function:
source_type:
source_anchor:
highlight:
word_count:
claim_delta: precision_only
qa_status:
```

Fail or flag the essay if:

- a micro-detail insertion has no source anchor;
- a micro-detail insertion has no parent PPT/source slot;
- a micro-detail insertion is long enough to become a new explanation or second argument;
- a micro-detail insertion has a source type that does not match its highlight colour;
- a micro-detail insertion changes the original claim instead of making it more precise;
- a highlighted span is broader than the source-derived insertion;
- the insertion pushes Extra Reading above the allowed ratio.
- the insertion is true but not needed for the question.

## Extra Reading Ratio

If relevant Extra Reading Books are uploaded:

- integrate Extra Reading content into the essay;
- target 10-15% of total essay body word count;
- count only yellow-highlighted words as Extra Reading content;
- do not include more than 15% unless the user explicitly requests more external material;
- if no relevant chapter can be found, flag `extra_reading_chapter_not_found` and do not invent.

If Extra Reading Books are not uploaded:

- do not fabricate extra reading;
- set `extra_reading_status = not_supplied`.

## Citation-Source Integration

If the user does not provide citations for Example Essay generation, the workflow must perform citation discovery:

1. inspect relevant lecture slides for citation information;
2. resolve and read lecture-slide cited originals where possible;
3. if no usable slide citation exists, search for several classic experiments or landmark primary studies directly tied to the lecture mechanism.

If the relevant lecture slides contain citations:

- parse all citations on slides used by the essay;
- resolve them to original papers, books, theories, or experiments where possible;
- read the original source before adding source-derived content;
- insert author-year in-text citations;
- highlight source-derived content green;
- record the citation in the source audit.

If a citation cannot be resolved or the original source cannot be read:

- do not use content from that citation;
- do not add a green-highlighted sentence;
- add QA flag `citation_original_unreadable`;
- list the unresolved citation in `example_essay_source_audit.json`.

If the relevant lecture slides contain no usable citations:

- perform targeted academic search using lecture terms, mechanism names, model systems, methods, and named experiments;
- prefer primary experimental papers with DOI/PubMed/publisher records;
- use authoritative reviews only for orientation unless the paragraph claim is review-level;
- record `lecture_slide_citation_absent_classic_experiment_search_required` internally;
- insert only verified, read classic-experiment content, with author-year citation and green highlight.

## Source Hierarchy

Essay content must be built in this order:

1. Relevant lecture slides.
2. Official lecture notes / official course handouts.
3. Formal exam question wording or predicted practice question prompt.
4. Lecture-slide cited original sources, only after reading them.
5. Verified classic experiments found because no usable lecture-slide citation exists.
6. Uploaded Extra Reading Books, only relevant chapters/sections.
7. Other peer-reviewed or textbook sources only if explicitly allowed or needed for citation resolution.

Extra Reading and citation-source content must enrich the lecture answer, not replace it.

## Lecture Grounding

No Example Essay may be drafted before the relevant lecture slides have been read, mapped, and converted into a lecture-logic plan.

Every body paragraph must have:

- at least one lecture-slide anchor or official course-material anchor;
- one clear claim;
- mechanism or evidence development;
- a link back to the essay question.

The final essay must visibly follow lecture logic:

- the essay begins from the biological problem or principle established by the lecture;
- body paragraphs follow the mechanism / evidence / consequence sequence taught by the lecture;
- named examples are those emphasised in the lecture;
- experimental evidence is placed where the lecture uses it to support a claim;
- conclusions synthesise the lecture argument rather than adding unrelated external material.

## Fail Conditions

Fail DOCX generation or mark the essay as non-compliant if:

- no relevant lecture slides were read;
- a body paragraph has no lecture-slide or official course anchor;
- Extra Reading content exceeds 15% without user instruction;
- yellow-highlighted content lacks an Extra Reading source anchor;
- green-highlighted content lacks an in-text citation;
- green-highlighted content is not linked to a read original citation source;
- classic-experiment fallback content was used without verification or without direct relevance to the paragraph claim;
- margins, font family, line spacing, title alignment, subtitle alignment, or body justification fail the DOCX linter;
- the essay is generic and not traceable to lecture logic;
- the essay contains slide/page narration, repeated filler, unsupported claims, citation stacking, or examples used as standalone case detail rather than evidence for the answer;
- the essay contains lecture-route narration, exam-guidance phrasing, or citation-strength overclaiming;
- the essay contains true-but-not-needed detail, review-style drift, or a channel/receptor/gene/pathway catalogue without analytic use;
- compression changes claim scope, causal strength, model boundaries, or experimental interpretation;
- a citation printed on a slide is copied into the essay without resolving and reading the original source;
- an uploaded formatting PDF or style exemplar is used as biological content.

## User-Facing Output Contract

When the user asks for Example Essays, return paths in this form:

```text
Generated:
- Example_Essays_DOCX/EE01_<title>.docx
- Example_Essays_DOCX/EE02_<title>.docx
```

The user should not need to manually reformat the Word documents.
