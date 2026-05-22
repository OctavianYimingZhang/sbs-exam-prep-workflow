#!/usr/bin/env python3
"""Validate citation fallback artefacts for Example Essay mode."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Check citation fallback output.")
    parser.add_argument("--dir", type=Path, required=True)
    parser.add_argument("--require-classic-plan", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    log_path = args.dir / "citation_resolution_log.json"
    if not log_path.exists():
        failures.append("citation_resolution_log_missing")
    else:
        log = json.loads(log_path.read_text(encoding="utf-8"))
        if args.require_classic_plan and "lecture_slide_citation_absent_classic_experiment_search_required" not in log.get("qa_flags", []):
            failures.append("classic_experiment_fallback_flag_missing")

    plan_path = args.dir / "classic_experiment_search_plan.json"
    if args.require_classic_plan:
        if not plan_path.exists():
            failures.append("classic_experiment_search_plan_missing")
        else:
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            if plan.get("desired_verified_sources", 0) < 3:
                failures.append("classic_experiment_desired_count_too_low")
            if len(plan.get("academic_search_queries", [])) < 3:
                failures.append("classic_experiment_search_queries_missing")
            if len(plan.get("selection_standard", [])) < 4:
                failures.append("classic_experiment_selection_standard_missing")

    result = {"pass": not failures, "failures": failures}
    print(json.dumps(result, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
