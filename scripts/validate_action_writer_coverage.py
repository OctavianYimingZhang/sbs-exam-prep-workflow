#!/usr/bin/env python3
"""Validate that ontology objects have writer actions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(path: Path) -> dict[str, Any]:
    data = load_json(path)
    object_types = set(data.get("object_types", {}))
    link_types = set(data.get("link_types", {}))
    action_types = data.get("action_types", {})
    failures: list[dict[str, Any]] = []
    writers: dict[str, list[str]] = {name: [] for name in object_types}

    for action_name, outputs in action_types.items():
        if not isinstance(outputs, list) or not outputs:
            failures.append({"type": "action_missing_outputs", "action_type": action_name})
            continue
        for output in outputs:
            if output in object_types:
                writers[output].append(action_name)
            elif output in link_types:
                continue
            else:
                failures.append({"type": "action_writes_unknown_type", "action_type": action_name, "output": output})

    missing = sorted(name for name, actions in writers.items() if not actions)
    if missing:
        failures.append({"type": "object_without_writer_action", "items": missing})

    return {
        "pass": not failures,
        "counts": {
            "object_types": len(object_types),
            "action_types": len(action_types),
            "objects_with_writers": sum(1 for actions in writers.values() if actions),
        },
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ontology", type=Path, default=Path("ontology/ontology.json"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = validate(args.ontology)
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
