# Operational Ontology Protocol

The Skill uses an operational ontology to control workflow, evidence permissions, and output generation. The ontology is not a topic taxonomy and not an embedding index. It is an object-link-action model:

```text
SkillConfig -> WorkflowPlan -> SourceDocument -> SourceFragment -> KnowledgePoint -> ExaminerOperation -> QuestionArchetype -> EvidenceClaim -> PrepArtifact -> QAFlag
```

## Purpose

The ontology exists to make exam preparation evidence-bound and auditable:

- the user request becomes a plan before execution;
- source files become typed objects before they influence output;
- links encode what a source is allowed to support;
- actions write back objects, links, artifacts, and QA flags;
- validators block unsupported claims, wrong-regime evidence, unverified citations, and helper artifacts in public output.

## Internal Lakehouse Layers

Treat each exam-prep run as a small auditable data product, not a one-off response. The internal layers are:

```text
Bronze layer
Raw source inventory:
SourceDocument, extraction status, source hash, raw extracted text, slide/page images.

Silver layer
Normalized fragments:
SourceFragment, FragmentPartition, PastPaperQuestion, AssessmentRegime, ExamBlueprint.

Gold layer
Validated semantic objects:
KnowledgePoint, ExaminerOperation, QuestionArchetype, SlotGrammar,
EvidenceClaim, ReadingSource, MethodBlock, QAFlag.

Serving layer
Student-facing artifacts:
Lecture Knowledge Walkthrough DOCX, question-type DOCX reports,
Essay Module Example Essays DOCX, direct answer, plus hidden
diagnostics, lineage, and source audit when requested.
```

Student-visible output may only be generated from Gold objects whose support links pass validation.

## Object Layer

Use `ontology/ontology.json` as the machine-readable contract for object types.

Core objects:

- `UserExamPrepRequest`, `UserConstraint`, `SourceCoverageMap`, `GateResult`, `WorkflowPlan`, and `OutputView`: interaction-layer objects that select mode, plan actions, expose source coverage, and prevent hidden blockers.
- `LectureModule` and `KnowledgeWalkthroughPlan`: Word-first lecture-review objects that preserve lecture order while converting slides or notes into conceptual modules.
- `SourceDocument`: every uploaded or discovered file, with role, trust level, allowed evidence use, and extraction status.
- `SourceFragment`: slide, page, question, figure, table, protocol step, chapter, or section.
- `FragmentPartition`: metadata partition used to prune irrelevant fragments before expensive reasoning or generation.
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
- `RunManifest`: persisted run-level source hashes, actions, object-store paths, artifact list, and QA summary.
- `LineageEvent`: append-only action event linking input objects, output objects, artifacts, and QA flags.

## Fragment Partitioning

Build `FragmentPartition` objects when the run contains multiple source roles, multiple years/regimes, any past-paper prediction, any Example Essay source audit, or any large source set.

Partition metadata should include:

```yaml
FragmentPartition:
  partition_id:
  source_id:
  fragment_ids: []
  source_role:
  analysis_context:
  target_group_key:
  exam_regime:
  year:
  lecture_or_module:
  question_type:
  concept_type:
  command_verbs: []
  input_format:
  image_count:
  extraction_confidence:
  allowed_evidence_use: []
  source_hash:
```

Use partitions as a pruning layer:

- MCQ prep reads MCQ-compatible KPs, MCQ past-paper questions, definition/classification/mechanism/calculation partitions, and visible scoring-policy evidence.
- Example Essay mode reads the relevant lecture scope, citation candidates, verified reading, and essay-relevant evidence partitions; it does not read unrelated answer keys by default.
- Data/problem prep reads graph, table, protocol, case, calculation, readout, control, and limitation partitions.
- QA/lint-only requests read output artifacts and lineage before rerunning upstream analysis.
- Source-inventory-only requests stop at Bronze unless the user asks for deeper processing.

## Link Layer

Links must encode evidence permission, not only semantic similarity.

Allowed examples:

```text
SourceDocument CONTAINS SourceFragment
SourceDocument PARTITIONED_AS FragmentPartition
FragmentPartition GROUPS_FRAGMENT SourceFragment
SourceFragment SUPPORTS_KP KnowledgePoint
SourceFragment SUPPORTS_LECTURE_MODULE LectureModule
KnowledgePoint SUPPORTS_CLAIM EvidenceClaim
PastPaperQuestion INSTANTIATES QuestionArchetype
QuestionArchetype USES_OPERATION ExaminerOperation
KnowledgePoint COMPATIBLE_WITH QuestionArchetype
ReadingSource ENRICHES_KP KnowledgePoint
PrepArtifact GENERATED_FROM_KP KnowledgePoint
PrepArtifact GENERATED_FROM_LECTURE_MODULE LectureModule
PrepArtifact GENERATED_FROM_MCQ_POLICY MCQScoringPolicy
PrepArtifact GENERATED_FROM_SHORT_ANSWER_VARIANT ShortAnswerVariant
PrepArtifact GENERATED_FROM_ESSAY_COVERAGE_PLAN EssayCoveragePlan
PrepArtifact GENERATED_FROM_METHOD_BLOCK MethodBlock
PrepArtifact GENERATED_FROM_PRACTICAL_OPERATION PracticalOperation
QAFlag BLOCKS PrepArtifact
WorkflowRun HAS_MANIFEST RunManifest
WorkflowRun EMITS_LINEAGE LineageEvent
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
ParseUserExamPrepRequest
BuildSourceCoverageMap
SelectOutputView
RecordGateResult
PlanWorkflow
ExtractFragments
BuildFragmentIndex
BuildLectureModules
BuildKnowledgeWalkthroughPlan
NormalizeTargetGroup
SplitExamRegime
ExtractPastPaperQuestions
ClassifyQuestionType
InferQuestionArchetype
SegmentKnowledgePoints
BuildPracticalOperations
BuildMethodBlocks
BuildMCQScoringPolicy
GenerateShortAnswerVariants
BuildEssayCoveragePlan
MapKPToArchetype
VerifyReadingSource
GeneratePrepArtifact
CreateWorkflowRun
ValidateOntologyRuntime
WriteRunManifest
RunDeliverableQA
ApproveStudentOutput
```

Actions may use helper scripts, but production behaviour must be controlled by object properties, link types, and validation rules rather than benchmark names or source-set identity.

## Query Discipline

Student-facing artifacts should be generated from eligible ontology queries, not direct raw-file concatenation.

Workflow plan preview query:

```text
request scope + selected preset + target + actions + skipped modules + blockers + publish gate
```

Knowledge walkthrough query:

```text
lecture order + lecture overview + module map + lecture modules + key logic + common confusions + lecture recap
```

Student output filter query:

```text
internal objects + selected output mode + allowed visible fields + forbidden visible fields
```

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
internal_qa/ontology_objects/workflow_plans.jsonl
internal_qa/ontology_objects/source_fragments.jsonl
internal_qa/ontology_objects/fragment_partitions.jsonl
internal_qa/ontology_objects/past_paper_questions.jsonl
internal_qa/ontology_objects/question_archetypes.json
internal_qa/ontology_objects/evidence_claims.jsonl
internal_qa/ontology_links/links.jsonl
internal_qa/run_manifest.json
internal_qa/lineage_events.jsonl
internal_qa/input_readiness.json
internal_qa/workflow_plan.md
```

These files are helper artifacts. They must not be mixed into the final user-facing output unless the user explicitly requests an audit package.

## Validation Gates

Fail or block student-facing output when:

- a claim has no source anchor;
- an ontology object has no writer action;
- the requested output mode has no selected `OutputView`;
- a major generation path has no `WorkflowPlan`;
- student-facing output exposes internal evidence, confidence, source-anchor, discriminator, task-verb, or examiner-operation fields;
- a knowledge walkthrough follows slide/page order instead of conceptual module order;
- the source coverage map hides a blocking gap;
- a source role is not allowed to support the claim;
- old-regime evidence controls current-regime prediction;
- external examples provide factual or prediction content;
- a citation or extra-reading source is not verified/read where required;
- output mode does not match the detected question type;
- a prediction claims exact future wording, guarantee, or fake numerical precision;
- a student-facing artifact has no valid Gold-object lineage;
- a blocking QA flag is unresolved;
- a publish action has no run manifest or lineage event;
- public output contains helper artifacts.

## Control-Plane Invariants

Use these as hard publish gates:

```text
No object -> no link.
No valid link -> no claim.
No verified claim -> no student-facing synthesis.
No lineage -> no reproducible publish.
No QA pass -> no publish.
```

Do not implement distributed compute, warehouses, or platform-specific services. The transferable idea is local metadata, pruning, validation, lineage, and reproducibility.
