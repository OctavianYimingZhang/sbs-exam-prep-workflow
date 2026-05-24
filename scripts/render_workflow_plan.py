#!/usr/bin/env python3
"""Render a WorkflowPlan JSON file as a concise markdown preview."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def render_plan(plan: dict[str, Any]) -> str:
    lines = [
        f"# Workflow Plan: {plan.get('selected_preset', 'unknown')}",
        "",
        f"- Plan ID: `{plan.get('plan_id', 'unknown')}`",
        f"- Target: `{plan.get('target_group_key', 'unspecified_target')}`",
        f"- Source inventory required: `{str(plan.get('source_inventory_required')).lower()}`",
        f"- Fragment index required: `{str(plan.get('fragment_index_required')).lower()}`",
        "",
        "## Actions",
        "",
        "| Action | Module | Type | Reuse | Gate |",
        "| --- | --- | --- | --- | --- |",
    ]
    for action in plan.get("actions", []):
        gate = action.get("qa_gate", {}).get("gate_name", "")
        lines.append(
            f"| `{action.get('action_id', '')}` | `{action.get('module', '')}` | `{action.get('action_type', '')}` | `{str(action.get('can_reuse_existing')).lower()}` | `{gate}` |"
        )

    blockers = plan.get("blockers", [])
    lines.extend(["", "## Blockers", ""])
    if blockers:
        for blocker in blockers:
            lines.append(f"- `{blocker.get('missing_input')}`: {blocker.get('resolution_prompt')}")
    else:
        lines.append("- None.")

    skipped = plan.get("skipped_modules", [])
    lines.extend(["", "## Skipped Modules", ""])
    if skipped:
        for item in skipped:
            lines.append(f"- `{item.get('module')}`: {item.get('reason')}")
    else:
        lines.append("- None.")

    publish_gate = plan.get("publish_gate", {})
    lines.extend(
        [
            "",
            "## Publish Gate",
            "",
            f"- Object validation: `{str(publish_gate.get('object_validation')).lower()}`",
            f"- Lineage required: `{str(publish_gate.get('lineage_required')).lower()}`",
            f"- QA required: `{str(publish_gate.get('qa_required')).lower()}`",
            f"- Fail on blocking flags: `{str(publish_gate.get('fail_on_blocking_flags')).lower()}`",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    plan = load_json(args.plan)
    text = render_plan(plan)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
