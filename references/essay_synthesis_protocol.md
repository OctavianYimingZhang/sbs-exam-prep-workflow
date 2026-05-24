# Essay Synthesis Protocol

This file is the compatibility entry point for earlier workflow prompts that asked for `essay_synthesis_protocol.md`.

Use `references/kp_essay_synthesis_protocol.md` as the legacy/internal protocol for KP-level essay synthesis linting.

Use `references/essay_generation_protocol.md` as the operative protocol for:

- Example Essay Mode;
- lecture-logic extraction;
- knowledge inventory;
- lecturer-intent analysis;
- paragraph planning;
- extra-reading insertion;
- mechanism-heavy essay contribution checks from benchmark fixtures;
- comparison-axis and style-exemplar contribution checks from benchmark fixtures;
- DOCX-first output for explicit Example Essay Mode;
- paragraph-row exports only as optional audit artefacts when explicitly requested.

KP synthesis and full Example Essay Mode are separate:

- KP synthesis writes one compact concept-first paragraph fragment per knowledge point.
- Example Essay Mode writes complete answers only when essay prep or Example Essays are explicitly requested and exports `Essay_Module_Example_Essays.docx` by default, or one standalone DOCX per essay when separate files are requested.

If this file and `kp_essay_synthesis_protocol.md` appear to conflict for KP-level prose linting, follow `kp_essay_synthesis_protocol.md`. If this file and `essay_generation_protocol.md` appear to conflict for full Example Essays, follow `essay_generation_protocol.md`.
