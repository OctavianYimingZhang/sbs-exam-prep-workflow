#!/usr/bin/env python3
"""Skill self-check and explicit safe-update helper."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
import time
import zipfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "skill_manifest.json"


def run(command: str | list[str], *, check: bool = False, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    args = shlex.split(command) if isinstance(command, str) else command
    proc = subprocess.run(args, cwd=str(cwd), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and proc.returncode != 0:
        display = command if isinstance(command, str) else " ".join(command)
        raise RuntimeError(
            f"Command failed: {display}\n"
            f"exit={proc.returncode}\n"
            f"stdout={proc.stdout}\n"
            f"stderr={proc.stderr}"
        )
    return proc


def git(args: list[str], *, check: bool = True) -> str:
    return run(["git", *args], check=check).stdout.strip()


def load_manifest() -> dict[str, Any]:
    if not MANIFEST_PATH.exists():
        raise SystemExit(f"Missing manifest: {MANIFEST_PATH}")
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    required = ["schema_version", "skill_id", "repo", "branch", "entrypoint", "health_commands"]
    missing = [key for key in required if key not in data]
    if missing:
        raise SystemExit(f"Manifest missing fields: {', '.join(missing)}")
    entrypoint = ROOT / str(data["entrypoint"])
    if not entrypoint.exists():
        raise SystemExit(f"Missing Skill entrypoint: {entrypoint}")
    if not isinstance(data.get("health_commands"), list):
        raise SystemExit("Manifest field health_commands must be a list.")
    return data


def has_git() -> bool:
    return run(["git", "rev-parse", "--is-inside-work-tree"]).returncode == 0


def dirty_files() -> list[str]:
    proc = run(["git", "status", "--porcelain"])
    return [line for line in proc.stdout.splitlines() if line.strip()]


def sync_status(branch: str, *, fetch: bool = True) -> dict[str, Any]:
    if fetch:
        run(["git", "fetch", "--quiet", "origin", branch], check=True)
    remote_ref = f"origin/{branch}"
    local = git(["rev-parse", "HEAD"])
    remote = git(["rev-parse", remote_ref])
    base = git(["merge-base", "HEAD", remote_ref])
    if local == remote:
        state = "up_to_date"
    elif base == local:
        state = "behind"
    elif base == remote:
        state = "ahead"
    else:
        state = "diverged"
    if state == "up_to_date":
        incoming_range = None
        outgoing_range = None
    elif state == "behind":
        incoming_range = f"HEAD..{remote_ref}"
        outgoing_range = None
    elif state == "ahead":
        incoming_range = None
        outgoing_range = f"{remote_ref}..HEAD"
    else:
        incoming_range = f"{base}..{remote_ref}"
        outgoing_range = f"{base}..HEAD"
    incoming_changes_proc = run(["git", "diff", "--name-status", incoming_range]) if incoming_range else None
    outgoing_changes_proc = run(["git", "diff", "--name-status", outgoing_range]) if outgoing_range else None
    log_proc = run(["git", "log", "--oneline", incoming_range]) if incoming_range else None
    outgoing_log_proc = run(["git", "log", "--oneline", outgoing_range]) if outgoing_range else None
    incoming_changed_files = [line for line in incoming_changes_proc.stdout.splitlines() if line.strip()] if incoming_changes_proc else []
    outgoing_changed_files = [line for line in outgoing_changes_proc.stdout.splitlines() if line.strip()] if outgoing_changes_proc else []
    if state == "ahead":
        changed_files = outgoing_changed_files
        change_direction = "outgoing"
    else:
        changed_files = incoming_changed_files
        change_direction = "incoming"
    return {
        "state": state,
        "local": local,
        "remote": remote,
        "remote_ref": remote_ref,
        "change_direction": change_direction,
        "changed_files": changed_files,
        "incoming_changed_files": incoming_changed_files,
        "outgoing_changed_files": outgoing_changed_files,
        "incoming_commits": [line for line in log_proc.stdout.splitlines() if line.strip()] if log_proc else [],
        "outgoing_commits": [line for line in outgoing_log_proc.stdout.splitlines() if line.strip()] if outgoing_log_proc else [],
    }


def run_health(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    results = []
    for command in manifest.get("health_commands", []):
        proc = run(str(command))
        results.append(
            {
                "cmd": command,
                "ok": proc.returncode == 0,
                "exit_code": proc.returncode,
                "stdout_tail": proc.stdout[-4000:],
                "stderr_tail": proc.stderr[-4000:],
            }
        )
    return results


def make_backup(skill_id: str, old_sha: str) -> Path:
    backup_dir = ROOT / ".skill_backups"
    backup_dir.mkdir(exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    target = backup_dir / f"{skill_id}-{old_sha[:12]}-{stamp}.zip"
    excluded = {".git", ".venv", "__pycache__", ".pytest_cache", ".mypy_cache", ".skill_backups"}
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in ROOT.rglob("*"):
            if any(part in excluded for part in path.parts):
                continue
            if path.is_file():
                zf.write(path, path.relative_to(ROOT))
    return target


def print_result(data: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    print(f"skill: {data.get('skill_id')}")
    print(f"git: {data.get('git')}")
    sync = data.get("sync", {})
    print(f"sync: {sync.get('state')}")
    dirty = data.get("dirty_files", [])
    if dirty:
        print("\ndirty files:")
        for line in dirty[:50]:
            print(f" {line}")
    incoming = sync.get("incoming_commits", [])
    if incoming:
        print("\nincoming commits:")
        for line in incoming[:20]:
            print(f" {line}")
    changed = sync.get("changed_files", [])
    if changed:
        direction = sync.get("change_direction", "changed")
        print(f"\nchanged files ({direction}):")
        for line in changed[:50]:
            print(f" {line}")
    health = data.get("health", [])
    if health:
        print("\nhealth:")
        for item in health:
            mark = "PASS" if item["ok"] else "FAIL"
            print(f" [{mark}] {item['cmd']}")


def cmd_doctor(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    result: dict[str, Any] = {
        "skill_id": manifest["skill_id"],
        "root": str(ROOT),
        "manifest": str(MANIFEST_PATH),
        "git": "present" if has_git() else "missing",
    }
    if has_git():
        result["dirty_files"] = dirty_files()
        try:
            result["sync"] = sync_status(manifest["branch"], fetch=not args.offline)
        except Exception as exc:
            result["sync"] = {"state": "unknown", "error": str(exc)}
    else:
        result["sync"] = {
            "state": "no_git_metadata",
            "message": "This installed Skill is not a git checkout. Use a git-based install for self-update.",
        }
    result["health"] = [] if args.skip_health else run_health(manifest)
    print_result(result, args.json)
    failed_health = any(not item["ok"] for item in result["health"])
    return 1 if failed_health else 0


def cmd_update(args: argparse.Namespace) -> int:
    if args.dry_run and args.yes:
        raise SystemExit("Choose either --dry-run or --yes, not both.")
    manifest = load_manifest()
    if not has_git():
        raise SystemExit("Cannot update: this Skill directory has no .git metadata.")
    dirty = dirty_files()
    status = sync_status(manifest["branch"], fetch=True)
    base_result = {"skill_id": manifest["skill_id"], "git": "present", "sync": status, "dirty_files": dirty}
    if status["state"] == "up_to_date":
        print_result({**base_result, "updated": False, "dry_run": bool(args.dry_run)}, args.json)
        return 0
    if args.dry_run:
        print_result({**base_result, "dry_run": True}, args.json)
        return 0
    if status["state"] != "behind":
        raise SystemExit(f"Cannot fast-forward safely: local state is {status['state']}.")
    if dirty:
        raise SystemExit("Cannot update: working tree is dirty. Commit, stash, or discard local changes first.\n" + "\n".join(dirty))
    if not args.yes:
        raise SystemExit("Refusing to update without --yes. Run --dry-run first, then update with --yes.")

    old_sha = git(["rev-parse", "HEAD"])
    backup = make_backup(str(manifest["skill_id"]), old_sha)
    try:
        run(["git", "merge", "--ff-only", status["remote_ref"]], check=True)
        for command in manifest.get("post_update_commands", []):
            run(str(command), check=True)
        health = run_health(manifest)
        failed = [item for item in health if not item["ok"]]
        if failed:
            raise RuntimeError("Health check failed after update.")
        print_result(
            {
                "skill_id": manifest["skill_id"],
                "updated": True,
                "from": old_sha,
                "to": git(["rev-parse", "HEAD"]),
                "backup": str(backup),
                "health": health,
            },
            args.json,
        )
        return 0
    except Exception as exc:
        run(["git", "reset", "--hard", old_sha])
        raise SystemExit(f"Update failed and code was reset to {old_sha}.\nBackup: {backup}\nError: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="Inspect git status, remote freshness, and health commands.")
    doctor.add_argument("--json", action="store_true")
    doctor.add_argument("--offline", action="store_true")
    doctor.add_argument("--skip-health", action="store_true")
    doctor.set_defaults(func=cmd_doctor)

    update = sub.add_parser("update", help="Preview or run a fast-forward update.")
    update.add_argument("--dry-run", action="store_true")
    update.add_argument("--yes", action="store_true")
    update.add_argument("--json", action="store_true")
    update.set_defaults(func=cmd_update)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
