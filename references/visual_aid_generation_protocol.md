# Visual Aid Generation Protocol

Generated images are optional revision aids. They are never factual authorities, official course figures, or substitutes for reading supplied sources.

Use this protocol only after the text content is already source-backed and the selected route would benefit from a schematic.

For essay-specific figure, table, or data decisions, also apply `essay_tutor_workflow_protocol.md`.

## When To Use

Use a visual aid only when all conditions hold:

- the platform supports image generation or diagram generation;
- the concept benefits from visual structure;
- every represented claim is already supported by accepted sources;
- the schematic can be made without copying a lecture, textbook, article, or private figure.

Usually useful:

- mechanism pathway;
- process sequence;
- spatial relation;
- comparison framework;
- method workflow;
- data-interpretation logic.

Usually not useful:

- definition-only content;
- pure essay thesis;
- unsupported student-note claim;
- content that would require copying a supplied figure.

## Hard Boundaries

Do not:

- introduce new facts through an image;
- reproduce copyrighted lecture, textbook, article, or private figures;
- create exact diagrams from supplied slides;
- imply the image is official course material;
- use visual style to increase confidence in a weak claim;
- use generated images as citation, evidence, or answer authority.
- reproduce academic paper, textbook, lecture, or private figures unless licence or permission allows the intended use. Citation alone is not permission.

If generation is unavailable, skip the visual aid silently in student-facing output and attach the internal flag `visual_aid_skipped_platform_unavailable` when an audit package is requested.

## Figure Reuse Gate

Before reusing any published figure, table image, chart, or adapted visual, record:

```yaml
FigureReuseGate:
  source:
  figure_or_table_number:
  licence:
  permission_status:
  can_reuse_directly:
  required_attribution:
```

If permission or licence is unclear, do not reproduce the image. Create an original schematic or an academic table from cited claims instead.

## VisualAidSpec

Create an internal spec before generation:

```yaml
VisualAidSpec:
  visual_aid_id:
  kp_id:
  aid_type: mechanism_pathway | process_sequence | spatial_relation | comparison_framework | method_workflow | data_interpretation_logic
  source_backed_claims: []
  visual_elements: []
  caption:
  alt_text:
  generation_prompt:
  forbidden_elements: []
  qa_flags: []
```

The prompt must be schematic and generic. It should describe relationships and labels, not ask for a copy of a supplied figure.

## Caption Contract

Use this caption or a close equivalent:

```text
Generated schematic for revision. It illustrates the source-backed mechanism; it is not an official course figure.
```

If a subject-specific caption is needed, keep the official-figure boundary explicit.

## Visual Aid QA

Before embedding or attaching a visual aid, check:

- all labels correspond to source-backed claims;
- no unsupported mechanism, direction, number, date, citation, source name, or official answer appears;
- no private or copyrighted source figure has been copied;
- licence or permission exists for any reused published visual;
- the caption states the image is generated for revision;
- the visual does not replace the written explanation.

Block or rewrite the visual aid when any check fails.

## Tables And Data Figures

Tables must be argument-useful, not decorative. Use academic styling: no vertical lines, top rule, header rule, bottom rule, caption above, and abbreviation/source note below.

For user-supplied data, use GraphPad Prism when available and appropriate for the final graph. If Prism is unavailable, use a reproducible local analysis workflow and state that Prism output was not generated. Report test choice, assumptions, effect size and confidence interval where appropriate, and a concise methods sentence.
