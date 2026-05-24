# Legacy Excel Compatibility Protocol

This file is retained only for migration checks, internal QA, and backwards-compatible lint fixtures. It does not define an ordinary student-facing output route.

Current public exam-prep outputs are Word-first:

- `Lecture_Knowledge_Walkthrough.docx`;
- `MCQ_Exam_Analysis_Report.docx`;
- `ShortAnswer_Exam_Analysis_Report.docx`;
- `LongAnswer_Project_Scenario_Report.docx`;
- `Essay_Module_Example_Essays.docx`.

Do not generate Excel workbooks, prediction workbooks, confidence-band files, archetype-registry files, or essay-theme-plan-only files as ordinary student-facing outputs.

If a legacy workbook is explicitly requested for audit or migration, keep it outside the public student-output folder unless the user asks for an audit package. It must not contain unsupported claims, hidden-source inference, benchmark-specific content, or complete essays stored only in spreadsheet cells.

Legacy audit labels may include:

- Essay / Problem-Essay: `Predicted Essay Theme / Scope / Practice Angle`
- Short Answer: `Likely Short-Answer Form / Mark-Producing Answer Schema`
- MCQ: `Likely Statement Trap / Discriminator / One-line Rule`
- Problem/Data: `Likely Data-Problem Archetype / Graph-Reading Operation / Mechanism Inference`
- Long-Answer Project: `Likely Project Operation / Method-Readout-Interpretation / Control`

These labels are audit labels, not public route names. For current output generation, convert the same analysis into the matching DOCX add-on report.
