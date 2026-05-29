# Knowledge Walkthrough DOCX Protocol

`knowledge_walkthrough_docx` is the compatibility lecture-first route when the user explicitly asks to go through lecture knowledge in source order. It is Word-first and lecture-first. It is not an Excel workbook converted into a DOCX file.

For general revision, exam-prep notes, or "go through the material" requests, prefer `exam_prep_notes_docx` in `exam_prep_notes_protocol.md`. That route uses exam-informed Academic Exam-Ready Notes logic while preserving the public artifact name `Lecture_Knowledge_Walkthrough.docx`.

## Purpose

The student opens this Word file to do one task:

```text
Go through the main knowledge in lecture order, understand each conceptual module, and know the common exam-facing use of the knowledge.
```

The route is not:

- essay exam preparation by default;
- past-paper prediction;
- MCQ or short-answer high-yield report;
- Excel-style `Exam_Prep_Map`;
- a slide/page paraphrase.

The route is:

```text
Lecture -> conceptual module -> explanation -> key logic -> common confusion -> must master
```

## Student-Facing Structure

Use this document structure:

```text
Title Page
How To Use This Document
Lecture 1: [Lecture Title]
Lecture Overview
Module Map
Module 1.1
Module 1.2
Module 1.3
Lecture Recap
Lecture 2: [Lecture Title]
...
```

Do not use table-like Excel columns such as:

```text
Lecture | Topic | Source | Evidence | Exam Type | Prediction | Action
```

The document should read continuously.

## Lecture Section

Each lecture section must include:

```text
Lecture X: [Lecture Name]
What This Lecture Is About
[3-5 sentences in the assistant's own words.]
Module Map
1. [Module 1]: [one-sentence function]
2. [Module 2]: [one-sentence function]
Core Logic
[one mechanism chain or concept chain.]
```

## Module Card

Each module must use this structure:

```text
Module X.X: [Module Title]
What This Module Explains
[2-4 sentences.]
Knowledge Walkthrough
[Natural explanatory prose. Bold required terms. Do not dump bullets. Do not retell slide order.]
Key Logic
[Arrow chain or compact mechanism chain.]
Key Distinctions
[Only source-backed distinctions or misconception boundaries. Omit the section when none are useful.]
Knowledge Points
[3-5 short factual recall/action points.]
```

## Generation Steps

Step 1: Lecture-level reading. Read the full lecture before output. Identify the actual biological, biochemical, clinical, methodological, or conceptual problem the lecture is solving.

Step 2: Module extraction. Split by conceptual function, not by slide number:

- definition module;
- mechanism module;
- regulation module;
- integration module;
- comparison module;
- disease/application module;
- method/data module.

Step 3: Knowledge compression. Merge repeated content and convert pathways into mechanism chains only after checking protected KnowledgePoints. Official definitions, contrast pairs, criteria/features/stages lists, named examples, `Why X?` blocks, diagrams, tables, equations, calculations, workflows, and past-paper terms must remain visible as named module content. Demote or omit only genuinely unsupported or repetitive detail, not protected source-backed items.

Step 4: Student-facing rewrite. Use direct explanatory prose and bold required terms. Keep default English labels unless the user explicitly requests another language or mixed-language output. Do not write `slides say`, `according to page`, or source-tracing narration.

Step 5: Lecture recap. End each lecture with a compact recap, normally 6-10 lines.

Step 6: Select `RouteDocxStyleProfile` before DOCX writing. If the user supplies a formatting screenshot, old generated DOCX, or visual layout example, analyse it only as transferable layout evidence: density, spacing, alignment, heading hierarchy, page-break policy, and label discipline. Do not copy source-specific wording, course titles, or factual content from the example.

Step 7: Run the Knowledge Walkthrough DOCX style linter before publish. A walkthrough that falls back to essay-style margins, essay-style 1.5 spacing, justified body text, inconsistent fonts, or excessive whitespace must be regenerated.

Step 8: Run the knowledge-only rendering gate. The walkthrough must contain only source-backed knowledge points and knowledge-bearing labels. Remove `How To Use This Document`, `How To Answer`, `Integrated reasoning`, `Integrated practical reasoning`, `Answer Logic`, `Exam Strategy`, `Recommended Approach`, `A strong answer should`, `Use this module`, and commentary about whether a topic is reliable by question type. Rewrite any real content inside those sections as factual `Knowledge Points`, `Key Logic`, `Key Distinctions`, method workflow, graph/data rule, calculation rule, comparison, or limitation.

## Forbidden Student Fields

The DOCX must not show:

- source anchor;
- confidence;
- evidence score;
- recurrence count;
- examiner operation;
- discriminator axis;
- essay theme;
- essay plan;
- full example essay;
- long-answer paragraph bank;
- practice question;
- answer key;
- past-paper year mapping;
- prediction score.

## DOCX Formatting

Use the compact lecture-note formatting contract:

- Arial;
- 2.0 cm margins;
- compact 1.05-1.15 line spacing;
- body text left-aligned;
- subheadings left-aligned;
- main title centered;
- black text;
- stable heading hierarchy;
- lecture page breaks;
- no essay-style 2.5 cm margins, 1.5 spacing, or justified body text unless the user explicitly asks for essay-style formatting.

Required style profile:

```yaml
RouteDocxStyleProfile:
  route: knowledge_walkthrough_docx
  margin_cm: 2.0
  line_spacing: 1.05-1.15
  body_alignment: left
  body_font_pt: 10.5
  heading_font_pt: 12
  lecture_heading_font_pt: 14
  text_color: black
  lecture_page_breaks: true
  essay_style_spacing_forbidden: true
```

## Output Boundary

The public output folder should contain the DOCX only unless the user asks for an audit package. Internal QA files, source maps, and generation manifests must go to an internal QA folder.
