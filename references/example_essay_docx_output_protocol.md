# Example Essay DOCX Output Protocol

## Trigger

Use this protocol only when Example Essay Mode is explicitly requested by the user, such as `Example Essay`, `model essay`, `full essay-style answer`, or an equivalent request for complete essay answers/documents.

Do not trigger this DOCX protocol for ordinary workbook KP explanations, prediction-only outputs, or a request for a single essay-style paragraph unless the user explicitly asks for complete Example Essay documents.

The normal default workflow remains Excel-first. This DOCX protocol does not apply to prediction-only, workbook-only, MCQ, short-answer, or ordinary revision-map requests.

## Primary Output

Each Example Essay must be exported as one standalone `.docx` file.

If N Example Essays are generated, produce N Word documents:

- `EE01_<short_safe_question_title>.docx`
- `EE02_<short_safe_question_title>.docx`
- `EE03_<short_safe_question_title>.docx`

Also produce:

- `example_essay_manifest.json`
- `example_essay_source_audit.json`
- one source map JSON per essay, such as `EE01_source_map.json`
- one QA JSON per essay, such as `EE01_qa.json`
- optionally `Example_Essays_DOCX.zip`

Do not place a complete essay into one Excel cell. Do not merge multiple complete essays into one Word document. Excel paragraph-row output is allowed only as an optional audit artefact when the user explicitly requests it.

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
- Use examples as evidence for a broader claim, not as disconnected case descriptions.
- Make contrasts explicit and non-ambiguous.
- Keep citations minimal and sufficient; support theory, mechanisms, data, experiments, or non-obvious generalisations.
- Do not cite-stack.
- Omit unsupported claims rather than inventing citations.
- Conclude by synthesis, not by adding new content.

## Highlighting Rules

Use Word highlight, not font colour.

Highlight mapping:

- Extra Reading Books content: yellow highlight.
- Lecture-slide citation original-source content: green highlight.

Implementation mapping:

- Extra Reading Books: `WD_COLOR_INDEX.YELLOW`
- Cited original papers / theories / experiments from lecture-slide citations: `WD_COLOR_INDEX.BRIGHT_GREEN`

Rules:

- Yellow highlight is applied only to content derived from Extra Reading Books or chapters uploaded by the user.
- Green highlight is applied only to content derived from original citation sources identified from lecture slides and then read or verified.
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

## Source Hierarchy

Essay content must be built in this order:

1. Relevant lecture slides.
2. Official lecture notes / official course handouts.
3. Formal exam question wording or predicted practice question prompt.
4. Lecture-slide cited original sources, only after reading them.
5. Uploaded Extra Reading Books, only relevant chapters/sections.
6. Other peer-reviewed or textbook sources only if explicitly allowed or needed for citation resolution.

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
- margins, font family, line spacing, title alignment, subtitle alignment, or body justification fail the DOCX linter;
- the essay is generic and not traceable to lecture logic;
- the essay contains slide/page narration, repeated filler, unsupported claims, citation stacking, or examples used as standalone case detail rather than evidence for the answer;
- a citation printed on a slide is copied into the essay without resolving and reading the original source;
- an uploaded formatting PDF or style exemplar is used as biological content.

## User-Facing Output Contract

When the user asks for Example Essays, return paths in this form:

```text
Generated:
- Example_Essays_DOCX/EE01_<title>.docx
- Example_Essays_DOCX/EE02_<title>.docx
- Example_Essays_DOCX/example_essay_manifest.json
- Example_Essays_DOCX/example_essay_source_audit.json
- Example_Essays_DOCX.zip
```

The user should not need to manually reformat the Word documents.
