# Excel Output Protocol

The integrated workflow is Excel-first for default exam-prep workbooks. Old DOCX-oriented output contracts are overridden for default workbook mode only.

Explicit Example Essay Mode is the narrow exception: complete Example Essays are DOCX-first and follow `example_essay_docx_output_protocol.md`.

External examples contribute layout adaptation rules, not fixed course layouts. If a workbook layout decision is borrowed from an example, diagnostics must record the structural reason, such as `mixed-format current paper detected`, `old/current regime split detected`, `project/scenario long-answer detected`, or `slide-image alignment required`, not the example identity.

## Default Student-Facing Workbook

Default user-facing output is a single-sheet workbook with one visible table-like map:

- Sheet name: `Exam_Prep_Map`.
- No evidence/provenance columns in this sheet.
- Evidence-level detail may be preserved in diagnostics JSON or a separate evidence workbook.
- Do not add `Summary_QA`, `Excluded_Slides_QA`, `KP_Index`, `Coverage_Audit`, or other audit sheets to the student-facing workbook unless the user explicitly requests an audit workbook.
- The sheet is organized as vertically stacked knowledge-point blocks.
- The left locator columns act as a directory while the user scrolls down.

### Screenshot-Style Layout

Use the screenshot logic for simple essay-style source sets:

| Region | Columns | Required content |
| --- | --- | --- |
| Locator | A:B | Module/block, lecture title, knowledge-point number/title, exam type label. Omit lecturer unless the user explicitly asks for it. |
| Lecture slides | C:G | Original lecture slide images for the current knowledge point, pasted directly into the workbook. Use several relevant slides/pages when needed. |
| Explanation | H:J | Student-facing essay-style explanation in academic English. Use readable paragraphs, not dense unbroken text. |
| Prediction / prep | K:N | If essay exam: predicted practice essay questions only by default. If short-answer exam: likely archetypes and mark-producing answer skeletons. If MCQ exam: discriminator axes, distractor families, and traps. |

For mixed-format source sets, prefer the same minimal six-column layout when it can express the answer product clearly:

`Pages`, `Lecture / Module`, `Knowledge Point`, `Original PPT Page` or `Original Page Image`, `Essay-Style Synthesis`, and `Exam-Facing Prep`.

If backward compatibility keeps the old header `Essay-Style Sequential Explanation`, define `sequential` as the causal, mechanistic, or argument sequence inside the biological explanation. It does not mean slide/page sequence.

Only if the user explicitly asks for an expanded audit-style workbook, use this generic visible table layout:

| Column(s) | Required content |
| --- | --- |
| A | Module |
| B | Lecture |
| C | Lecturer |
| D | KP ID |
| E | Knowledge Point |
| F | Slide/Page Range |
| G:J | Original Slide Image Area |
| K:N | Student-facing Explanation |
| O:Q | Exam-facing Prediction Area |
| R | Student Positioning Notes |

The label for O:Q must be selected automatically after exam-format parsing:

- Essay: `Predicted Essay Question / Essay Archetype`
- Short Answer: `Likely Short-Answer Form / Mark-Producing Answer Schema`
- MCQ: `Likely Statement Trap / Discriminator / One-line Rule`
- Problem/Data: `Likely Data-Problem Archetype / Graph-Reading Operation / Mechanism Inference`
- Long-Answer Project: `Likely Project Operation / Method-Readout-Interpretation / Control`

For mixed-format source sets, apply layout rules from parsed paper structure:

- If the paper contains mini-essay plus data/problem sections, O:Q must support both mini-essay prompts and data/problem archetypes.
- If the paper contains a short conceptual section plus a major essay section, O:Q must distinguish short conceptual prompts from major essay prompts.
- If old and current regimes differ, O:Q must label old-regime schemas as coverage/schema evidence and current-regime prompts as prediction evidence.
- If the paper contains project/scenario long-answer parts, O:Q must show project operation, method principle, expected readout, interpretation, and control/limitation.

Every knowledge-point block should contain:

- a concise block header;
- one or more original slide/page images;
- the explanation immediately to the right of those slides;
- the predicted practice question or question-type-specific prep output further right.

Continue stacking blocks downward. Do not create a separate sheet per lecture for the default student-facing workbook.
Do not include page-function labels such as `content`, KP-chain IDs, chain-order values, sequence-locator prose, raw extracted slide text, OCR status, slide titles, or provenance columns in the student-facing sheet.

Reusable layout lessons:

- Use slide-image alignment when explanations require visual source inspection.
- Separate mini-essay and data/problem preparation when a paper contains both.
- Separate short conceptual prompts from major essay prompts when section structure requires it.
- Label old-regime schemas as coverage/schema evidence when old and current formats differ.
- For project/scenario long answers, show operation, method principle, readout, interpretation, and control/limitation.
- Paragraph-row splitting applies only to optional Excel/evidence audit exports when full Example Essays are explicitly requested; the primary full Example Essay deliverable is standalone DOCX.

These lessons are reusable only when target evidence has the matching structural condition. Benchmark topics and example content must not appear in a target workbook unless independently present in the target sources.

### Visual Formatting

- Font: Arial.
- Main block headings: bold 13-14 pt.
- Body: 10-11 pt.
- Wrapped text.
- Freeze the first row and locator columns.
- Use wide image columns and stable row heights.
- Avoid excessive blank space.
- Do not put full essays into one cell.
- If a knowledge point requires multiple slides, stack those slide images within the same block.
- Use pale fills only to distinguish locator, slide, explanation, and prediction regions.
- Keep the sheet printable/readable at normal zoom.
- Preserve original image aspect ratio. Do not stretch slides to fit a cell region if this distorts text, diagrams, graphs, or molecular/biological shapes.
- Decide image size first, then tune adjacent font sizes, merged text blocks, row heights, and column widths around the fixed image geometry.
- Keep slide image and explanation horizontally aligned for the same KP.
- Minimise blank space, but do not shrink images or text below readable size.
- Verify rendered previews at top, middle, and late workbook positions when the workbook is long.

### Content Rules

- Paste original slide/page images, not only extracted text.
- Do not hide evidence inside comments or footnotes in the student sheet.
- Do not include source-anchor/evidence columns in the student sheet.
- Exclude non-informative navigation pages from the student-facing workbook: lecture home/title pages, recommended-reading pages, pure `Content`/agenda/outline pages, section-divider title pages, learning-objective pages, resources-only pages, admin/project-logistics pages, blank pages, and end/interactive prompt pages.
- Retain slides with examinable mechanisms, equations, data figures, case studies, comparisons, experimental results, or crop examples even when OCR/extracted text is weak; the original slide image is then the source evidence.
- Label all predicted questions as `Predicted practice question`.
- For essay exams, do not include example essays unless explicitly requested.
- For short-answer and MCQ exams, show the operational preparation product: answer schemas or discriminator/trap banks.
- For non-essay long-answer/project exams, show the project operation and answer logic: method choice, expected readout, interpretation, and control/limitation. Do not label it as a broad essay prompt.
- Preserve lecture-slide order from first slide/page to last. The workbook may group several consecutive slides into one KP, but it must not jump only to high-yield slides and skip the rest.
- KP blocks must not be too coarse or too fine: split by examinable mechanism, process chain, experimental-evidence block, data-operation block, or essay paragraph block.
- When adjacent slides have similar or repeated content, merge them into one KP block and write a fuller essay-style sequential explanation that synthesises the whole group rather than repeating one short explanation per slide.
- The explanation cell must not narrate slide-by-slide using phrases such as `Page X shows...`; it should read like one coherent concept-first paragraph for the whole KP.
- If the output is requested as Essay-Ready, the explanation must be directly writable as an exam paragraph: no meta-advice, no `strong answer should`, no `essay point`, and no references to the workbook or slide sequence.

### Student-Facing Synthesis Column

The preferred visible header is `Essay-Style Synthesis`.

The explanation column must contain the paragraph itself, not commentary about how to write the paragraph. It must be concept-first prose:

```text
topic sentence -> causal/mechanistic development -> selected named example/evidence -> consequence or exam-relevant link-back
```

It must not preserve coverage by mentioning every page. Coverage is already handled by page ranges, original slide/page images, coverage audit, and diagnostics.

Hard-banned output patterns in the student-facing explanation column:

- `Page X first establishes`
- `Page X then develops`
- `Page X closes`
- `Pages X-Y should be read as`
- `KP covers pages`
- `slide sequence should be read as`
- `remaining linked pages`
- `the first part of the sequence establishes`
- `the later pages add`
- `In an essay answer, use these pages`
- `Turn pages X-Y into one paragraph`
- `central idea for this block`
- `central examinable idea in this knowledge block`
- `should be understood as`
- `best written as`
- `is mainly an argument about`
- `lecture develops it across slides`
- raw OCR fragments or bullet dumps

The same rule applies to semantically equivalent variants, including `slide X`, `these slides`, `this block should be read as`, or repeated prose that names three or more pages/slides in one paragraph.

If the source material is weak-OCR or image-heavy, keep the original image and flag the uncertainty in diagnostics. Do not write `no reliable extracted text` or use OCR debris as the student-facing synthesis.

### Exam-Facing Prep Column

`Exam-Facing Prep` should contain actual preparation products:

- predicted practice questions;
- answer operations;
- comparison axes;
- data/problem prompts;
- mark-producing schemas;
- MCQ discriminator axes;
- short-answer skeletons;
- method/readout/control prompts.

It must not say `Turn pages X-Y into one paragraph`, `use these pages`, or similar coverage-to-writing instructions.

## Optional Evidence Workbook

The evidence workbook is optional and audit-oriented. It may contain the detailed sheets below when useful or when explicitly requested. Keep it separate from the single-sheet student workbook.

## Example Essay Mode Boundary

When Example Essay Mode is explicitly requested:

- the primary output is standalone DOCX files, one per essay;
- Excel paragraph-row output is optional audit output only;
- do not put full essays into the student-facing visual workbook;
- if an index is useful, create a small `Example_Essay_Index` sheet or JSON manifest listing essay ID, question, DOCX filename, lecture anchors, citation status, extra-reading status, and QA status.

## Required Workbook Sheets

Evidence workbook may contain:

- `00_README`
- `01_Source_Inventory`
- `02_Exam_Format_Diagnosis`
- `03_Lecture_Module_Map`
- `04_Knowledge_Point_Map`
- `05_Past_Paper_Question_Map`
- `06_Examiner_Patterns`
- `07_Prediction_Dashboard`
- `08_MCQ_HighFreq_Statements`
- `09_ShortAnswer_Predicted_QA`
- `10_Essay_Predicted_Questions`
- `11_Example_Essays` only as an optional audit/index sheet for DOCX outputs, not as the primary full-essay deliverable
- `12_Figure_Plans`
- `13_Extra_Reading`
- `14_QA_Flags`

When explicit example-answer generation is requested for non-essay long-answer/project exams, the evidence workbook may also contain:

- `11_Example_Long_Answers`
- `12_Paragraph_Plans`
- `13_Extra_Reading_Integration`

Each long-answer paragraph row must include:

- `question_part`;
- `paragraph_text`;
- `paragraph_function`;
- `lecture_kps_used`;
- `scenario_facts_used`;
- `method_readout_interpretation`;
- `extra_reading_use`;
- `why_included`;
- `excluded_content`.

Do not put a complete long answer into one cell. Split it by paragraph and, where useful, by question part.

## Formatting

- Font: Arial.
- Body font: 10 or 11 pt.
- Main section headers: bold, 13-14 pt when practical.
- Use wrapped text.
- Freeze top row and first key columns.
- Add filters to all tables.
- Avoid one giant paragraph cell.
- Long essays must be split by paragraph rows only when the user explicitly requests an Excel audit/export version. Complete Example Essays use standalone DOCX as the primary deliverable.
- Cap column widths; text-heavy columns should be readable but not extreme.
- Use row height only as needed; avoid excessive blank rows.
- Use bold subheadings.
- Keep source-anchor columns visible.
- Use separate sheets for dense essay text and dashboards.

## Example-Pack Layout Cues

When bilingual or Chinese example packs are supplied, keep one examinable point/topic per row and add optional sortable columns where useful:

- `Topic CN`
- `Topic EN`
- `Priority marker`
- `Past paper years/Qs`
- `Common distractor/trap`
- `Calculation/diagram flag`
- `Evidence caveat`

Treat `Tier 1`, `Tier 2`, `Core`, `Anchor`, `>75%`, and `50-75%` as sortable priority values.

## QA_Flags Sheet

Must include:

- weak OCR;
- unreadable file;
- unsupported file;
- ambiguous question type;
- missing slide evidence;
- answer not found in lectures;
- unverified citation;
- low-confidence prediction;
- old paper excluded from prediction.
- long-answer project written as generic essay;
- missing method principle;
- missing expected readout;
- missing interpretation;
- missing control or limitation.

## Visual QA

Before delivery:

- inspect at least the first 20 rows of every sheet;
- render or otherwise visually check main text sheets;
- check no essential headers/text are clipped;
- check predictions are visibly labelled as predicted practice questions;
- check unsupported claims are labelled or omitted.
