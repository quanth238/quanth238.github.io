#!/usr/bin/env python3
"""Run a blog example script inside a remote WSL environment and import results."""

from __future__ import annotations

import argparse
import base64
import io
import json
import re
import shutil
import subprocess
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FIGURE_EXTENSIONS = {".svg", ".png", ".jpg", ".jpeg", ".webp"}


def validate_slug(slug: str) -> None:
    if not SLUG_RE.fullmatch(slug):
        raise ValueError("slug must use lowercase letters, digits, and single hyphens")


def shell_quote(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


def run_wsl_script(ssh_target: str, distro: str, script: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "ssh",
            "-o",
            "BatchMode=yes",
            ssh_target,
            "wsl.exe",
            "--distribution",
            distro,
            "--",
            "bash",
            "-s",
        ],
        input=script,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def decode_tarball(encoded: str, destination: Path) -> None:
    data = base64.b64decode(encoded.encode("ascii"))
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
        for member in tar.getmembers():
            target = (destination / member.name).resolve()
            if not str(target).startswith(str(destination.resolve())):
                raise ValueError(f"unsafe tar member: {member.name}")
        tar.extractall(destination)


def copy_figures(run_dir: Path, asset_dir: Path) -> list[Path]:
    asset_dir.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    for path in sorted(run_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in FIGURE_EXTENSIONS:
            continue
        target = asset_dir / path.name
        shutil.copy2(path, target)
        copied.append(target)
    return copied


def metadata_content(args: argparse.Namespace, run_id: str, remote_dir: str, copied: list[Path]) -> str:
    rel_assets = [str(path.relative_to(ROOT)) for path in copied]
    payload = {
        "slug": args.slug,
        "run_id": run_id,
        "ssh": args.ssh,
        "wsl_distro": args.wsl_distro,
        "remote_dir": remote_dir,
        "script": str(Path(args.script).resolve()),
        "copied_assets": rel_assets,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    return json.dumps(payload, indent=2) + "\n"


def remote_run_script(args: argparse.Namespace, run_id: str, script_b64: str, requirements_b64: str | None) -> tuple[str, str]:
    remote_dir = f"cv_blog_runs/{args.slug}/{run_id}"
    env_dir = f"cv_blog_envs/{args.slug}"
    script_name = Path(args.script).name
    req_block = ""
    if requirements_b64:
        req_block = f"""
base64 -d > "$RUN_DIR/requirements.txt" <<'REQ_B64'
{requirements_b64}
REQ_B64
python3 -m venv "$ENV_DIR"
"$ENV_DIR/bin/python" -m pip install --upgrade pip
"$ENV_DIR/bin/python" -m pip install -r "$RUN_DIR/requirements.txt"
PYTHON_BIN="$ENV_DIR/bin/python"
"""
    return (
        f"""\
set -u
RUN_DIR="$HOME/{remote_dir}"
ENV_DIR="$HOME/{env_dir}"
SCRIPT_NAME={shell_quote(script_name)}
mkdir -p "$RUN_DIR"
base64 -d > "$RUN_DIR/$SCRIPT_NAME" <<'SCRIPT_B64'
{script_b64}
SCRIPT_B64
PYTHON_BIN=python3
{req_block}
cd "$RUN_DIR"
STARTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
set +e
"$PYTHON_BIN" "$SCRIPT_NAME" > stdout.txt 2> stderr.txt
STATUS=$?
set -e
FINISHED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
cat > run_metadata.json <<EOF
{{
  "slug": "{args.slug}",
  "run_id": "{run_id}",
  "script": "$SCRIPT_NAME",
  "status": $STATUS,
  "started_at": "$STARTED_AT",
  "finished_at": "$FINISHED_AT",
  "python": "$("$PYTHON_BIN" --version 2>&1)"
}}
EOF
exit 0
""",
        remote_dir,
    )


def remote_fetch_script(remote_dir: str) -> str:
    return f"""\
set -euo pipefail
cd "$HOME/{remote_dir}"
tar -czf - . | base64 -w0
"""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", required=True, help="Series slug, e.g. flow-matching-guide")
    parser.add_argument("--script", required=True, help="Local Python example script to run remotely")
    parser.add_argument("--ssh", default="Admin@desktop-a4ko83o.tail7cb6d9.ts.net", help="SSH target")
    parser.add_argument("--wsl-distro", default="Ubuntu-24.04", help="WSL distro name")
    parser.add_argument("--requirements", help="Optional pip requirements file for a remote venv")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        validate_slug(args.slug)
        script_path = Path(args.script)
        if not script_path.is_absolute():
            script_path = ROOT / script_path
        if not script_path.exists():
            raise ValueError(f"script not found: {script_path}")

        requirements_b64 = None
        if args.requirements:
            requirements_path = Path(args.requirements)
            if not requirements_path.is_absolute():
                requirements_path = ROOT / requirements_path
            if not requirements_path.exists():
                raise ValueError(f"requirements file not found: {requirements_path}")
            requirements_b64 = base64.b64encode(requirements_path.read_bytes()).decode("ascii")

        run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        script_b64 = base64.b64encode(script_path.read_bytes()).decode("ascii")
        run_script, remote_dir = remote_run_script(args, run_id, script_b64, requirements_b64)
        run_result = run_wsl_script(args.ssh, args.wsl_distro, run_script)
        if run_result.returncode != 0:
            print(run_result.stderr, file=sys.stderr)
            return run_result.returncode

        fetch_result = run_wsl_script(args.ssh, args.wsl_distro, remote_fetch_script(remote_dir))
        if fetch_result.returncode != 0:
            print(fetch_result.stderr, file=sys.stderr)
            return fetch_result.returncode

        local_run_dir = ROOT / "_blog_work" / args.slug / "remote_runs" / run_id
        decode_tarball(fetch_result.stdout.strip(), local_run_dir)
        asset_dir = ROOT / "assets" / "img" / "blog" / args.slug
        copied = copy_figures(local_run_dir, asset_dir)
        (local_run_dir / "local_import_metadata.json").write_text(
            metadata_content(args, run_id, remote_dir, copied),
            encoding="utf-8",
        )
    except ValueError as exc:
        print(f"run_remote_example: {exc}", file=sys.stderr)
        return 1

    for path in copied:
        print(f"Imported {path.relative_to(ROOT)}")
    print(f"Saved remote logs in {local_run_dir.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
