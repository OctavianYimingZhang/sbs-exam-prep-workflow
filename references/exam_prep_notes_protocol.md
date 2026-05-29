# Exam Prep Notes Protocol

`exam_prep_notes_docx` is the default route when the user supplies course materials and asks for revision, notes, general exam preparation, or to go through the material without naming a narrower artifact. It produces Academic Exam-Ready Notes in the compatible public Word artifact `Lecture_Knowledge_Walkthrough.docx`.

This route is not a slide paraphrase, a chatty tutor explanation, a prediction file, an Excel map, or a complete Example Essay package.

## Core Principle

Accept any readable, ordered course-note source, but do not give every source the same authority.

```text
CourseContentSource -> OrderedContentItem -> SourceFragment -> AtomicKnowledgeLedger -> SourceBaselineNotesPlan -> KnowledgeOnlyStudentView -> PublicOutputPoint -> ExamOverlayPass -> PrepArtifact
```

The route reconstructs the course knowledge architecture and writes a protected source-first baseline before any exam overlay is allowed to affect density, order, priority, or add-ons. Source order is used to infer prerequisites, teaching intent, and causal development, not to force the final notes to preserve the original note sequence when a better exam logic exists.

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
3. Reconstruct course-level sections from the official source logic.
4. Map lecture sessions or ordered source blocks into the reconstructed course sections.
5. Extract lecture-level conceptual modules and KnowledgePoints.
6. Build the internal `AtomicKnowledgeLedger`.
7. Generate `SourceBaselineNotesPlan` from official source structure before exam pruning.
8. Run `BaselineCoverageFloorQA`.
9. If formal past papers are supplied, insert optional `exam_regime`, `past_paper_questions`, `question_archetypes`, and `examiner_operations` actions; use them for format, emphasis, and answer-operation evidence only.
10. Build `ExamEmphasisProfile` from formal past-paper question records when available.
11. Apply `ExamOverlayPass` to priority, density, ordering, examples, traps, and question-type add-ons.
12. Run `OverlayDidNotDamageCoverageQA`.
13. Build the `KnowledgeOnlyStudentView` filter.
14. Select the `OutputLanguageProfile` from the user request; keep default English labels unless the user explicitly requests another language.
15. Select the route-specific `RouteDocxStyleProfile`.
16. Build `PublicOutputPoint` and `PublicPointBlock` objects from the internal cards.
17. Bind protected atomic items to public points with `PointCoverageBinding`.
18. Generate integrated Academic Exam-Ready Notes from public points only.
19. Append a question-type add-on layer only when useful or requested.
20. Add optional visual aids only after the text is source-backed.
21. Run public-point, output-language, route-style, exam-prep-notes, student-output, evidence, DOCX, and helper-file boundary QA.

Exam evidence may add, split, reorder, prioritise, densify, and enrich. Exam evidence must not delete, hide, or over-compress protected source-backed modules.

Past-paper objects must not be visible to module segmentation, atomic-item extraction, or baseline coverage construction. Formal exam evidence may be loaded only after `AtomicKnowledgeLedger`, `SourceBaselineNotesPlan`, and `BaselineCoverageFloorQA` are complete. This prevents exam patterns from defining the factual boundary of the notes.

If no formal past papers are supplied, generate notes from source centrality, conceptual dependency, and official course emphasis only. Do not invent exam frequency or future-question probability.

Cross-target examples, exemplar answers, and feedback sources must run the internal example-learning chain before they affect any rule: example review ledger, transferable-rule synthesis, rule-promotion gate, and example-transfer linting. Accepted rules may control paragraph density, answer ordering, and transferable workflow checks only; they must not support target factual claims, prediction claims, official answers, priority labels, or production branching on example identity.

Visual-heavy PDFs, presentations, figures, tables, image exemplars, and image-only files must carry visual-inspection metadata in source inventory and fragment partitions. If a requested output depends on the visual content, inspect it before making the claim or keep the relevant conclusion limited.

## AtomicKnowledgeLedger

Before building baseline notes, create an internal `AtomicKnowledgeLedger`.

Every slide, page, table, figure, diagram, or source block must be decomposed into atomic units:

```yaml
AtomicKnowledgeUnit:
  unit_id: string
  source_id: string
  lecture_id: string
  slide_or_page_range: string
  raw_heading: string
  raw_text_summary: string
  unit_type:
    - definition
    - term
    - contrast_pair
    - criteria_item
    - mechanism_step
    - method_step
    - equation
    - calculation_rule
    - graph_readout
    - diagram_label
    - table_entry
    - named_example
    - disease_case
    - drug_case
    - limitation
    - misconception
    - administrative
    - decorative
    - duplicate
    - unreadable_visual
  student_visibility:
    - include_in_notes
    - internal_audit_only
    - exclude_admin
    - duplicate_covered_elsewhere
    - requires_visual_inspection
  bound_module_id: string | null
  coverage_status:
    - covered
    - grouped_but_named
    - audit_only
    - excluded_with_reason
    - missing
```

Rules:

- Every slide/page heading becomes at least one atomic item unless it is purely administrative.
- Every bullet containing a term, process, definition, method, equation, graph, example, limitation, or contrast becomes an atomic item.
- Every table row or diagram label that teaches knowledge becomes an atomic item.
- Administrative units are excluded from student output.
- Knowledge units must be bound to final modules or named submodules.
- Grouping is allowed only when each grouped item is still named and explained inside the module.

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
- mark content as `★★★`, `★★`, or `★` without exposing scoring logic.

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

## Protected KnowledgePoint Rule

A source-backed item is protected when it is:

- an intended learning outcome;
- a slide/page heading or major notes heading;
- an official definition;
- a contrast pair;
- a criteria, features, stages, classes, or components list;
- a named example used to teach a concept;
- a source section of the form `Why X?`;
- a labelled diagram, table, graph, equation, calculation, or workflow;
- a summary or take-home point;
- a term, operation, or concept appearing in formal past papers.

Protected items must appear in the source baseline plan. They may not disappear, be hidden only in `Common Error / Trap`, or be reduced to one checklist phrase. If a protected item is genuinely low value, keep it brief and label it `★`; do not remove it unless a QA flag records why it cannot be supported.

## Knowledge-Only Student View

For ordinary `exam_prep_notes_docx`, student-facing output must contain only knowledge-related revision content.

Do not include:

- assessment percentages;
- exam timing;
- mark splits;
- Section A / Section B administrative rules;
- historical-paper comparability notes;
- `no mark scheme supplied` notes;
- `Coverage note` warnings;
- source-quality caveats;
- ELM-check warnings;
- audit, provenance, extraction-quality, source-coverage, or lineage explanations.

Keep these in an internal audit file or chat-only diagnostic only when explicitly requested. The public DOCX is a knowledge document, not an exam-format audit.

Replace `Course-Level Exam Map` with `Course Knowledge Map`.

Allowed public top matter:

- course/module title;
- knowledge section map;
- lecture/topic mapping;
- one short sentence on how the knowledge is organised.

Generic exam advice stays internal. A concrete graph-reading rule, calculation operation, case-study decision rule, or answer-shaping rule may appear only when it adds knowledge; otherwise it belongs in a question-type add-on. Do not expose exam timing, marks, paper comparability, source limitations, or audit caveats.

## Background Demotion Rule

Background/context modules include industry overview, stakeholder landscape, broad pipeline narration, commercial context, historical framing, and assessment administration.

Default rating: `★`.

Raise to `★★` only when the background is needed to justify target choice, candidate progression, regulatory logic, or case-study decisions.

Raise to `★★★` only when the current source set shows that the exam explicitly asks students to define, compare, calculate, or justify using that background as the central answer operation.

Background modules must normally be capped at 4-6 lines and must not appear before higher-yield definitional, mechanistic, methodological, or criteria-list modules when this would obscure exam-core material.

## Granularity Rule

Use one card per examinable concept.

Do not merge the following into one dense paragraph:

- definition + criteria + example;
- mechanism + limitation + named drug;
- method principle + readout + limitation;
- graph parameter + calculation + interpretation;
- contrast pair + application.

If a source section contains a list, preserve it as a numbered or bulleted list when the list itself is examinable.

If a source gives a named example, include it as an `Example` block unless the example is clearly decorative.

## Module Density Floor

The Skill must not compress a lecture or PPT section below the density required by protected source features. Supplied examples may raise this floor only after the example-learning promotion gate converts the observation into a generic validation rule.

For each lecture or PPT file:

- every major source heading must become either a module or a named submodule;
- every protected list must be preserved as a list;
- every named method must receive a module or submodule;
- every named example must appear as an Example block or named example submodule;
- every diagram, table, equation, or workflow that teaches knowledge must be explained;
- no module may combine more than one definition set, mechanism, criteria list, method workflow, named example, graph, or calculation logic unless each receives its own visible subheading.

Heuristic minimum:

- If a lecture contains 1-10 protected atomic units: at least 2 modules.
- If a lecture contains 11-25 protected atomic units: at least 4 modules.
- If a lecture contains 26+ protected atomic units: at least 6 modules or clearly separated submodules.
- A course section spanning more than 2 lectures must not be represented by fewer than 4 modules unless the source itself is extremely short.

Fail QA when broad cards replace lecture-level coverage.

## Student-Facing Structure

Use a Word-first structure that reads as revision notes, not an audit:

```text
Title
Course Knowledge Map
Lecture [Number or Name]
[★★★ | ★★ | ★] [Public Point Title]
[Main explanation]
[Definitions / Criteria / Steps / Mechanism / Equation / Calculation Logic / Graph Logic / Comparison / Example / Limitation blocks as needed]
Question-Type Add-On Layer
Optional Visual Aid
```

Internal card fields guide planning and QA. They are not public headings. Ordinary Academic Exam-Ready Notes must not render headings named `Exam Specificity`, `Core Exam Claim`, `Exam Use`, `Common Error / Trap`, or `Must Master`.

Render only knowledge-bearing blocks. If a planned `Exam Use` contains only generic advice such as how to use a module in an answer, suppress it. If a planned trap contains a real distinction, integrate it into a Comparison or Limitation block.

The internal `ExamPrepNotesPlan` must use structured course sections, lecture mapping, source-backed internal knowledge cards, public output points, official definition records, source-baseline binding, exam-emphasis binding, exam-overlay binding, output-language profile, route DOCX style profile, render decisions, point coverage bindings, question-type add-ons, content-coverage checks, QA flags, and a visible-output field filter. Every public output point must have source support, one visible star priority label, a point kind, protected atomic coverage, and a coverage binding.

Priority meanings:

- `★★★` = answer-producing exam core: standalone definition, mechanism, calculation, graph/data operation, criteria list, method workflow, named source example, or case-study decision point.
- `★★` = supporting examinable knowledge: useful for explanation, comparison, justification, or transfer.
- `★` = background/context: useful framing only; keep brief unless directly tested.

## Route DOCX Style

`exam_prep_notes_docx` uses compact revision-note formatting, not essay-submission formatting:

```yaml
RouteDocxStyleProfile:
  route: exam_prep_notes_docx
  margin_cm: 2.0
  line_spacing: 1.05-1.15
  body_alignment: left
  body_font_pt: 10.5
  heading_font_pt: 12
  lecture_heading_font_pt: 14
  lecture_page_breaks: true
```

Every lecture starts on a new page. Body text is left-aligned. The 2.5 cm margin, 1.5 line spacing, and justified-body format belongs to `example_essay_docx`, not ordinary Academic Exam-Ready Notes.

For ordinary Academic Exam-Ready Notes, the public DOCX is a knowledge document, not an exam-format audit. The Skill must first decompose all official source material into an `AtomicKnowledgeLedger`, exclude administrative items from student output, preserve every source-backed knowledge item in a baseline module or named submodule, and only then apply exam evidence as priority, density, ordering, and add-on guidance. Past papers may change emphasis; they must not define the factual boundary of the notes.

## Academic Exam-Ready Notes Prose Policy

Use these as internal planning functions, not required public headings:

- `Core Exam Claim`;
- `Key Definitions`;
- `Exam-Ready Knowledge Synthesis`;
- `Criteria / Components / Steps`;
- `Mechanism / Process Logic`;
- `Canonical Example`;
- `Exam Use`;
- `Common Error / Trap`;
- `Must Master`.

Skill package files, fixtures, and protocol text are authored in English. This is a package-authoring convention, not a restriction on user-requested outputs. Public labels should stay as default English labels unless the user explicitly requests another language or mixed-language output. Do not infer multilingual output from source-language mixture alone.

Avoid:

- `In this section we will learn...`;
- `This slide explains...`;
- `The notes are trying to say...`;
- `You should understand...`;
- page-by-page or slide-by-slide narration.

The writing should start with the examinable claim or problem, then explain mechanism, evidence, scope, limitation, and concrete application where it adds knowledge.

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
- `past_paper_loaded_before_baseline_qa`;
- `administrative_exam_audit_in_student_notes`;
- `atomic_knowledge_unit_missing`;
- `broad_card_below_density_floor`;
- `protected_item_only_in_trap_or_must_master`;
- `non_black_docx_text`;
- `blue_docx_heading`;
- `student_note_used_as_fact_without_verification`;
- `ai_note_used_as_fact`;
- `definition_specificity_without_support`;
- `question_type_addon_before_base_notes`;
- `generated_visual_aid_treated_as_evidence`;
- `internal_helper_artifact_in_student_output`.
