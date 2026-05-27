#!/usr/bin/env python3
"""Report whether a SkillConfig has the source classes required by its preset."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from plan_workflow import PRESET_REQUIRED_CLASSES, available_source_classes, blocker_for_missing, load_json, missing_required_classes, normalize_preset


def build_report(config: dict[str, Any], source_scan: dict[str, Any] | None = None) -> dict[str, Any]:
    output_mode = config.get("output_mode", {})
    selected_preset = normalize_preset(str(output_mode.get("preset") or "exam_prep_notes_docx"))
    required = PRESET_REQUIRED_CLASSES[selected_preset]
    available = available_source_classes(config, source_scan)
    missing = missing_required_classes(required, available)
    blockers = [blocker_for_missing(index, item, selected_preset) for index, item in enumerate(missing, start=1)]
    warnings: list[dict[str, Any]] = []

    source_inputs = config.get("source_inputs", {})
    source_policy = config.get("source_policy", {})
    if not source_inputs.get("extra_reading_books_or_papers") and source_policy.get("allow_online_academic_search"):
        warnings.append(
            {
                "warning_id": "warn_online_reading_needed",
                "severity": "info",
                "message": "No supplied extra reading was listed; online academic search may be needed only for directly relevant enrichment.",
            }
        )
    if source_inputs.get("exemplars_or_feedback") and not source_policy.get("treat_examples_as_style_only", True):
        warnings.append(
            {
                "warning_id": "warn_example_policy",
                "severity": "warning",
                "message": "Examples or feedback should be style/workflow evidence only unless independently verified from target sources.",
            }
        )

    project = config.get("project", {})
    return {
        "report_id": f"input_readiness_{selected_preset}",
        "selected_preset": selected_preset,
        "target_group_key": str(project.get("target_group_key") or "unspecified_target"),
        "required_source_classes": required,
        "available_source_classes": sorted(available),
        "missing_required": missing,
        "blockers": blockers,
        "warnings": warnings,
        "can_run": not blockers,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--source-scan", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fail-on-blockers", action="store_true")
    args = parser.parse_args()

    try:
        config = load_json(args.config)
        source_scan = load_json(args.source_scan) if args.source_scan else None
        report = build_report(config, source_scan)
    except Exception as exc:
        print(json.dumps({"status": "fail", "error": str(exc)}, indent=2), file=sys.stderr)
        return 1

    text = json.dumps(report, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    if args.fail_on_blockers and report["blockers"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
