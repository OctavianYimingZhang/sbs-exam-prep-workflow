# Scientific Precision Protocol

This protocol controls the precision layer for scientific, biomedical, clinical, quantitative, methodological and sector-level writing. It prevents high-density output from becoming a list of true but unstructured details.

```text
EvidenceClaim -> EntityPrecisionPass -> CategoryMatchedSentenceRule -> EvidenceLadderRule -> MechanismPerDetailRule -> ClaimStrengthCalibration -> Student prose
```

## Purpose

High-scoring notes and essays need more than correct facts. They need the correct entity type, the correct evidence strength, and a clear reason why each named detail matters.

A named detail may enter public prose only when it performs a function:

- sharpens a source-backed mechanism;
- distinguishes one model, pathway, method, cell type, molecule, case or sector mechanism from another;
- explains what an experiment, assay, graph, figure or dataset shows;
- defines a scope boundary or limitation;
- links a molecular/cellular/method detail to the question-level answer.

## Entity Precision Pass

Before final prose, collapse aliases and classify named entities.

```yaml
EntityPrecisionRecord:
  entity:
  aliases:
  entity_category:
    - gene
    - transcript
    - protein
    - receptor
    - channel
    - ligand_or_morphogen
    - cell_type
    - circuit_element
    - anatomical_structure
    - pathway
    - assay
    - method
    - chemical_species
    - disease_or_patient_group
    - company_or_case
    - regulatory_body
    - quantitative_parameter
  source_anchor:
  allowed_claim_type:
  student_visible_decision:
```

Rules:

- Do not mix entity categories inside one sentence unless the relation between categories is explicit.
- Do not use a gene name as if it were the protein, receptor, pathway or disease phenotype unless the source supports that wording.
- Collapse synonyms before writing so the output does not look like a catalogue of separate items.
- When a term is ambiguous, state the precise level or omit the detail.

## Category-Matched Sentence Rule

Each sentence should match grammar to the category it names.

Examples:

- A gene can encode a protein, carry a mutation, contain an expansion or alter expression.
- A protein can bind, aggregate, mislocalise, phosphorylate, transport, catalyse or interact.
- A receptor or channel can gate, signal, open, close, desensitise or change downstream output.
- An assay can measure, detect, compare or validate; it cannot by itself prove disease causality.
- A patient cohort or model can support, implicate or test a mechanism; it does not automatically prove universal human causation.
- A company or case can illustrate a sector mechanism; it does not become the sector mechanism itself.

Reject sentences that list entities from different categories without stating their causal or evidential relation.

## Evidence Ladder Rule

When several evidence streams support one mechanism, write them as an evidence ladder rather than a flat list.

```text
source observation -> model or assay result -> mechanism tested -> interpretation -> scope or limitation
```

For scientific essays, common ladders include:

```text
patient evidence -> cell model -> animal model -> treatment logic -> calibrated conclusion
lecture experiment -> assay readout -> mechanism -> limitation
genetic lesion -> molecular consequence -> cellular phenotype -> system-level effect
```

For sector/system essays, common ladders include:

```text
market problem -> platform mechanism -> firm example -> sector implication -> limitation
```

The ladder should preserve claim strength. Association stays association; rescue or perturbation can support causality only within its model and conditions.

## Mechanism-Per-Detail Rule

Every named detail must earn its word count.

Accept a named detail only when at least one is true:

- it changes the causal mechanism;
- it names the specific object measured or manipulated;
- it explains why an experiment supports or limits a claim;
- it distinguishes one answer option, model, pathway, method or disease subtype from another;
- it directly improves revision accuracy or exam transfer.

Reject the detail when:

- it is true but not needed for the question;
- it creates a gene/channel/receptor/pathway/company catalogue;
- it requires a new explanatory paragraph not supported by the question scope;
- it shifts the answer away from the lecture/source mechanism;
- it is used only to increase molecular, mechanism or extra-reading volume.

## Claim Strength Calibration

Use calibrated verbs:

| Source situation | Preferred wording | Avoid |
|---|---|---|
| correlation, association or altered abundance | associated with, linked to, consistent with | proves, causes |
| perturbation changes a model readout | supports, contributes to, is required under these conditions | universally proves |
| rescue experiment restores a phenotype | supports a causal role in that model | proves sole cause |
| review-level synthesis | suggests, implicates, supports a model | demonstrates directly |
| company/case example | illustrates, shows a route, exemplifies | proves sector-wide rule |

## ScientificPrecisionGate

Run this gate before final notes, long answers and Example Essays.

```yaml
ScientificPrecisionGate:
  entity_precision_pass:
  alias_collapse_pass:
  category_matched_sentence_pass:
  evidence_ladder_pass:
  mechanism_per_detail_pass:
  claim_strength_pass:
  qa_flags:
```

Fail or rewrite when:

- a sentence mixes entity categories without relation;
- a detail has no mechanism or evidence function;
- a claim overstates the source;
- a named list replaces explanation;
- extra reading replaces lecture logic;
- academic-paper content lacks parenthetical author-year citation where required;
- a biological, clinical, method or sector example is used as direct factual authority for a new target source set without verification.

## Route Integration

- `exam_prep_notes_docx`: apply to public points and calculation/method/graph explanations.
- `knowledge_walkthrough_docx`: apply to conceptual walkthrough prose and synthesis blocks.
- `essay_exam_prep`: apply after paragraph planning and again after compression.
- `long_answer_project_scenario_prep`: apply to method/readout/interpretation/control paragraphs.
- `mcq_exam_prep` and `short_answer_exam_prep`: apply to point cards so distractors and concise answers do not blur entities or claim strength.

Scientific precision is not a request to add more detail. It is a filter that keeps only the detail that improves the answer's mechanism, evidence or decision value.
