# Gap Closure Loop Protocol

The Skill is not complete after one rewrite. It is complete when the example-analysis and QA loop no longer finds high or medium gaps.

## Loop

```text
collect examples
-> classify source roles
-> extract ExampleContribution and LanguageDelta records
-> update protocols/scripts
-> generate or lint representative outputs
-> import external review notes when available
-> produce gap report
-> repeat until high/medium gaps are closed
```

## Gap Severity

High:

- unsupported factual claims can reach a student-facing answer;
- live-assessment or contract-cheating boundary is unclear;
- course/benchmark identity can trigger production behaviour;
- formal past papers and examples are pooled incorrectly;
- Example Essay DOCX fails required formatting or source-grounding rules.

Medium:

- answer keys lack provenance separation;
- practical/data/problem papers do not get a question-type-specific prep strategy;
- language contract violations persist in generated prose;
- legacy or spreadsheet inputs are ignored without a clear QA flag;
- external review recommendations are not converted into validation checks.

Low:

- naming, documentation, or CLI ergonomics issues that do not change output correctness.

## Completion Condition

The loop can stop only when:

- `gap_report` has no high gaps;
- `gap_report` has no medium gaps unless explicitly accepted with rationale;
- `github_ready_check.py --ci` passes;
- installed Skill copy matches the repository copy;
- Git working tree contains only intentional changes ready for commit.

## External Review

Chrome ChatGPT Pro/Extended review, if available, is an external review artefact. It is not a runtime dependency.

If external review is unavailable, record that fact and continue with local evidence, local examples, and automated checks.
