#!/usr/bin/env python3
"""Summarize a run manifest and lineage events for audit review."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def build_report(manifest: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
    action_counts = Counter(str(event.get("action_type", "unknown")) for event in events)
    status_counts = Counter(str(event.get("status", "unknown")) for event in events)
    return {
        "run_id": manifest.get("run_id"),
        "request_scope": manifest.get("request_scope"),
        "source_count": len(manifest.get("source_hashes", {})),
        "artifact_count": len(manifest.get("artifacts", [])),
        "lineage_event_count": len(events),
        "action_counts": dict(sorted(action_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
        "qa_summary": manifest.get("qa_summary", {}),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--lineage-events", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = build_report(load_json(args.manifest), load_jsonl(args.lineage_events))
    text = json.dumps(report, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
