#!/usr/bin/env python3
"""Validate user-interaction mode, coverage, and blocker contract text."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_MODES = {
    "full_workflow",
    "source_inventory",
    "exam_format_diagnosis",
    "prediction_workbook",
    "mcq_prep",
    "short_answer_prep",
    "practical_data_prep",
    "long_answer_plan",
    "essay_theme_plan",
    "example_essay_docx",
    "evidence_gap_audit",
    "incremental_refresh",
}

REQUIRED_OBJECTS = {
    "UserExamPrepRequest",
    "UserConstraint",
    "SourceCoverageMap",
    "GateResult",
    "OutputView",
}

REQUIRED_ACTIONS = {
    "ParseUserExamPrepRequest",
    "BuildSourceCoverageMap",
    "SelectOutputView",
    "RecordGateResult",
}

REQUIRED_TEXT = {
    "Source Coverage Card": "source coverage card",
    "Best Source Pack": "best source pack",
    "one clarification question": "one clarification question",
    "blocked conclusions": "blocked conclusions",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(root: Path) -> dict:
    failures: list[dict] = []
    ontology = load_json(root / "ontology/ontology.json")
    object_types = set(ontology.get("object_types", {}))
    action_types = set(ontology.get("action_types", {}))
    missing_objects = sorted(REQUIRED_OBJECTS - object_types)
    if missing_objects:
        failures.append({"type": "missing_interaction_objects", "items": missing_objects})
    missing_actions = sorted(REQUIRED_ACTIONS - action_types)
    if missing_actions:
        failures.append({"type": "missing_interaction_actions", "items": missing_actions})

    protocol_path = root / "references/user_interaction_protocol.md"
    if not protocol_path.exists():
        failures.append({"type": "missing_user_interaction_protocol"})
        protocol_text = ""
    else:
        protocol_text = protocol_path.read_text(encoding="utf-8").lower()

    skill_text = (root / "SKILL.md").read_text(encoding="utf-8").lower()
    readme_text = (root / "README.md").read_text(encoding="utf-8").lower()
    combined = "\n".join([protocol_text, skill_text, readme_text])

    missing_modes = sorted(mode for mode in REQUIRED_MODES if mode not in combined)
    if missing_modes:
        failures.append({"type": "missing_modes", "items": missing_modes})
    for label, needle in REQUIRED_TEXT.items():
        if needle not in combined:
            failures.append({"type": "missing_interaction_text", "label": label, "needle": needle})

    schema_dir = root / "schemas"
    for object_name in REQUIRED_OBJECTS:
        snake = []
        for char in object_name:
            if char.isupper() and snake:
                snake.append("_")
            snake.append(char.lower())
        schema = schema_dir / ("".join(snake) + ".schema.json")
        if not schema.exists():
            failures.append({"type": "missing_interaction_schema", "object_type": object_name, "path": str(schema)})

    return {
        "pass": not failures,
        "counts": {
            "required_modes": len(REQUIRED_MODES),
            "required_objects": len(REQUIRED_OBJECTS),
            "required_actions": len(REQUIRED_ACTIONS),
        },
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = validate(args.root)
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
