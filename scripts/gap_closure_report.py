#!/usr/bin/env python3
"""Aggregate QA outputs into a gap-closure report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def status_from_payload(payload: dict[str, Any]) -> bool:
    if "pass" in payload:
        return bool(payload["pass"])
    status = str(payload.get("status", "")).lower()
    return status == "pass" or status == "ok"


def gap_for_check(name: str, payload: dict[str, Any], path: Path) -> dict[str, str]:
    reasons = payload.get("fail_reasons") or payload.get("qa_flags") or payload.get("global_failures") or payload.get("failures") or []
    return {
        "id": f"{name}_failed",
        "description": f"{name} did not pass.",
        "evidence": f"{path}: {json.dumps(reasons, ensure_ascii=False)[:500]}",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a gap-closure report from check JSON files.")
    parser.add_argument("--check", action="append", default=[], help="NAME=PATH JSON check output.")
    parser.add_argument("--external-review-unavailable", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    checks = []
    high_gaps = []
    medium_gaps = []
    low_gaps = []

    for item in args.check:
        if "=" not in item:
            medium_gaps.append({"id": "malformed_check_argument", "description": "Check argument must be NAME=PATH.", "evidence": item})
            continue
        name, raw_path = item.split("=", 1)
        path = Path(raw_path)
        try:
            payload = load_json(path)
            passed = status_from_payload(payload)
        except Exception as exc:
            payload = {"error": str(exc)}
            passed = False
        checks.append({"name": name, "status": "pass" if passed else "fail", "evidence": str(path), "command": ""})
        if not passed:
            severity = "high" if name in {"identity_trigger", "public_safety", "docx_source", "github_ready"} else "medium"
            gap = gap_for_check(name, payload, path)
            if severity == "high":
                high_gaps.append(gap)
            else:
                medium_gaps.append(gap)

    if args.external_review_unavailable:
        low_gaps.append(
            {
                "id": "external_review_unavailable",
                "description": "External ChatGPT/Chrome review artefact was not available for import.",
                "evidence": "Local protocol and script checks were used instead.",
            }
        )

    next_actions = []
    if high_gaps:
        next_actions.append("Fix high-severity gates before commit or push.")
    if medium_gaps:
        next_actions.append("Close medium gaps and rerun the gap loop.")
    if not high_gaps and not medium_gaps:
        next_actions.append("No high or medium gaps remain; run GitHub-ready check before push.")

    result = {
        "status": "pass" if not high_gaps and not medium_gaps else "fail",
        "high_gaps": high_gaps,
        "medium_gaps": medium_gaps,
        "low_gaps": low_gaps,
        "checks": checks,
        "next_actions": next_actions,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"status": result["status"], "output": str(args.output), "high": len(high_gaps), "medium": len(medium_gaps), "low": len(low_gaps)}, indent=2))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
