#!/usr/bin/env python3
"""Create a compact run-status object from a WorkflowPlan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def build_status(plan: dict[str, Any], completed_actions: set[str] | None = None) -> dict[str, Any]:
    completed_actions = completed_actions or set()
    blocked_actions = [action["action_id"] for action in plan.get("actions", []) if action.get("skip_reason")]
    remaining = [
        action["action_id"]
        for action in plan.get("actions", [])
        if action.get("action_id") not in completed_actions and action.get("action_id") not in blocked_actions
    ]
    if blocked_actions:
        status = "blocked"
    elif remaining:
        status = "planned"
    else:
        status = "passed"
    return {
        "run_id": f"run_{plan.get('plan_id', 'unknown')}",
        "plan_id": plan.get("plan_id", "unknown"),
        "status": status,
        "current_action": remaining[0] if remaining else None,
        "completed_actions": sorted(completed_actions),
        "blocked_actions": blocked_actions,
        "artifacts": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--completed-actions", type=Path, help="Optional JSON array of completed action IDs.")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    plan = load_json(args.plan)
    completed = set(load_json(args.completed_actions)) if args.completed_actions else set()
    status = build_status(plan, completed)
    text = json.dumps(status, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
