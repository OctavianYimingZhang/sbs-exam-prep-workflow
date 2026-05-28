# Essay Tutor Workflow Protocol

Use this protocol for `essay_exam_prep`, complete Example Essays, model essays, assessed-style essay drafts, essay plans, citation-controlled essay work, and essay figure/table/data support.

This protocol extends the existing lecture-first Example Essay route. It does not replace `essay_generation_protocol.md`, `example_essay_docx_output_protocol.md`, or `language_quality_contract.md`.

## Core Rule

Complete essay work follows this chain:

```text
EssaySkillConfig
-> EssayInputReadinessReport
-> DeepResearch
-> DetailedEssayPlan
-> PlanApprovalGate
-> SubagentOrRoleResearch
-> Draft
-> CitationFigureTableDataQA
-> DOCXOrFinalOutput
```

Do not draft a complete final essay before the plan is approved unless the user explicitly asks to skip the approval loop or requests direct generation.

For exam-prep package generation, a user request such as "generate the essay pack" or "make the Word document now" counts as approval to execute the planned route after the source-readiness gate passes.

## Essay Intake

Collect the smallest blocking set first. Continue with labelled assumptions when the missing information does not block planning.

Required when available:

| Field | Capture |
| --- | --- |
| Essay topic or exact question | Exact wording, whether the title can change, and whether it is an assessed prompt. |
| Word limit | Upper limit, lower limit, tolerance, and whether references, title, captions, figures, tables, and abstract count. |
| Academic level | Undergraduate, master's, doctoral, professional, or exam-prep level. |
| Course/module context | Module, faculty, lecture block, learning outcomes, and target source set. |
| Required format | Chat plan, Markdown, DOCX, PDF, headings, abstract, figures, tables, or separate essay files. |
| Citation style | APA, Harvard, Vancouver, AMA, IEEE, Chicago, MLA, journal style, or university style. |
| Source base | Lecture slides, official notes, reading list, required papers, uploaded papers, textbooks, practical materials, datasets. |
| Rubric | Marking criteria, feedback, grade descriptors, K/C/U/A/R expectations, or learning outcomes. |
| Stage | Planning only, first draft, revision, final polish, or DOCX generation. |
| AI-use policy | Whether AI-assisted writing is allowed and whether a disclosure is needed. |

Strongly recommended:

- target grade or standard;
- required number and type of sources;
- recency requirement;
- user's intended thesis or preferred argument;
- forbidden sources, theories, or content;
- figure, table, or data-analysis requirements;
- previous feedback;
- preferred example essays for style only.

Ask at most one blocking clarification question at a time. If a field is not blocking, record it under:

```yaml
EssayAssumption:
  field:
  assumed_value:
  risk_if_wrong:
EssayOpenRequirement:
  field:
  why_it_matters:
  when_to_resolve:
```

## DeepResearch Before Planning

Before a full plan, run enough research to avoid a generic outline:

```text
Topic deconstruction
-> key concepts
-> source-scope boundary
-> competing models or mechanisms
-> required lecture/source logic
-> seminal sources
-> recent evidence when relevant
-> methodological limits
-> clinical/theoretical/translation implications
-> critical debates
-> figure/table/data opportunities
-> citation map
```

For course-linked essays, official lecture/source logic remains the skeleton. External search sharpens mechanism, evidence, limitations, or citations only after source scope is clear.

Plan-stage citation rule:

- Use exact author-year, DOI, PMID, title, journal, or "recent review" claims only after verification.
- If a source has not been verified, label it `candidate_source`.
- Candidate sources may guide planning but must not enter the draft, reference list, green highlight, or DOCX until metadata and claim relevance are verified.

## Detailed Essay Plan

Every complete essay plan must go below heading level. The main body must include subtitles or paragraph blocks, not only `Introduction`, `Main Body`, `Discussion`, and `Conclusion`.

Use this shape:

```yaml
DetailedEssayPlan:
  essay_question:
  interpreted_scope:
  excluded_scope:
  working_thesis:
  word_limit_strategy:
  proposed_title:
  source_scope:
    official_sources:
    required_readings:
    external_sources_allowed:
    candidate_sources:
  section_plan:
    introduction:
      function:
      content_sequence:
      key_terms_to_define:
      thesis_move:
    main_body:
      - heading:
        section_function:
        subheadings:
          - subtitle:
            specific_content:
            key_claim:
            evidence_needed:
            analytic_angle:
            candidate_or_verified_citations:
        transition_to_next_section:
    discussion:
      synthesis_paragraph:
      limitations_paragraph:
      future_direction_paragraph:
    conclusion:
      final_answer:
      no_new_evidence_rule:
  citation_strategy:
    intensive_reading_citations:
    broad_support_citations:
    classic_sources:
    recent_sources:
  figure_table_data_strategy:
    figures:
    tables:
    data_analysis:
  critical_thinking_strategy:
    main_body_analytic_targets:
    discussion_analytic_targets:
  assumptions:
  open_questions:
```

## Approval Loop

Use this loop unless the user explicitly asks to skip it:

```text
Plan v0.1
-> user edits
-> Plan v0.2 with concise change log
-> repeat until approval
-> draft from approved plan
```

Rules:

- Revise only requested parts unless the change creates a dependency.
- Preserve approved thesis, section hierarchy, paragraph logic, citation strategy, critical-thinking targets, and visual/data strategy.
- Treat "Approve Plan", "approved", "go ahead", or explicit file-generation instruction as approval.
- If new research contradicts the approved plan, stop and request plan revision instead of silently changing the argument.

## Research Roles

Use real subagents when available and appropriate. Otherwise execute these roles sequentially:

```yaml
QuestionAndRubricAgent:
  command_verb:
  required_scope:
  excluded_scope:
  required_argument:
  examiner_expectation:
  off_topic_risk:

LiteratureRetrievalAgent:
  must_read:
  should_read:
  optional:
  excluded:
  identifier:
  claim_supported:
  verification_status:

MechanismTheoryAgent:
  model:
  mechanism:
  source:
  evidence_strength:
  limitation:
  essay_section:

EvidenceAppraisalAgent:
  claim:
  supporting_sources:
  evidence_type:
  strength:
  limitation:
  allowed_verbs:

CitationAgent:
  citation_key:
  source:
  DOI_or_PMID_or_URL:
  used_for_claim:
  citation_mode:
  in_text_location:
  bibliography_entry:
  verification_status:

FigureTableDataAgent:
  figure_needed:
  figure_type:
  source_backed_claims:
  reuse_permission_status:
  table_needed:
  data_analysis_needed:
  legend_or_caption:
```

Accept role output only after checking that sources exist, identifiers are verified where possible, claims match source scope, and uncertainty is labelled.

## Drafting Standard

Write from the approved plan.

Default paragraph:

```text
Claim -> mechanism/evidence -> interpretation -> scope or limitation -> link back
```

Evidence-heavy paragraph:

```text
Evidence -> mechanism tested -> result -> interpretation -> limitation
```

Comparison paragraph:

```text
Shared problem -> comparison axis -> model A -> model B -> evidence -> evaluation
```

Minimum analytic target:

```yaml
AnalyticMinimum:
  main_body: at_least_30_percent
  discussion: mostly_analytic
  conclusion: synthesis_without_new_evidence
```

Do not solve weak analysis by adding a detached final sentence. Rewrite the paragraph so evidence and interpretation are adjacent.

## Citation Strategy

Use two citation modes:

1. Intensive-reading citation: one sentence, several sentences, or one paragraph focuses on one core paper. Use this for landmark mechanisms, primary experiments, trials, and paper-specific limitations.
2. Broad-support citation: one synthesis sentence cites several verified sources only when every source supports the same claim.

Formatting and metadata:

- Resolve DOI, PMID, ISBN, arXiv, publisher page, or official source where possible.
- Prefer CSL-compatible formatting and verified metadata. Citation.js or similar CSL-compatible tools may be used when available and license-compatible.
- CSL styles may be used for journal or university styles when available.
- Do not scrape citation-generator websites or copy third-party Skill code without license review.

## Figure, Table, And Data Rules

Directly reuse academic paper images only when the licence or permission allows the intended use. Citation alone is not permission.

If licence or permission is unclear, do not reproduce the image. Create an original source-backed schematic instead.

Use:

```yaml
FigureReuseGate:
  source:
  figure_number:
  licence:
  permission_status:
  can_reuse_directly:
  required_attribution:
```

Generated mechanism figures:

- must be original schematics;
- must represent only source-backed claims;
- must not copy lecture, textbook, paper, or private figure layouts;
- must include a legend stating that the image is generated, original, and not reproduced from a published article or course material.

Data figures:

- Use GraphPad Prism when available and appropriate for the graph and analysis.
- Use Prism scripts or PZFX workflows only through official Prism functionality or license-compatible automation.
- If Prism is unavailable, use a reproducible local analysis workflow and state that Prism output was not generated.
- Report test choice, assumptions, effect size, confidence interval where appropriate, and a concise methods sentence.

Academic tables:

- no vertical lines;
- top rule, header rule, bottom rule;
- concise caption above;
- abbreviation/source note below;
- only include information used by the argument.

## Final QA

The essay fails or must be revised when it contains:

- invented citations;
- unverified source metadata used as verified evidence;
- fake statistics;
- unsupported mechanisms;
- lecture/source-route narration inside essay prose;
- mainly descriptive discussion;
- overclaimed causality;
- paper figure reuse without licence or permission;
- generated figures that introduce unsupported content;
- decorative tables;
- a conclusion with new evidence;
- word-limit violation without warning.
