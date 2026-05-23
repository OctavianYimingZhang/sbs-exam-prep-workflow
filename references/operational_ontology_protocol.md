# Operational Ontology Protocol

The Skill uses an operational ontology to control workflow, evidence permissions, and output generation. The ontology is not a topic taxonomy and not an embedding index. It is an object-link-action model:

```text
SourceDocument -> SourceFragment -> KnowledgePoint -> ExaminerOperation -> QuestionArchetype -> EvidenceClaim -> PrepArtifact -> QAFlag
```

## Purpose

The ontology exists to make exam preparation evidence-bound and auditable:

- source files become typed objects before they influence output;
- links encode what a source is allowed to support;
- actions write back objects, links, artifacts, and QA flags;
- validators block unsupported claims, wrong-regime evidence, unverified citations, and helper artifacts in public output.

## Object Layer

Use `ontology/ontology.json` as the machine-readable contract for object types.

Core objects:

- `SourceDocument`: every uploaded or discovered file, with role, trust level, allowed evidence use, and extraction status.
- `SourceFragment`: slide, page, question, figure, table, protocol step, chapter, or section.
- `AssessmentRegime` and `ExamBlueprint`: current versus old exam structures.
- `PastPaperQuestion`: question-level record extracted from a paper.
- `KnowledgePoint`: examinable reasoning block, not a raw topic label.
- `ExaminerOperation`: task verb, input format, cognitive operation, answer shape, and marking logic.
- `QuestionArchetype`: recurrent question-family skeleton with slot grammar.
- `EvidenceClaim`: answer claim with source anchors and support strength.
- `ReadingSource`: recommended book, paper, DOI/PubMed/publisher record, or verified academic source.
- `PracticalOperation`, `MethodBlock`, `MCQScoringPolicy`, `ShortAnswerVariant`, and `EssayCoveragePlan`: type-specific preparation objects.
- `PrepArtifact`: student-facing or internal output.
- `QAFlag`: blocking or warning condition.
- `WorkflowRun`: modules run, modules skipped, outputs created, and QA summary.

## Link Layer

Links must encode evidence permission, not only semantic similarity.

Allowed examples:

```text
SourceDocument CONTAINS SourceFragment
SourceFragment SUPPORTS_KP KnowledgePoint
KnowledgePoint SUPPORTS_CLAIM EvidenceClaim
PastPaperQuestion INSTANTIATES QuestionArchetype
QuestionArchetype USES_OPERATION ExaminerOperation
KnowledgePoint COMPATIBLE_WITH QuestionArchetype
ReadingSource ENRICHES_KP KnowledgePoint
QAFlag BLOCKS PrepArtifact
```

Forbidden examples:

```text
cross_target_example SUPPORTS_FACTUAL_CLAIM EvidenceClaim
old_or_different_regime CONTROLS_CURRENT_BLUEPRINT ExamBlueprint
unverified_external_source SUPPORTS_CLAIM EvidenceClaim
unreadable_source SUPPORTS_KP KnowledgePoint
```

## Action Layer

Every workflow step should be expressible as an action that reads objects and writes objects, links, or QA flags:

```text
CreateSourceInventory
ExtractFragments
NormalizeTargetGroup
SplitExamRegime
ExtractPastPaperQuestions
ClassifyQuestionType
InferQuestionArchetype
SegmentKnowledgePoints
MapKPToArchetype
VerifyReadingSource
GeneratePrepArtifact
RunDeliverableQA
ApproveStudentOutput
```

Actions may use helper scripts, but production behaviour must be controlled by object properties, link types, and validation rules rather than benchmark names or source-set identity.

## Query Discipline

Student-facing artifacts should be generated from eligible ontology queries, not direct raw-file concatenation.

Essay theme query:

```text
current regime + essay archetype + compatible KPs + lecture scope + confidence band + QA flags
```

MCQ prep query:

```text
MCQ archetype + discriminator axes + distractor families + scoring policy + confidence band
```

Practical/data query:

```text
input type + required operation + expected inference + limitation/control + follow-up
```

Extra-reading insertion query:

```text
verified reading source + matched KP + matched chapter/section + sentence-budget decision
```

## Runtime Object Store

When an implementation persists ontology outputs, use JSONL or JSON under an internal QA directory, not in the public student deliverable folder:

```text
internal_qa/ontology_objects/source_documents.jsonl
internal_qa/ontology_objects/source_fragments.jsonl
internal_qa/ontology_objects/past_paper_questions.jsonl
internal_qa/ontology_objects/question_archetypes.json
internal_qa/ontology_objects/evidence_claims.jsonl
internal_qa/ontology_links/links.jsonl
```

These files are helper artifacts. They must not be mixed into the final user-facing output unless the user explicitly requests an audit package.

## Validation Gates

Fail or block student-facing output when:

- a claim has no source anchor;
- a source role is not allowed to support the claim;
- old-regime evidence controls current-regime prediction;
- external examples provide factual or prediction content;
- a citation or extra-reading source is not verified/read where required;
- output mode does not match the detected question type;
- a prediction claims exact future wording, guarantee, or fake numerical precision;
- public output contains helper artifacts.
