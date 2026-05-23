#!/usr/bin/env python3
"""Lint run manifests and lineage events for reproducible Skill runs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


MANIFEST_REQUIRED = ["run_id", "created_at", "request_scope", "source_hashes", "actions", "object_store", "artifacts", "qa_summary"]
ACTION_REQUIRED = ["action_id", "action_type", "status", "inputs", "outputs"]
LINEAGE_REQUIRED = ["event_id", "run_id", "action_id", "action_type", "input_object_ids", "output_object_ids", "artifact_ids", "qa_flag_ids", "timestamp", "status"]
HELPER_PATTERNS = (
    "internal_qa",
    "ontology_objects",
    "ontology_links",
    "source_map",
    "run_manifest",
    "example_essay_manifest",
    "lineage_events",
    "lineage_report",
    "source_audit",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.strip():
            row = json.loads(line)
            row["_line_no"] = line_no
            rows.append(row)
    return rows


def lint_manifest(manifest: dict[str, Any], lineage_events: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    for key in MANIFEST_REQUIRED:
        if key not in manifest:
            failures.append({"type": "manifest_missing_required_field", "field": key})

    action_ids = set()
    for action in manifest.get("actions", []):
        for key in ACTION_REQUIRED:
            if key not in action:
                failures.append({"type": "action_missing_required_field", "action": action.get("action_id"), "field": key})
        if action.get("action_id") in action_ids:
            failures.append({"type": "duplicate_action_id", "action_id": action.get("action_id")})
        action_ids.add(action.get("action_id"))

    if not manifest.get("source_hashes"):
        failures.append({"type": "source_hashes_empty"})
    if not manifest.get("object_store"):
        failures.append({"type": "object_store_empty"})

    qa_summary = manifest.get("qa_summary", {})
    if qa_summary.get("blocking", 0):
        failures.append({"type": "manifest_has_blocking_qa", "blocking": qa_summary.get("blocking")})

    for artifact in manifest.get("artifacts", []):
        artifact_id = artifact.get("artifact_id")
        if artifact.get("student_visible"):
            if artifact.get("qa_status") != "pass":
                failures.append({"type": "student_visible_artifact_without_passed_qa", "artifact_id": artifact_id})
            path = str(artifact.get("path") or "")
            if any(pattern in path for pattern in HELPER_PATTERNS):
                failures.append({"type": "student_visible_artifact_is_helper_file", "artifact_id": artifact_id, "path": path})

    run_id = manifest.get("run_id")
    seen_events = set()
    for event in lineage_events:
        for key in LINEAGE_REQUIRED:
            if key not in event:
                failures.append({"type": "lineage_event_missing_required_field", "event": event.get("event_id"), "field": key})
        if event.get("event_id") in seen_events:
            failures.append({"type": "duplicate_lineage_event_id", "event_id": event.get("event_id")})
        seen_events.add(event.get("event_id"))
        if event.get("run_id") != run_id:
            failures.append({"type": "lineage_run_id_mismatch", "event_id": event.get("event_id"), "run_id": event.get("run_id")})
        if event.get("action_id") not in action_ids:
            failures.append({"type": "lineage_action_missing_from_manifest", "event_id": event.get("event_id"), "action_id": event.get("action_id")})

    publish_actions = [action for action in manifest.get("actions", []) if action.get("action_type") == "ApproveStudentOutput" and action.get("status") == "pass"]
    if publish_actions and not lineage_events:
        failures.append({"type": "publish_action_without_lineage"})

    return {
        "pass": not failures,
        "counts": {
            "actions": len(manifest.get("actions", [])),
            "artifacts": len(manifest.get("artifacts", [])),
            "lineage_events": len(lineage_events),
        },
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--lineage-events", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = lint_manifest(load_json(args.manifest), load_jsonl(args.lineage_events))
    except Exception as exc:
        result = {"pass": False, "failures": [{"type": "read_error", "error": str(exc)}]}
    text = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
