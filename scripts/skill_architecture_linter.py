#!/usr/bin/env python3
"""Validate the Skill architecture, improvement ledger and structural gates."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "SKILL.md",
    "skill_manifest.json",
    "references/skill_architecture_protocol.md",
    "references/protected_source_coverage_protocol.md",
    "references/knowledge_surface_protocol.md",
    "references/scientific_precision_protocol.md",
    "schemas/analysis_context.schema.json",
    "schemas/unit_example_contribution.schema.json",
    "schemas/knowledge_surface_contract.schema.json",
    "governance/skill_improvement_ledger.json",
    "scripts/zero_mention_lint.py",
    "scripts/knowledge_surface_linter.py",
    "scripts/scientific_precision_linter.py",
    "scripts/skill_architecture_linter.py",
]

REQUIRED_ARCHITECTURE_TERMS = [
    "AnalysisContext",
    "UnitExampleContribution",
    "SlideAtomicLedger",
    "PastPaperTermMustAppear",
    "SourceToOutputBinding",
    "ZeroMentionLint",
    "KnowledgeSurfaceContract",
    "EssayAdaptiveBudget",
    "ScientificPrecisionGate",
    "ImprovementImplementationLedger",
]

REQUIRED_HEALTH_COMMANDS = [
    "python3 scripts/skill_architecture_linter.py --self-test",
    "python3 scripts/zero_mention_lint.py --self-test",
    "python3 scripts/knowledge_surface_linter.py --self-test",
    "python3 scripts/scientific_precision_linter.py --self-test",
]

VALID_LEDGER_STATUS = {"implemented", "implemented_with_gap", "deferred", "replaced_by_later_rule"}
REQUIRED_LEDGER_FIELDS = {
    "improvement_id",
    "source_summary",
    "user_purpose",
    "architectural_layer",
    "implemented_files",
    "validation_gates",
    "status",
    "remaining_gaps",
    "next_action",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def script_path_from_command(command: str) -> str | None:
    match = re.match(r"\s*python3\s+(scripts/[^\s]+\.py)\b", command)
    if match:
        return match.group(1)
    return None


def validate_required_files(root: Path) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for rel_path in REQUIRED_FILES:
        if not (root / rel_path).exists():
            failures.append({"type": "missing_required_architecture_file", "path": rel_path})
    return failures


def validate_terms(root: Path) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    combined_paths = [
        "SKILL.md",
        "references/skill_architecture_protocol.md",
        "references/protected_source_coverage_protocol.md",
        "references/knowledge_surface_protocol.md",
        "references/scientific_precision_protocol.md",
    ]
    combined = "\n".join(read_text(root / rel_path) for rel_path in combined_paths if (root / rel_path).exists())
    for term in REQUIRED_ARCHITECTURE_TERMS:
        if term not in combined:
            failures.append({"type": "missing_architecture_term", "term": term})
    return failures


def validate_manifest(root: Path) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    manifest_path = root / "skill_manifest.json"
    if not manifest_path.exists():
        return [{"type": "missing_manifest"}]
    try:
        manifest = load_json(manifest_path)
    except Exception as exc:
        return [{"type": "manifest_json_error", "error": str(exc)}]
    commands = set(manifest.get("health_commands", []))
    for command in REQUIRED_HEALTH_COMMANDS:
        if command not in commands:
            failures.append({"type": "manifest_missing_health_command", "command": command})
    for command in manifest.get("health_commands", []):
        script_path = script_path_from_command(str(command))
        if script_path and not (root / script_path).exists():
            failures.append({"type": "manifest_command_missing_script", "command": command, "script": script_path})
    return failures


def validate_ledger(root: Path) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    ledger_path = root / "governance/skill_improvement_ledger.json"
    if not ledger_path.exists():
        return [{"type": "missing_improvement_ledger"}]
    try:
        ledger = load_json(ledger_path)
    except Exception as exc:
        return [{"type": "ledger_json_error", "error": str(exc)}]
    records = ledger.get("records")
    if not isinstance(records, list) or not records:
        failures.append({"type": "ledger_missing_records"})
        return failures
    seen: set[str] = set()
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            failures.append({"type": "ledger_record_not_object", "index": index})
            continue
        missing = sorted(REQUIRED_LEDGER_FIELDS - set(record))
        if missing:
            failures.append({"type": "ledger_record_missing_fields", "index": index, "fields": missing})
        improvement_id = str(record.get("improvement_id") or f"record_{index}")
        if improvement_id in seen:
            failures.append({"type": "duplicate_improvement_id", "improvement_id": improvement_id})
        seen.add(improvement_id)
        status = record.get("status")
        if status not in VALID_LEDGER_STATUS:
            failures.append({"type": "bad_ledger_status", "improvement_id": improvement_id, "status": status})
        files = record.get("implemented_files") or []
        if status in {"implemented", "implemented_with_gap"} and not files:
            failures.append({"type": "implemented_record_missing_files", "improvement_id": improvement_id})
        for rel_path in files:
            if not (root / str(rel_path)).exists():
                failures.append({"type": "ledger_implemented_file_missing", "improvement_id": improvement_id, "path": rel_path})
        gates = record.get("validation_gates") or []
        if status in {"implemented", "implemented_with_gap"} and not gates:
            failures.append({"type": "implemented_record_missing_validation_gate", "improvement_id": improvement_id})
        for command in gates:
            script_path = script_path_from_command(str(command))
            if script_path and not (root / script_path).exists():
                failures.append({"type": "ledger_gate_missing_script", "improvement_id": improvement_id, "command": command})
        gaps = record.get("remaining_gaps") or []
        if status == "implemented" and gaps:
            failures.append({"type": "implemented_record_has_remaining_gaps", "improvement_id": improvement_id, "remaining_gaps": gaps})
        if status == "implemented_with_gap" and not gaps:
            failures.append({"type": "gap_status_without_gap", "improvement_id": improvement_id})
    return failures


def validate(root: Path) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    failures.extend(validate_required_files(root))
    failures.extend(validate_terms(root))
    failures.extend(validate_manifest(root))
    failures.extend(validate_ledger(root))
    return {
        "status": "pass" if not failures else "fail",
        "counts": {
            "required_files": len(REQUIRED_FILES),
            "required_terms": len(REQUIRED_ARCHITECTURE_TERMS),
            "required_health_commands": len(REQUIRED_HEALTH_COMMANDS),
        },
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--self-test", action="store_true", help="Validate the current repository architecture.")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = validate(args.root)
    text = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0 if result.get("status") == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
