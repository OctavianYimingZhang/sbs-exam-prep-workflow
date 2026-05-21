---
name: sbs-exam-prep-workflow
description: Excel-first top-level SBS exam preparation workflow with subagents/modules for source inventory, unit/regime grouping, lecture segmentation, archetype-centric examiner-pattern inference, MCQ discriminator analysis, short-answer schema planning, essay prediction, visual student workbook generation, evidence workbook generation, and QA from lecture slides, notes, past papers, mocks, practice materials, exemplars, and marking guidance.
---

# SBS Exam Prep Workflow

Build one top-level, Excel-first workflow. This Skill owns file routing, evidence hierarchy, workflow order, final Excel output, and QA. Existing systems such as `Past-Paper-Analysis-Skill` and `$exam-essay-prep-pack` are design references for mapping/statistics and essay writing logic; do not copy them blindly and do not inherit their Word-first output contract.

This Skill is modular and composable. Every major function can be used alone when requested, and the same functions can be chained into the full workflow. Use `references/modular_entrypoints_protocol.md` to decide module scope, dependencies, and stopping point.

The main theory is not KP hotness prediction. It is a unit-internal, question-type-separated, question-archetype-driven examiner-operation inference system:

```text
Exam blueprint -> Question archetype -> Slot grammar -> compatible knowledge points -> preparation action
```

KP posterior/hotness remains an auxiliary metric only. Do not ask first which topic is hottest; first identify whether the unit blueprint is stable, which archetypes are reused, which variable slots rotate, and which preparation action follows.

Default exam-prep output is Excel-first. Word output is generated only when explicitly requested. Explicit Example Essay Mode is the narrow exception: complete Example Essays are DOCX-first, one standalone Word document per essay, while default prediction and KP synthesis remain in Excel.

Do not help with a live exam, active assessed submission, or contract-cheating request.

## Unit Example Contribution Policy

All Unit-specific examples are regression/contribution examples, not reusable content predictions.

Each Unit example must be interpreted through three layers:

1. Observed Unit behaviour: what happened in that Unit's lecture materials, formal papers, exemplars, or answer style.
2. Generic Skill contribution: what reusable analysis capability this example teaches the workflow.
3. Transfer rule for future Units: how to recognise the same structural pattern in a different Unit without importing this Unit's content, topics, question recurrence, or lecturer-specific assumptions.

Do not write examples as `if this Unit appears, do X` unless the section is explicitly a regression test for that same Unit. In all general protocols, phrase examples as `this Unit demonstrates a transferable rule: ...`.

The Skill must never branch production behaviour on known benchmark Unit names. Unit names are allowed in fixture files, regression reports, and contribution cards only. Future Units must be routed by evidence conditions such as exam format, question family, section structure, mark weights, source role, and lecture/exam reasoning pattern.

## Mandatory References

- `references/input_processing_protocol.md`: file roles, trust levels, extraction, exam-format fields.
- `references/modular_entrypoints_protocol.md`: standalone and full-workflow entry points for each module.
- `references/question_type_protocol.md`: question-type gates, MCQ statements, short-answer layers, essay paragraph mapping.
- `references/scoring_and_pattern_protocol.md`: hotness/retention separation, primary/secondary KP mapping, lecturer/module slot detection.
- `references/kp_essay_synthesis_protocol.md`: mandatory default KP synthesis pass separating internal page coverage from visible student-facing essay paragraphs.
- `references/essay_generation_protocol.md`: explicit Example Essay Mode, lecture-logic extraction, paragraph planning, extra-reading insertion, and examiner-fit checks.
- `references/example_essay_docx_output_protocol.md`: DOCX-first output contract for explicit Example Essay Mode, including formatting, highlighting, source audit, and linting requirements.
- `references/essay_synthesis_protocol.md`: compatibility entry point for the same essay synthesis rules when a user asks for essay-style lecture knowledge.
- `references/long_answer_example_protocol.md`: non-essay project/scenario long-answer writing logic learned from method-driven benchmark examples; benchmark content is not a content template.
- `references/excel_output_protocol.md`: required workbook sheets and formatting.
- `references/subagent_protocol.md`: subagent/module responsibilities and handoff schemas.
- `references/evidence_policy.md`: source hierarchy, exemplar use, extra-reading verification, hard negatives.
- `references/cross_subject_regression_protocol.md`: contribution/regression benchmark suite; named Units validate generic workflow rules and are not content templates.

Use `scripts/extract_sources.py` for read-only source inventory and text extraction. Use `scripts/unit_grouper.py` for unit-key and exam-regime grouping. Use `scripts/archetype_models.py` as the canonical schema for archetype-centric outputs. Use `scripts/essay_style_linter.py` to validate generated workbook language before delivery when a workbook is produced. In explicit Example Essay Mode, use `scripts/generate_example_essay_docx.py`, `scripts/docx_format_linter.py`, `scripts/example_essay_source_audit.py`, `scripts/lecture_citation_resolver.py`, `scripts/extra_reading_chapter_matcher.py`, and render QA where available. Use `scripts/cross_subject_regression_check.py` for benchmark validation when regression examples are available. Use `$exam-essay-prep-pack` for essay-writing logic when available, but keep this workflow's default workbook structure intact.

## Workflow

0. **Module routing**
   - First decide whether the user requested one module, a subset of modules, or the complete workflow.
   - Follow `references/modular_entrypoints_protocol.md`.
   - If the user requests a single module, run only that module and any minimum dependency required for a valid output.
   - If the user supplies valid intermediate artefacts, use them directly rather than rerunning upstream work.
   - If the user requests the full workflow, run the modules in dependency order and produce the default deliverables.
   - Always report which modules were run, which were skipped, and which artefacts were generated.

1. **Source inventory**
   - Classify every uploaded or discovered file before analysis using the FileRole enum in `input_processing_protocol.md`.
   - Record unit code/name, year, trust level, extraction status, and allowed evidence use.
   - Record `AnalysisContext` and classify every non-target Unit example as a transferable workflow contribution, style exemplar, layout exemplar, or benchmark fixture before prediction.
   - Never infer hidden content from failed, image-only, weak-OCR, or unsupported files.

2. **Unit grouping and regime split**
   - Normalize every file to a `unit_key` before comparing papers.
   - Compare MCQ and short-answer patterns only within the same normalized unit key.
   - Do not pool content evidence across different units. Cross-unit examples may teach transferable workflow structure only, not content prediction.
   - Split formal papers into exam regimes when section structure, answer rules, timing, mark weights, or dominant question type changes.
   - Old-regime papers may provide concept-pool evidence but must not drive current-regime blueprint predictions.
   - Unit examples teach the regime-detection method; they do not license assuming the same topics, lecturers, or section pattern in future Units.

3. **Question-type gate**
   - Classify each paper and question before prediction using the QuestionType enum in `question_type_protocol.md`.
   - Never apply SBS K/C/U/A/R to MCQ, fill-blank, short-answer, or problem-based questions. Use it only for essay-based theory answers.
   - Use Unit examples only to strengthen evidence-triggered routing. Route future Units by parsed current exam format, not by similarity of biological content or Unit name.

4. **Exam-format diagnosis**
   - Parse duration, sections, answer rules, question counts, weights/marks, page/word/character limits, figure/citation rules, calculator rules, answer submission mode, penalties, and formatting requirements.
   - Formal papers drive retention and examiner-pattern inference. Practice papers, quizzes, mocks, answer keys, and exemplars may support coverage/answer style but must not change formal-year retention unless explicitly configured.
   - For every Unit example, extract reusable diagnostics such as answer-all versus answer-one, section split, mark weighting, current versus old regime, data/problem requirements, project/scenario requirements, and missing-section QA.

5. **Lecture/module segmentation**
   - Segment lecture sources by lecture number/title, lecturer, objectives, summaries, readings, module markers, and topic transitions.
   - Student handwritten annotations may help interpretation, but are not authoritative course facts unless supported by slide text, official notes, or reliable sources.
   - Select segmentation patterns from target lecture/exam evidence, such as mechanism-evidence-consequence, process chain, method-readout-limitation, data-operation, comparison-axis, or visual slide-aligned explanation.

6. **Knowledge-point optimisation**
   - Create KnowledgePoint records from examinable causal units, not from every slide.
   - A valid knowledge point must be usable as one MCQ concept, one short-answer mark cluster, one essay paragraph, or one component of an essay plan.
   - Each KP must include source anchors, examinability, linked/prerequisite KPs, likely question types, and student-facing prose.
   - Generic KP templates learned from Unit examples are reusable only as structure: mechanism -> evidence -> consequence; process input -> actors -> mechanism -> output; method principle -> scenario application -> readout -> interpretation -> control; data -> inference -> limitation -> further test; comparison axis -> mechanism examples -> synthesis.

7. **KP Essay Synthesis Pass**
   - Run `references/kp_essay_synthesis_protocol.md` for every default workbook KP explanation after KP optimisation and before Excel generation.
   - Use slide/page order only to understand lecture logic. Compress raw extracted text into examinable claims and choose a paragraph archetype such as mechanism, process chain, evidence/data operation, comparison, or application.
   - Draft the visible explanation as direct student-facing prose: claim -> mechanism -> named example/evidence where useful -> consequence. Do not write instructions to the student inside the explanation cell.
   - Run a de-slide rewrite pass before writing the workbook. Remove page/slide/source-tracing language such as `Page X first establishes`, `Pages X-Y should be read as`, `KP covers pages`, `slide sequence should be read as`, `remaining linked pages`, `central idea for this block`, and `In an essay answer`.
   - Source coverage is satisfied by page ranges, original slide/page images, coverage audit, and diagnostics. The explanation cell is not responsible for mentioning every page and must never preserve coverage by narrating page-by-page content.
   - If evidence is too weak to support a confident synthesis, write only the conservative supported claim and flag the uncertainty in diagnostics rather than inventing biological content.

8. **Archetype mapping and coverage closure**
   - Extract reusable examiner operations, not just topics.
   - Represent each archetype as task verb + input format + cognitive operation + expected output + mark-scheme structure.
   - Represent each slot grammar with replaceable variables such as molecule set, disease example, graph parameter, channel subtype, circuit element, experimental assay, figure type, or calculation parameter.
   - Build an all-examinable matrix by checking every unit KP against factual, mechanistic, structural, quantitative, and comparative task dimensions.
   - Store archetype grammar separately from Unit content. Unit examples may contribute operation grammar, rotating-slot logic, and answer-shape logic; they must not contribute factual content to another Unit.

9. **Past-paper mapping and statistics**
   - Map each formal question to one primary KP for frequency/retention statistics.
   - Add secondary/supporting KPs only for answer generation. Do not inflate frequency by counting one question fully against multiple topics.
   - Report hotness, retention, recency, lecture centrality, question-shape fit, and lecturer/module slot fit separately. Use a combined PredictionScore only as an explainable ranking aid.
   - Separate topic recurrence from archetype recurrence. Do not pool across Units or regimes, and do not report fake precision for small paper sets.

10. **Pattern detection**
   - Use LecturerModuleSlotDetector. Test, do not assume: one lecturer one question, one module block one question, one lecture one question, one detailed KP one question, cross-lecture synthesis, disease/application slot, experiment/design slot, scenario slot, and figure-required slot.
   - Record supporting years, contradicted years, mapped questions, confidence, and consequence for prediction.
   - Translate Unit examples into detector tests, not assumptions. For future Units, ask whether the same structural condition exists and record the evidence before applying the pattern.

11. **Question-type outputs**
   - MCQ: predict discriminator axes and distractor families, not full stems. Generate contrast tables, formula flashcards, wrong-option diagnoses, exception lists, mechanism-order traps, and lecture-only wording.
   - Short answer: predict archetype + mark-producing answer schema. Generate 2/4/6/8-mark answer skeletons plus `Exam Answer` and `Reference Expansion` layers in English.
   - Essay: predict practice essay questions and knowledge-point explanations. Do not generate example essays unless explicitly requested.
   - Long-answer project/scenario: predict examiner operation slots and method-driven answer plans. Do not generate generic essays; use `long_answer_example_protocol.md` for high-score example long answers when explicitly requested.
   - The far-right student workbook area must adapt to detected question type, not to the source Unit name of any benchmark example.

12. **Example Essay Mode**
   - Trigger this branch only when the user explicitly asks for complete `Example Essay`, `model essay`, `full essay-style answer`, `write an essay`, or equivalent complete essay answers. A request for workbook KP explanations or one essay-style paragraph does not by itself require DOCX output unless the user asks for full Example Essays.
   - Explicit Example Essay Mode is DOCX-first. Produce one standalone `.docx` per complete essay using `references/example_essay_docx_output_protocol.md`. Do not put whole essays into the student workbook.
   - Default workbook behaviour remains unchanged: predicted practice questions only, unless examples are explicitly requested.
   - In Example Essay Mode, each complete essay must be exported as a standalone DOCX. Excel paragraph-row output is allowed only as an optional audit artefact when explicitly requested, not as the primary Example Essay deliverable.
   - No Example Essay may be drafted before the relevant lecture slides have been read, mapped, and converted into a lecture-logic plan.
   - Lecture slides are the primary factual source. Extra Reading and cited papers may enrich the essay, but they must not replace the lecture sequence, introduce unrelated mechanisms, or change the lecturer's intended answer structure.
   - Before drafting, produce the internal sequence in `essay_generation_protocol.md`: Question Analysis, Lecture Slide Scope Detection, Lecture Slide Reading, Lecture Logic Reconstruction, Citation Detection, Citation Original Source Resolution and Reading, Extra Reading Chapter Matching and Reading when supplied, Paragraph Plan, Highlight Plan, Source-to-Run Mapping, DOCX Generation, DOCX Format Linting, Render/Visual QA, Source Audit JSON, and Examiner-Fit Checklist.
   - Build essays from paragraph functions and causal mechanism chains, not from slide-by-slide summaries.
   - Keep Example Essays below the stated limit; if the only limit is 1000 words and no minimum is stated, maximise relevance per word and do not pad.
   - Format each DOCX as A4, 2.5 cm margins, Arial 10 pt, 1.5 line spacing, zero paragraph spacing before/after, justified body, centered title, and left-aligned subtitles/headings.
   - If Extra Reading Books are supplied and a relevant chapter/section is found, integrate 10-15% of essay body words from that material and highlight those runs yellow. If no relevant chapter is found, flag it and do not invent.
   - If relevant lecture slides contain citations, resolve and read the original cited source before using source-derived content. Green-highlight cited-source runs and include author-year in-text citations.
   - Generate `example_essay_manifest.json`, `example_essay_source_audit.json`, one source map JSON per essay, and one QA JSON per essay.

13. **Long Answer Project Mode**
   - Trigger this branch when exam-format parsing identifies a non-essay, answer-one, project/scenario-based long-answer paper, or when the user explicitly requests a model answer for such a question.
   - For project/scenario-based long-answer exams, the answer is not a broad essay. It is a compact experimental argument: what should be done, why that method is suitable, what result would be expected, how the result answers the question, and what caveats or controls are needed.
   - Before writing, produce: question deconstruction, lecture/module knowledge inventory, examiner operation/archetype, paragraph plan, final high-score answer, optional extra-reading refinement, and self-check against the question.
   - Structure answers by question parts, mark weights, scenario facts, method principles, readouts, interpretation, and controls.
   - For method-driven project/scenario papers structurally similar to the BIOL21111 benchmark, treat the current project/scenario format as the answer-style regime. Older short-answer or coverage-only papers may support concept coverage but must not control current long-answer structure.

14. **Extra reading and exemplars**
   - Verify author surname and year before using in-text citations.
   - In Example Essay Mode, a citation printed on a slide is not enough. Resolve and read the original cited source before using source-derived content; otherwise omit the source-derived claim and flag `citation_original_unreadable`.
   - In Example Essay Mode, uploaded Extra Reading Books require chapter/section matching before use. Use only relevant passages, target 10-15% yellow-highlighted body words, and never let extra reading replace lecture logic.
   - Use exemplars only for structure, paragraph grammar, density, comparison strategy, and strong/weak answer patterns. Do not treat exemplar biological claims as factual authority unless verified.
   - Unit exemplars contribute transferable style lessons only. Do not reuse biological claims, citations, student annotations, or extra-reading claims unless independently verified from target Unit evidence or reliable sources.

15. **Excel generation**
   - Default student-facing output is a single-sheet visual workbook named `Exam_Prep_Map`.
   - The sheet must follow the screenshot-style layout: left locator columns for module/lecture and knowledge point, middle block with original lecture slide/page images for the current knowledge point, right block with essay-style explanation, and far-right block with predicted practice questions or question-type-specific prep outputs.
   - Use a minimal student-facing column set unless the user explicitly asks otherwise: `Pages`, `Lecture / Module`, `Knowledge Point`, `Original PPT Page` or `Original Page Image`, `Essay-Style Synthesis`, and `Exam-Facing Prep`. If backward compatibility keeps `Essay-Style Sequential Explanation`, define sequential as causal or argument sequence, not slide/page sequence.
   - Do not include `Lecturer`, `Slide Title`, `Extracted Slide Text`, OCR dumps, evidence/provenance columns, weak-OCR status messages, page-function labels such as `content`, KP-chain IDs, chain-order columns, or sequence-locator prose in the student-facing sheet.
   - Do not add summary, QA, excluded-slide, KP-index, or coverage-audit sheets to the student-facing workbook unless the user explicitly asks for an audit workbook. Keep diagnostics in an external JSON or a separate evidence workbook.
   - Stack knowledge-point blocks vertically so the left locator acts as a directory.
   - Merge adjacent slides/pages that teach the same mechanism, process, comparison, diagram sequence, experiment, or scenario into one knowledge-point block. Do not make one row per slide with repeated short explanations when several slides form one examinable unit.
   - A merged knowledge-point block may span several original pages. Retain every included original slide/page image in source order inside that block so no source content disappears.
   - Write the explanation for each merged block as one smooth essay-style synthesis paragraph that explains the whole knowledge point. Do not write page-by-page narration such as `Page 8 shows... Page 9 then...`; the page range belongs in the `Pages` column and the explanation should read like a coherent answer paragraph.
   - When the user asks for Essay-Ready wording, write the explanation as text that could be placed directly into an exam answer. Avoid meta-instructions such as `a strong answer should`, `the essay point is`, `this block shows`, or `the lecture material`; state the biological concept, mechanism/evidence, evaluation, and consequence directly.
   - Write the explanation for each merged block in complete essay-style language that synthesises all pages in the block. Do not paste extracted text, list raw slide bullets, or write placeholder sentences such as `no reliable extracted text`; use diagnostics for extraction failures.
   - Exclude non-informative navigation pages from the student workbook, including lecture home/title pages, recommended-reading pages, pure `Content`/agenda/outline pages, section-divider title pages, learning-objective pages, resources-only pages, admin/project-logistics pages, blank pages, and end/interactive prompt pages. If a slide contains an examinable mechanism, equation, data figure, case study, comparison, or experimental result, retain it even if the text extraction is sparse.
   - Preserve the original aspect ratio of slide/page images. Do not distort images to fit arbitrary cell blocks. After image placement is stable, adjust text font size and row height for readability.
   - Make the workbook readable by default: use wrapped Arial text, approximately 10-12 pt fonts, wider explanation/prep columns, stable image-column width, frozen headers/locator columns, and row heights large enough for the slide image and paragraph text.
   - Analyse and output lecture content from the first slide/page to the last slide/page in source order. Do not skip intermediate slides because they look low priority.
   - Segment by examinable mechanism/process/evidence/data-operation units, while preserving lecture order.
   - Unit examples contribute layout adaptation rules only: slide-image alignment, mixed-format prediction areas, Section A/B distinction, old/current-regime labels, long-answer project columns, and paragraph-row splitting when explicitly requested.

16. **QA**
   - Produce a QA_Flags sheet and diagnostics JSON listing weak OCR, unreadable files, unsupported files, ambiguous question type, missing slide evidence, answer not found in lectures, unverified citation, low-confidence prediction, and old papers excluded from prediction.
   - Predictions must be labelled as predicted practice questions, never official exam questions.
   - Before delivery, lint the generated workbook explanation/prep language with `scripts/essay_style_linter.py` or an equivalent check. Fail or rewrite if more than 5% of explanations contain banned page/slide/meta-writing patterns, if any explanation repeats page-by-page narration, or if more than 10% of explanations contain how-to-write language rather than content.
   - Add QA flags when a Unit example is used as content prediction, when a Unit-specific instruction appears outside regression context, when a transfer rule is missing, when non-transferable content is unmarked, or when an example claim is used without verification.

17. **Cross-subject regression**
   - When benchmark examples are supplied, run each named Unit as a separate benchmark key and also validate the generic contribution it provides.
   - Do not pool content evidence across these units.
   - Verify unit-specific pass/fail plus generic contribution pass/fail: unit separation, exam-regime split, question-type routing, KP granularity, lecture-order coverage, KP essay-synthesis quality, Excel adaptation, transferable rule presence, non-transferable content marking, and cross-unit leakage prevention using `cross_subject_regression_protocol.md`.

## Output Contract

Default requested deliverable is:

1. a student-facing single-sheet Excel workbook with no evidence columns;
2. diagnostics JSON;
3. optionally, a separate evidence workbook when useful for audit or debugging.

Explicit Example Essay Mode deliverable is:

1. `Example_Essays_DOCX/` containing one standalone `.docx` per essay;
2. `example_essay_manifest.json`;
3. `example_essay_source_audit.json`;
4. per-essay source maps and QA JSON files;
5. optionally `Example_Essays_DOCX.zip`.

Do not edit, rename, delete, or overwrite source files.

When a user asks to keep only the latest output, remove older generated workbook versions, previews, temporary slide-image folders, and stale diagnostics from the requested report folder after verifying the latest workbook. Do not delete source files.
