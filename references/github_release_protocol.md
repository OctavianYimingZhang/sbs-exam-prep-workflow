# GitHub Release Protocol

Use this protocol before committing and pushing Skill updates.

## Pre-Push Checklist

1. Run compile checks for all scripts.
2. Run the ontology contract linter.
3. Run the fragment-index fixture.
4. Run the runtime ontology validator fixture, including a negative cross-target leakage case.
5. Run the run-manifest and lineage fixture.
6. Run workbook prose fixture lint.
7. Run benchmark metadata/regression checks.
8. Generate the positive Example Essay DOCX fixture in strict mode.
9. Lint the generated DOCX formatting and source mapping.
10. Run the Example Essay language linter.
11. Run the no-identity-trigger linter.
12. Run the public safety scan for private absolute paths and institutional-private markers.
13. Confirm the installed Skill copy matches the repository copy.
14. Confirm `git status --short` contains only intentional changes.

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

## Runtime Control-Plane Rule

When a run generates public artifacts through helper scripts, the internal QA folder should be able to provide:

- `ontology_objects/*.jsonl` or equivalent object JSON;
- `ontology_links/links.jsonl`;
- `run_manifest.json`;
- `lineage_events.jsonl`.

These are helper artifacts. They should be linted before publish, but they must not be mixed into the default student-facing output folder unless the user explicitly asks for an audit package.
