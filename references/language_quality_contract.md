# Language Quality Contract

This contract is the shared prose-quality standard for workbook KP explanations, Example Essays, long-answer model answers, and any essay-style revision output.

The contract is subject-independent. Biological, chemical, quantitative, clinical, methodological, and sector-level essays use different factual evidence, but the same language discipline.

## Core Paragraph Shape

Every substantive paragraph should have a visible function:

```text
claim or problem -> mechanism/process/evidence -> scope or limitation -> consequence -> link back
```

Acceptable variants:

- `debate -> model A -> model B -> evidence -> evaluation`;
- `question demand -> method principle -> readout -> interpretation -> control`;
- `shared problem -> comparison axis -> contrast -> synthesis`;
- `sector/system problem -> example evidence -> implementation mechanism -> wider implication`.

## Required Rules

- Start with the answer or problem, not with metacommentary.
- Preserve necessary mechanisms when compressing language.
- Remove repeated definitions, repeated claims, decorative transitions, and low-value case details.
- Use examples as evidence for a wider claim.
- Make contrasts explicit; do not rely on ambiguous `rather than` phrasing.
- Separate model, mechanism, evidence, and implication when a question asks for evaluation.
- Use citations only for non-obvious facts, theories, mechanisms, methods, evidence, data, or broad generalisations.
- Avoid citation stacking; one precise citation is usually better than several weakly connected citations.
- Do not invent statistics, dates, mechanisms, source names, quotations, or citations.
- Conclude by synthesis. Do not add new evidence in the conclusion.

## Banned Patterns

Reject or rewrite paragraphs that:

- narrate pages or slides instead of giving the argument;
- say how the student should write instead of writing the answer;
- list examples without explaining what they prove;
- repeat the question using different words without adding mechanism;
- overuse broad claims such as `this is important` without specifying consequence;
- hide uncertainty behind confident language;
- use a citation copied from lecture slides without verifying the original source when source-derived content is included.

## Compression Standard

Compression is not sentence shortening. It is function filtering.

For each sentence, ask:

```text
Does it state the claim?
Does it explain the mechanism/process?
Does it provide evidence or an example that changes the answer?
Does it define the scope, limitation, or contrast?
Does it link back to the question?
```

Delete or merge sentences that do none of these.

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
- extra-reading material matched to a chapter or section;
- online academic sources verified by DOI, PubMed, publisher page, textbook, or equivalent academic source.

## Completion Standard

Language quality is acceptable only when:

- no high-severity language linter failures remain;
- no medium-severity gap remains without an explicit reason;
- the source audit supports factual claims;
- Example Essay DOCX formatting and source-highlight rules pass;
- no benchmark or course identity is used as a production trigger.
