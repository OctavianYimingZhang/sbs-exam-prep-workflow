# Language Quality Contract

This contract is the shared prose-quality standard for lecture walkthrough explanations, question-type reports, Example Essays, long-answer model answers, and any essay-style revision output.

The contract is subject-independent. Biological, chemical, quantitative, clinical, methodological, and sector-level essays use different factual evidence, but the same language discipline.

## Core Paragraph Shape

Every substantive paragraph should have a visible function:

```text
claim or problem -> mechanism/process/evidence -> scope or limitation -> consequence -> link back
```

Acceptable variants:

- `debate -> model A -> model B -> evidence -> evaluation`;
- `evidence -> mechanism -> interpretation -> limitation`;
- `question demand -> method principle -> readout -> interpretation -> control`;
- `shared problem -> comparison axis -> contrast -> synthesis`;
- `sector/system problem -> example evidence -> implementation mechanism -> wider implication`.

## Required Rules

- Start with the answer or problem, not with metacommentary.
- Preserve necessary mechanisms when compressing language.
- Remove repeated definitions, repeated claims, decorative transitions, and low-value case details.
- Remove lecture-route narration and exam-guidance phrasing from the answer body.
- Add words only when they add mechanism, evidence, interpretation, limitation, or a required contrast.
- Add named biological, chemical, quantitative, clinical, methodological, or sector-specific detail only when it sharpens a lecture/source-derived mechanism slot or evidence function.
- When writing essay/problem-essay prediction outputs, phrase the prediction as an examinable theme with scope and operation, not as a guaranteed future question.
- Use examples as evidence for a wider claim.
- Convert experiments, data, and examples into evidence, mechanism, interpretation, and limitation when the question is evidence-heavy.
- Make contrasts explicit; do not rely on ambiguous `rather than` phrasing.
- Separate model, mechanism, evidence, and implication when a question asks for evaluation.
- Use citations only for non-obvious facts, theories, mechanisms, methods, evidence, data, or broad generalisations.
- Calibrate citation strength. Use `supports`, `implicates`, `is consistent with`, or `contributes to` unless the verified source directly proves causality.
- Avoid citation stacking; one precise citation is usually better than several weakly connected citations.
- Do not invent statistics, dates, mechanisms, source names, quotations, or citations.
- If the user supplies no Example Essay citations, cite only sources found by slide-citation mining or verified classic-experiment fallback; never cite from memory.
- Conclude by synthesis. Do not add new evidence in the conclusion.

## Banned Patterns

Reject or rewrite paragraphs that:

- narrate pages or slides instead of giving the argument;
- narrate the lecture/source route instead of giving the answer;
- say how the student should write instead of writing the answer;
- include exam-guidance sentences such as telling the student what the final thesis should be;
- list examples without explaining what they prove;
- repeat the question using different words without adding mechanism;
- overuse broad claims such as `this is important` without specifying consequence;
- hide uncertainty behind confident language;
- turn supporting or associative evidence into a single-cause claim;
- use a citation copied from lecture slides without verifying the original source when source-derived content is included.
- include a list of named channels, receptors, genes, cell classes, methods, examples, firms, or pathways without explaining what the list proves or distinguishes;
- use true but unneeded detail that makes the answer more encyclopedic but less exam-efficient;
- compress wording so that a modulating, gating, entraining, stabilising, supporting, or associative mechanism becomes the primary generator or proof.

## Compression Standard

Compression is not sentence shortening. It is function filtering.

For each sentence, ask:

```text
Does it state the claim?
Does it explain the mechanism/process?
Does it provide evidence or an example that changes the answer?
Does it interpret what that evidence proves and what it does not prove?
Does it define the scope, limitation, or contrast?
Does it link back to the question?
```

Delete or merge sentences that do none of these.

Compression must preserve causal strength, scope qualifiers, negative distinctions, model boundaries, and evidence interpretation. Do not rewrite `not necessary for generating the core rhythm` as `not necessary for locomotion`, or `supports a mechanism` as `proves the mechanism`, unless the source warrants the stronger claim.

## Detail-Level Discipline

Named detail is valuable only when it improves the answer's function. Do not include a list of channels, receptors, nuclei, genes, cell classes, molecules, methods, firms, case names, equations, or pathways unless the lecture/source logic or exact question requires that level.

When a list is illustrative, compress it to a higher-level mechanism. When a list is examiner-relevant, keep only the items that distinguish mechanisms, evidence, limitations, or consequences.

For every named detail, ask:

- Does this detail map to a PPT/source mechanism slot?
- Does it distinguish this mechanism from another?
- Does it explain an experiment, method readout, clinical consequence, sector consequence, or limitation?
- Would deleting it make the answer less accurate, or only less encyclopedic?

## Analytic-Over-Descriptive Standard

A paragraph fails if it contains more than two consecutive descriptive sentences without an analytic sentence.

A valid analytic sentence must do at least one of the following:

- explain why the mechanism solves a control, causal, methodological, clinical, or sector-level problem;
- state what an experiment, example, dataset, or figure proves or fails to prove;
- compare two models, pathways, cases, mechanisms, or methods;
- define the scope or boundary of a claim;
- link a named detail to system-level function or the essay question.

## Example Use

Examples, case studies, firms, organisms, diseases, methods, figures, calculations, or datasets should be treated as evidence slots.

Allowed:

```text
The example demonstrates the mechanism because...
```

Forbidden:

```text
Example A happened. Example B happened. Example C happened.
```

## Citation Discipline

Use the smallest citation set that supports the claim. Do not cite:

- obvious lecture framing;
- generic background;
- every sentence in a paragraph;
- unsupported material copied from another essay.

Use citations for:

- original papers cited by lecture slides and actually read;
- verified classic experiments or landmark primary studies found because relevant lecture slides contain no usable citations;
- extra-reading material matched to a chapter or section;
- online academic sources verified by DOI, PubMed, publisher page, textbook, or equivalent academic source.

## Completion Standard

Language quality is acceptable only when:

- no high-severity language linter failures remain;
- no medium-severity gap remains without an explicit reason;
- the source audit supports factual claims;
- Example Essay DOCX formatting and source-highlight rules pass;
- no benchmark or course identity is used as a production trigger.
