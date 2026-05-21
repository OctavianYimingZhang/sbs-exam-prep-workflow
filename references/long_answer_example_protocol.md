# Long-Answer Example Protocol

Use this protocol when a unit uses non-essay, paragraph-style, project/scenario-based long answers. The output should read as a high-score experimental argument, not as a broad essay.

The BIOL21111 Proteins benchmark demonstrates the transferable rule for method-driven project/scenario exams. It is regression evidence for this workflow, not a Proteins-only trigger or content template. Apply this protocol to future units only when current exam-format parsing shows project, scenario, method-design, readout-interpretation, or research-proposal structure.

## A. Source Digestion Before Writing

Before planning or drafting:

- read every lecture slide/page in source order;
- inspect rendered slide/page images when diagrams, structures, gels, spectra, graphs, or handwritten exemplar answers matter;
- preserve lecture logic before segmenting: why the lecture is taught in this order, what method or mechanism is introduced, what evidence/readout it produces, and what limitation follows;
- use student English exemplars only for answer structure, paragraph logic, density, and wording style;
- ignore student Chinese annotations as factual course content unless the user explicitly asks to use them as notes;
- do not use exemplar biological claims as facts unless verified from official lecture material or reliable academic sources.

The BIOL21111 benchmark demonstrates that lecture digestion for method-heavy project exams may need to separate method families such as:

- protein purification and characterisation;
- folding, stability, chaperones, and activity;
- binding and affinity measurements;
- enzyme catalysis, mutation, and rational design;
- structural biology method choice;
- in vivo or biotechnological caveats.

Do not transfer these protein-specific method families to another unit unless the target unit's own sources contain them. The transferable contribution is the separation of method principle, scenario application, readout, interpretation, and limitation.

## B. Knowledge Inventory For Writing

Construct this inventory before writing a long answer:

```yaml
KnowledgeUseInventory:
  must_use_core:
    - lecture points directly required by the question
  should_use_if_space:
    - supporting lecture points that improve precision
  method_principle:
    - the examinable principle of each method
  scenario_application:
    - how the method applies to the named protein/system
  readout_and_interpretation:
    - what the experimental output would show and how it answers the question
  controls_or_limitations:
    - caveats, controls, alternative methods, or weaknesses
  cross_module_links:
    - legitimate links to other lecture blocks in the same unit
  outside_module_but_relevant:
    - verified extra-reading material that can refine the answer briefly
  exclude:
    - true but non-useful lecture facts for this question
```

Prioritise lecture material that directly answers the command verb. Exclude methods that are true but not justified by the scenario.

## C. Lecturer And Module Pattern Inference

The detector must test, not assume:

- one lecturer gives one question;
- one module gives one question;
- one lecture gives one question;
- one knowledge point gives one question;
- cross-module synthesis;
- experiment-design slot;
- structural-method slot;
- binding/affinity slot;
- purification/characterisation slot;
- mutation/rational-design slot;
- in vivo limitation slot.

For method-driven project/scenario papers structurally similar to the BIOL21111 benchmark, infer whether recent formal papers combine several lecturers' material inside one research-project question. Do not write by lecturer in isolated blocks unless the question itself is split that way.

## D. Long-Answer Paragraph Planning

Every long answer must be planned paragraph-by-paragraph before drafting:

```yaml
LongAnswerParagraphPlan:
  paragraph_no:
  question_part:
  paragraph_function:
    - strategy_framing
    - core_biological_mechanism
    - method_principle
    - method_application
    - readout_interpretation
    - comparison_choice
    - limitation_control
    - extra_reading_refinement
    - concluding_integration
  claim_or_goal:
  lecture_kps_used:
  scenario_facts_used:
  method_or_mechanism:
  expected_readout:
  interpretation:
  control_or_limitation:
  extra_reading_use:
  excluded_content:
  word_budget:
```

The plan should follow question parts and mark weighting. If a part has higher marks, allocate more explanation, readout interpretation, and controls.

## E. Required Paragraph Logic

Default paragraph logic:

```text
question goal -> lecture principle -> scenario-specific application -> expected evidence/readout -> interpretation -> limitation/control
```

Useful internal pattern:

- To determine X, first establish Y.
- This method is appropriate because it measures, separates, or detects Z.
- Given scenario fact A, apply the method as B.
- If the hypothesis is correct, the expected readout is C.
- This would indicate D.
- The main limitation is E, so include control or alternative F.

Do not write generic topic summaries. Every sentence must answer the command verb, justify method choice, connect knowledge to the scenario, interpret a readout, or add a necessary caveat/control.

## F. Style Language Bank

Use compact academic language:

Purpose framing:

- `To address this question, I would first...`
- `The central experimental problem is to determine whether...`

Scenario anchoring:

- `Given that [protein/system fact], [method] is appropriate because...`
- `Because the question specifies [fact], the answer should focus on...`

Principle-to-application:

- `[Technique] works by [principle]; therefore, in this case it can be used to...`

Sequential logic:

- `Once [purity/fold/oligomeric state/activity] has been established, [next method] can then be used...`

Readout interpretation:

- `A shift/loss/increase/decrease in [signal] would indicate...`
- `If the mutant behaves as intended, one would expect...`

Contrast:

- `This method is preferable to [alternative] here because...`
- `However, this alone would not prove..., so it should be combined with...`

Limitation/control:

- `The main caveat is...`
- `A suitable control would be...`
- `This should be checked because...`

Avoid decorative introductions, repeated vague phrases, unconnected method lists, and padding. A word limit is a maximum, not a target.

## G. Extra-Reading Insertion

Extra reading must be a compact refinement, not a second answer.

Source hierarchy:

1. recommended reading explicitly listed in unit slides or handouts;
2. books recommended by the lecturer or unit handbook;
3. papers named in lecture slides;
4. peer-reviewed reviews or primary papers from PubMed, Google Scholar, DOI, or publisher pages;
5. standard textbooks.

If recommended reading is not present in uploaded material, ask the user whether the unit has a recommended reading list. If the user says no, unknown, or gives no usable list, use verified academic papers or textbooks only.

Extra reading may appear only as:

- one short paragraph;
- two to four integrated sentences;
- one named method example;
- one method-limitation clarification;
- one directly relevant modern/application context.

Extra-reading refinements demonstrated by the BIOL21111 benchmark include the following examples. Transfer the refinement type only when the target unit sources and exact question contain matching methods:

- one BN-PAGE method sentence if the question concerns native complexes;
- one DsbA substrate-identification sentence if the question concerns non-reducing/reducing 2D SDS-PAGE;
- one cryo-EM limitation sentence if the question concerns EM;
- one extinction-coefficient refinement if the question concerns A280 concentration determination.

Reject unrelated disease detail, unverified citations, multiple extra-reading paragraphs, or any external point that changes the lecture answer.

## H. Method-Driven Long-Answer Project Archetypes Learned From BIOL21111 Benchmark

Apply these archetypes to future units only when exam-format parsing confirms scenario, project, method-design, or readout-interpretation structure. Do not transfer protein-specific systems, techniques, or recurrence claims unless supplied in the new unit's sources.

Transferable operation archetypes:

- design purification strategy;
- choose and justify characterisation methods;
- assess folding, secondary, tertiary, or quaternary structure;
- quantify binding affinity or dimerisation affinity;
- interpret mutation effect;
- determine protein-protein interface;
- determine atomic or high-resolution structure;
- compare X-ray, NMR, cryo-EM, AlphaFold, or modelling by suitability;
- quantify enzyme activity or substrate specificity;
- explain chaperone/folding mechanism;
- identify in vivo or biotechnological caveats.

For every archetype, include:

- lecture principle;
- scenario-specific method choice;
- expected readout;
- interpretation;
- limitation/control.

## I. BIOL21111 Regression Expectations (Fixture Only)

The following items are regression assertions for the BIOL21111 fixture. They must not be used as production triggers or as content predictions for another unit.

Current formal regime:

- 2023, 2024, and 2025 should be treated as project/scenario long-answer evidence.
- 2015 and 2021 may inform concept coverage only unless exam-format parsing proves comparability.

Expected project mappings:

- 2023 Ept/Hi: mutation design, purification, enzyme specificity, affinity, and structural determination operations.
- 2024 Protein A/G: chaperone co-expression, purification, integrity, antibody affinity, linker design, and interface determination.
- 2025 HdeA: chaperone mechanism, purification, unfolding/secondary structure, dimerisation affinity, pH-sensitive mutation, and atomic structure determination.

Behavioural tests:

- For HdeA activity at pH 2, produce planned paragraphs for chaperone principle/hydrophobic exposure, purification of native HdeA, CD or fluorescence for unfolding/secondary structure, a suitable contact-residue method if justified, and controls/caveats.
- For His-tagged protein purification and oligomeric state, connect IMAC, lysis/clarification, adsorption/wash/elution, optional tag cleavage, SEC/BN-PAGE/native methods, A280/SDS-PAGE/CD/fluorescence checks, and expected elution/readout.
- For structural determination, select between X-ray, NMR, cryo-EM, AlphaFold, or modelling by size, stability, crystallisation, flexibility, concentration, complex size, resolution, and the question aim.

## J. QA Flags

Add or use these flags when relevant:

- `long_answer_project_scope_uncertain`;
- `paragraph_plan_missing`;
- `method_principle_missing`;
- `scenario_fact_not_used`;
- `expected_readout_missing`;
- `interpretation_missing`;
- `control_or_limitation_missing`;
- `generic_essay_written_for_project_question`;
- `old_regime_used_as_current_blueprint`;
- `extra_reading_unverified`;
- `example_used_as_fact`.

Fail-safe by omitting uncertain mechanisms, citations, or lecturer preferences rather than inventing them.

## K. Output Contract

Direct-chat high-score example long answers should use:

```text
Question Deconstruction
Knowledge Inventory
Paragraph Plan
High-Score Example Long Answer
Optional Extra-Reading Refinement
Self-Check
```

In Excel, split long answers by paragraph rows. Include question part, paragraph text, paragraph function, lecture KPs used, scenario facts used, method/readout/interpretation, extra-reading use, why included, and excluded content.
