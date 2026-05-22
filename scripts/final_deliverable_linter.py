#!/usr/bin/env python3
"""Check a public output directory does not contain internal helper artefacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


HELPER_NAMES = {
    "example_essay_manifest.json",
    "example_essay_source_audit.json",
    "citation_candidates.json",
    "citation_resolution_log.json",
    "citation_source_notes.json",
    "classic_experiment_search_plan.json",
    "source_scan.json",
    "target_groups.json",
}
HELPER_SUFFIXES = ("_source_map.json", "_qa.json", "_render_qa.json")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate that public output folders exclude internal helper artefacts.")
    parser.add_argument("path", type=Path)
    parser.add_argument("--allowed", help="Optional comma-separated extension allow-list for stricter checks.")
    args = parser.parse_args()

    allowed = {item.strip().lower() for item in args.allowed.split(",") if item.strip()} if args.allowed else None
    failures = []
    files = sorted(item for item in args.path.rglob("*") if item.is_file())
    if not files:
        failures.append({"type": "no_deliverable_files", "path": str(args.path)})
    for item in files:
        name = item.name
        if name in HELPER_NAMES or any(name.endswith(suffix) for suffix in HELPER_SUFFIXES):
            failures.append({"type": "helper_artifact_in_public_output", "path": str(item)})
        elif allowed and item.suffix.lower() not in allowed:
            failures.append({"type": "non_deliverable_file", "path": str(item), "suffix": item.suffix})
    result = {
        "pass": not failures,
        "allowed_extensions": sorted(allowed) if allowed else None,
        "file_count": len(files),
        "failures": failures,
    }
    print(json.dumps(result, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
