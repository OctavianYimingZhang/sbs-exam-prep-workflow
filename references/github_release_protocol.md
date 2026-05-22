# GitHub Release Protocol

Use this protocol before committing and pushing Skill updates.

## Pre-Push Checklist

1. Run compile checks for all scripts.
2. Run workbook prose fixture lint.
3. Run benchmark metadata/regression checks.
4. Generate the positive Example Essay DOCX fixture in strict mode.
5. Lint the generated DOCX formatting and source mapping.
6. Run the Example Essay language linter.
7. Run the no-identity-trigger linter.
8. Run the public safety scan for private absolute paths and institutional-private markers.
9. Confirm the installed Skill copy matches the repository copy.
10. Confirm `git status --short` contains only intentional changes.

## Identity Trigger Rule

Production files must not branch on course names, benchmark names, or private folder identities.

Allowed:

- generic course-code regex;
- target-group fields;
- benchmark fixture data under `benchmarks/`;
- tests under `tests/`.

Forbidden:

- course-name alias tables;
- hardcoded benchmark names in production routing;
- file names from private source folders as production triggers.

## Push Rule

Commit only after local GitHub-ready checks pass. Push only the repository changes, not generated temporary artefacts or private source material.
