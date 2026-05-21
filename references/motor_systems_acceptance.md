# Motor Systems Contribution / Acceptance Criteria

This file is a regression acceptance file for the Motor Systems benchmark. It also contributes generic rules for answer-one regime detection, old-regime exclusion from current blueprint prediction, and slide-aligned visual workbook output. Motor-specific topics must not be transferred to other Units unless they are present in the target Unit's own supplied sources.

## Generic Contribution Summary

Observed Motor Systems behaviour:

- older papers contain answer-all short-answer/problem-style evidence;
- recent papers use answer-one essay/problem-essay formal evidence;
- the student-facing workbook is most usable when lecture locator, original slide image, essay-style explanation, and prediction area are aligned horizontally in source order.

Transferable rule:

- for any future Unit, compare answer rule, section structure, question family, timing, and mark weighting across years before pooling papers;
- if old papers have a different answer regime, use them for coverage/schema evidence only;
- for visually taught slide units, preserve first-to-last lecture order and align source image, explanation, and exam-facing preparation output.

Non-transferable content:

- MND/ALS, Brain Machine Interface, C9orf72, basal ganglia/Parkinson's, superior colliculus, vestibular scenarios, and all Motor-specific topic recurrence.

## Motor Systems Regression Acceptance Criteria

In the Motor Systems regression benchmark, expected behaviour:

1. Classify 2017 and 2018 papers as answer-all short-answer/problem-style papers.
2. Do not use 2017/2018 as direct essay-prediction evidence.
3. Use 2023, 2024, and 2025 as high-comparability answer-one essay/problem-essay formal papers.
4. Detect that 2023-2025 are `Answer ONE question` papers.
5. Detect essay/problem-essay themes:
   - MND/ALS disease mechanism;
   - Brain Machine Interface;
   - locomotion/CPG/proprioception/vestibular input;
   - M1 mapping experimental design;
   - C9orf72 and axonal transport;
   - basal ganglia and Parkinson's disease;
   - superior colliculus escape circuit;
   - vestibular spinning/dizziness/nausea scenario.
6. Generate final Excel workbook.
7. Create the Motor output folder under the user-requested report directory when supplied; otherwise use `./SBS_Exam_Prep_Motor_Systems/`.
8. Save:
   - `Motor_Systems_Exam_Prep.xlsx`;
   - optional `Motor_Systems_Evidence_Workbook.xlsx` when evidence audit is retained separately;
   - `diagnostics/internal_processing_report.json`;
   - `diagnostics/qa_flags.json`.
9. The student-facing workbook must use one sheet named `Exam_Prep_Map`, paste original lecture slide/page images into the middle slide region, place essay-style explanation immediately to the right, and place predicted practice essay questions further right. It must not include evidence columns.

If the requested output directory does not exist, create the same folder under the current working directory and report the fallback path.
