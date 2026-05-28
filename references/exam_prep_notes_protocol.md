# Exam Prep Notes Protocol

`exam_prep_notes_docx` is the default route when the user supplies course materials and asks for revision, notes, general exam preparation, or to go through the material without naming a narrower artifact. It produces Academic Exam-Ready Notes in the compatible public Word artifact `Lecture_Knowledge_Walkthrough.docx`.

This route is not a slide paraphrase, a chatty tutor explanation, a prediction file, an Excel map, or a complete Example Essay package.

## Core Principle

Accept any readable, ordered course-note source, but do not give every source the same authority.

```text
CourseContentSource -> OrderedContentItem -> SourceFragment -> KnowledgePoint -> PrepArtifact
```

The route reconstructs the course knowledge architecture before writing. Source order is used to infer prerequisites, teaching intent, and causal development, not to force the final notes to preserve the original note sequence when a better exam logic exists.

## Source Authority

Factual authority:

- official lecture slides;
- official notes or handouts;
- lecturer-provided PDF/DOCX notes;
- official practical material or assessment guidance;
- independently verified textbooks, chapters, papers, DOI/PubMed records, publisher pages, or equivalent academic sources.

Auxiliary sources:

- student typed notes;
- handwritten notes;
- annotated screenshots;
- flashcards;
- Notion-style or structured revision notes;
- unknown-provenance summaries.

Auxiliary sources may indicate what the student thinks matters, what needs clarification, or where an official source should be checked. They must not directly support factual course claims unless verified against factual-authority sources.

AI-generated notes have no factual authority. They may help with structure only after every factual claim is independently verified.

If only auxiliary notes are supplied, the route may still organise and clean the material, but it must mark factual conclusions as requiring verification and avoid adding unsupported specificity. Ask for official or verified sources only when the requested conclusion depends on factual authority.

## Internal Pipeline

Run the route in this order:

1. Classify source authority and extraction quality.
2. Build a source coverage map and identify unreadable or weak sources.
3. If formal past papers are supplied, insert optional `exam_regime`, `past_paper_questions`, `question_archetypes`, and `examiner_operations` actions; use them for format, emphasis, and answer-operation evidence only.
4. Reconstruct course-level sections from the official source logic.
5. Map lecture sessions or ordered source blocks into the reconstructed course sections.
6. Extract lecture-level conceptual modules and KnowledgePoints.
7. Apply exam-emphasis mapping to density, ordering, and priority labels.
8. Generate Academic Exam-Ready Notes.
9. Append a question-type add-on layer only when useful or requested.
10. Add optional visual aids only after the text is source-backed.
11. Run student-output, evidence, language, DOCX, and helper-file boundary QA.

If no formal past papers are supplied, generate notes from source centrality, conceptual dependency, and official course emphasis only. Do not invent exam frequency or future-question probability.

Cross-target examples, exemplar answers, and feedback sources may add an internal style-analysis action. That action may control paragraph density, answer ordering, and transferable workflow rules only; it must not support target factual claims, prediction claims, official answers, or priority labels.

Visual-heavy PDFs, presentations, figures, tables, image exemplars, and image-only files must carry visual-inspection metadata in source inventory and fragment partitions. If a requested output depends on the visual content, inspect it before making the claim or keep the relevant conclusion limited.

## ExamEmphasisProfile

Formal past papers may control preparation emphasis, not factual truth. The internal profile may include:

```yaml
ExamEmphasisProfile:
  target_group_key:
  current_regime:
  visible_question_types: []
  repeated_question_families: []
  compatible_knowledge_points: []
  answer_operations: []
  emphasis_level: high | medium | low | unknown
  limitation_flags: []
```

Allowed uses:

- increase depth for source-backed KnowledgePoints that match visible question families;
- order notes so high-transfer concepts appear before lower-transfer details;
- decide whether MCQ, short-answer, long-answer, practical/data, or essay add-ons are useful;
- mark content as `必备`, `重点`, or `补充` without exposing scoring logic.

Forbidden uses:

- exact future wording;
- unsupported official answers;
- fake numerical probability;
- content outside source-backed scope;
- public confidence bands, recurrence counts, or past-paper year mappings.

## Definition Policy

If an official course source gives a definition, preserve its meaning and wording as closely as possible while improving grammar and concision.

If a definition appears only in student notes or unknown-provenance notes, treat it as a cue. Write a clean academic definition only after checking official course sources or verified academic sources.

If no support is found, use a conservative definition, avoid extra specificity, and attach an internal QA flag. Do not invent mechanism, scope, exception, or terminology.

## Student-Facing Structure

Use a Word-first structure that reads as revision notes, not an audit:

```text
Title Page
Course-Level Exam Map
Course Section: [Title]
Section Exam Function
Lecture Mapping
Core Conceptual Threads
Lecture [Number or Name]
Lecture Function Within Section
Lecture-Level Module Map
Module: [Title]
Priority: 必备 | 重点 | 补充
Core Exam Claim
Exam-Ready Knowledge Synthesis
Mechanism / Process Logic
Evidence / Example Function
Common Error / Trap
Must Master
Question-Type Add-On Layer
Optional Visual Aid
```

Omit headings that add no value for a specific source set. Do not expose internal evidence fields.

The internal `ExamPrepNotesPlan` must use structured course sections, lecture mapping, source-backed knowledge cards, official definition records, exam-emphasis binding, question-type add-ons, content-coverage checks, QA flags, and a visible-output field filter. Every student-visible knowledge card must have source support, one visible priority label, an exam function, and a coverage status.

## Academic Exam-Ready Notes Language

Prefer:

- `Core Exam Claim`;
- `Exam-Ready Knowledge Synthesis`;
- `Mechanism / Process Logic`;
- `Evidence / Example Function`;
- `Common Error / Trap`;
- `Must Master`.

Avoid:

- `In this section we will learn...`;
- `This slide explains...`;
- `The notes are trying to say...`;
- `You should understand...`;
- page-by-page or slide-by-slide narration.

The writing should start with the examinable claim or problem, then explain mechanism, evidence, scope, limitation, and exam use.

## Question-Type Add-On Layer

Question-type add-ons come after the base notes. They do not replace the base notes.

MCQ add-on:

```yaml
MCQAddOn:
  testable_statement:
  possible_wrong_or_distractor_statement:
  common_trap:
  must_remember_rule:
```

Do not claim official correct answers unless an answer key exists.

Short-answer add-on:

```yaml
ShortAnswerAddOn:
  bounded_example_question:
  concise_example_answer:
  required_terms_in_answer_text:
  avoid_this_mistake:
```

Bold required terms inside the answer. Do not expose `common omissions` as a visible field.

Essay add-on:

```yaml
EssayAddOn:
  essay_ready_paragraph_blocks:
    mechanism:
    process:
    comparison:
    evidence:
    limitation:
```

Generate complete Example Essays only when the user explicitly requests essay preparation, model essays, full essay-style answers, or complete essay documents.

## Visual-Aid Hook

Visual aids are optional and final-layer only:

```text
VisualAidPlanning -> ImageGenerationIfAvailable -> VisualAidQA -> EmbedOrAttach
```

Generated visual aids may illustrate already source-backed mechanisms, workflows, spatial relations, comparisons, or method logic. They must not introduce facts, reproduce private or copyrighted source figures, replace source reading, or imply an official course figure.

Follow `visual_aid_generation_protocol.md` for visual-aid specs, captions, and QA flags.

## QA Flags

Block or rewrite when any of these appear:

- `original_note_order_leakage`;
- `exam_emphasis_without_formal_evidence`;
- `student_note_used_as_fact_without_verification`;
- `ai_note_used_as_fact`;
- `definition_specificity_without_support`;
- `question_type_addon_before_base_notes`;
- `generated_visual_aid_treated_as_evidence`;
- `internal_helper_artifact_in_student_output`.
