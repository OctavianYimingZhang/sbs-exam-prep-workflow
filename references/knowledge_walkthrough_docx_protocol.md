# Knowledge Walkthrough DOCX Protocol

`knowledge_walkthrough_docx` is the default lecture-review route when the user supplies lecture materials and asks to go through the course knowledge. It is Word-first and lecture-first. It is not an Excel workbook converted into a DOCX file.

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
Common Confusions
[Only real confusion points. Omit the section when none are useful.]
Must Master
[3-5 short statements.]
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

Step 3: Knowledge compression. Merge repeated content. Convert pathways into mechanism chains. Demote low-value details into common confusions or omit them.

Step 4: Student-facing rewrite. Use direct explanatory prose, mixed English terms where useful, and bold required terms. Do not write `slides say`, `according to page`, or source-tracing narration.

Step 5: Lecture recap. End each lecture with a compact recap, normally 6-10 lines.

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

Use the Word formatting contract:

- Arial;
- 2.5 cm margins;
- body text justified;
- subheadings left-aligned;
- main title centered;
- 1.5 line spacing;
- all other settings default unless the user specifies otherwise.

## Output Boundary

The public output folder should contain the DOCX only unless the user asks for an audit package. Internal QA files, source maps, and generation manifests must go to an internal QA folder.
