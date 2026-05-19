#!/usr/bin/env python3
"""Validate that a CV research blog series is recoverable by a fresh agent."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - dependency is listed in requirements.txt.
    raise SystemExit("check_harness: PyYAML is required; install requirements.txt") from exc


ROOT = Path(__file__).resolve().parents[2]
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VALID_TASK_STATES = {"not_started", "active", "blocked", "passing"}
REQUIRED_ROOT_FILES = [
    "AGENTS.md",
    "codex/skills/cv-research-blogger/SKILL.md",
    "codex/skills/cv-research-blogger/visual_quality.md",
    "scripts/blog_pipeline/check_post.py",
    "scripts/blog_pipeline/check_harness.py",
    "scripts/blog_pipeline/new_series.py",
    "scripts/blog_pipeline/plan_visuals.py",
    "scripts/blog_pipeline/run_remote_example.py",
]
REQUIRED_SERIES_FILES = [
    "manifest.yml",
    "visual_sources.yml",
    "series_tasks.yml",
    "HANDOFF.md",
    "SESSION_BOOTSTRAP.md",
    "series_prompt.md",
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_yaml(path: Path, errors: list[str]) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        errors.append(f"{rel(path)} is not valid YAML: {exc}")
    except OSError as exc:
        errors.append(f"cannot read {rel(path)}: {exc}")
    return {}


def require_file(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing required file: {rel(path)}")


def require_text(path: Path, patterns: list[tuple[str, str]], errors: list[str]) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    for pattern, message in patterns:
        if not re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE):
            errors.append(f"{rel(path)}: {message}")


def local_path_exists(value: str, errors: list[str], label: str) -> None:
    if re.match(r"https?://", value):
        errors.append(f"{label} must be local, not external: {value}")
        return
    if not (ROOT / value.lstrip("/")).exists():
        errors.append(f"{label} does not exist: {value}")


def validate_manifest(slug: str, manifest: dict[str, Any], errors: list[str]) -> None:
    series = manifest.get("series") or {}
    if series.get("slug") != slug:
        errors.append("manifest.yml series.slug does not match requested slug")
    if not series.get("title"):
        errors.append("manifest.yml is missing series.title")
    if not series.get("audience"):
        errors.append("manifest.yml is missing series.audience")
    if len(manifest.get("source_materials") or []) < 1:
        errors.append("manifest.yml source_materials must include at least one source")

    harness = manifest.get("harness") or {}
    for key in ("bootstrap_contract", "task_source_of_truth", "visual_source_of_truth", "handoff"):
        value = harness.get(key)
        if not value:
            errors.append(f"manifest.yml harness.{key} is missing")
            continue
        local_path_exists(str(value), errors, f"manifest.yml harness.{key}")
    if harness.get("wip_limit") != 1:
        errors.append("manifest.yml harness.wip_limit must be 1")
    remote_runtime = harness.get("remote_runtime") or {}
    if remote_runtime.get("ssh") != "Admin@desktop-a4ko83o.tail7cb6d9.ts.net":
        errors.append("manifest.yml harness.remote_runtime.ssh must point to Admin@desktop-a4ko83o.tail7cb6d9.ts.net")
    if not remote_runtime.get("wsl_distro"):
        errors.append("manifest.yml harness.remote_runtime.wsl_distro is missing")
    if "WSL" not in str(remote_runtime.get("policy", "")):
        errors.append("manifest.yml harness.remote_runtime.policy must state the WSL runtime rule")


def validate_visual_plan(plan: dict[str, Any], errors: list[str], warnings: list[str]) -> None:
    for key in ("visual_contract", "policy", "quality_gate"):
        if key not in plan:
            errors.append(f"visual_sources.yml is missing {key}")
    policy_text = " ".join(str(value) for value in (plan.get("policy") or {}).values())
    if "copy" not in policy_text.lower() or "hotlink" not in policy_text.lower():
        errors.append("visual_sources.yml policy must forbid copying and hotlinking external figures")

    references = plan.get("references") or []
    if len(references) < 1:
        errors.append("visual_sources.yml references must include at least one source")
    for index, reference in enumerate(references, start=1):
        if not isinstance(reference, dict) or not reference.get("source") or not reference.get("idea"):
            errors.append(f"visual_sources.yml reference {index} must include source and idea")

    figure_briefs = plan.get("figure_briefs") or []
    if not figure_briefs:
        warnings.append("visual_sources.yml has no figure_briefs yet; draft/publish checks should fail until Planner adds them")
    for brief in figure_briefs:
        brief_id = brief.get("id", "<missing-id>") if isinstance(brief, dict) else "<invalid>"
        if not isinstance(brief, dict):
            errors.append("visual_sources.yml has a non-mapping figure brief")
            continue
        for key in ("id", "kind", "reader_question", "purpose", "must_show", "avoid", "cited_inspirations", "status"):
            if key not in brief or brief[key] in (None, "", []):
                errors.append(f"figure brief {brief_id} is missing {key}")
        if brief.get("status") == "redesign":
            warnings.append(f"figure brief {brief_id} is marked redesign")

    for section in ("generated_figures", "remote_code_figures"):
        for item in plan.get(section) or []:
            if not isinstance(item, dict):
                errors.append(f"visual_sources.yml {section} contains a non-mapping entry")
                continue
            path = item.get("path")
            if not path:
                errors.append(f"visual_sources.yml {section} entry is missing path")
            else:
                local_path_exists(str(path), errors, f"visual_sources.yml {section} path")
            if not item.get("alt"):
                errors.append(f"visual_sources.yml {section} entry for {path or '<missing-path>'} is missing alt text")
            if section == "generated_figures" and not item.get("prompt"):
                errors.append(f"visual_sources.yml generated figure {path or '<missing-path>'} is missing prompt")


def validate_tasks(tasks_doc: dict[str, Any], errors: list[str]) -> None:
    if tasks_doc.get("wip_limit") != 1:
        errors.append("series_tasks.yml wip_limit must be 1")
    tasks = tasks_doc.get("tasks") or []
    if not tasks:
        errors.append("series_tasks.yml must include at least one task")
        return

    active_ids: list[str] = []
    task_ids: set[str] = set()
    for task in tasks:
        if not isinstance(task, dict):
            errors.append("series_tasks.yml contains a non-mapping task")
            continue
        task_id = str(task.get("id") or "<missing-id>")
        if task_id in task_ids:
            errors.append(f"duplicate task id: {task_id}")
        task_ids.add(task_id)
        for key in ("id", "title", "behavior", "state", "verification"):
            if key not in task or task[key] in (None, "", []):
                errors.append(f"task {task_id} is missing {key}")
        state = task.get("state")
        if state not in VALID_TASK_STATES:
            errors.append(f"task {task_id} has invalid state {state!r}")
        if state == "active":
            active_ids.append(task_id)
        if state == "passing" and not task.get("evidence"):
            errors.append(f"task {task_id} is passing but has no evidence")

    if len(active_ids) > 1:
        errors.append(f"series_tasks.yml has multiple active tasks: {', '.join(active_ids)}")
    active_task = tasks_doc.get("active_task")
    if active_ids and active_task not in active_ids:
        errors.append("series_tasks.yml active_task does not match the active task")
    if not active_ids and active_task not in (None, "null"):
        errors.append("series_tasks.yml active_task is set but no task is active")


def validate_markdown_handoff(series_dir: Path, errors: list[str]) -> None:
    require_text(
        series_dir / "SESSION_BOOTSTRAP.md",
        [
            (r"Read Order", "bootstrap must include a read order"),
            (r"Cold-Start Questions", "bootstrap must include cold-start questions"),
            (r"Start Commands", "bootstrap must include start commands"),
            (r"Remote Runtime", "bootstrap must include remote runtime rules"),
            (r"Admin@desktop-a4ko83o\.tail7cb6d9\.ts\.net", "bootstrap must name the WSL SSH target"),
            (r"Task Rules", "bootstrap must include task rules"),
            (r"Clean Exit", "bootstrap must include clean exit rules"),
        ],
        errors,
    )
    require_text(
        series_dir / "HANDOFF.md",
        [
            (r"Current State", "handoff must include current state"),
            (r"Harness Files To Read First", "handoff must include the required read files"),
            (r"Bootstrap Check", "handoff must include bootstrap checks"),
            (r"Remote Runtime", "handoff must include remote runtime rules"),
            (r"Admin@desktop-a4ko83o\.tail7cb6d9\.ts\.net", "handoff must name the WSL SSH target"),
            (r"Clean Exit", "handoff must include clean exit requirements"),
        ],
        errors,
    )
    require_text(
        series_dir / "series_prompt.md",
        [
            (r"\$cv-research-blogger", "series prompt must invoke the CV blogger skill"),
            (r"Three-role workflow", "series prompt must include Planner/Generator/Evaluator workflow"),
            (r"Harness rules", "series prompt must include harness rules"),
            (r"Admin@desktop-a4ko83o\.tail7cb6d9\.ts\.net", "series prompt must name the WSL SSH target"),
            (r"Writing constraints", "series prompt must include writing constraints"),
        ],
        errors,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", help="Series slug, e.g. flow-matching-guide")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if not SLUG_RE.fullmatch(args.slug):
        print("check_harness: slug must use lowercase letters, digits, and single hyphens", file=sys.stderr)
        return 2

    errors: list[str] = []
    warnings: list[str] = []
    series_dir = ROOT / "_blog_work" / args.slug
    for path in REQUIRED_ROOT_FILES:
        require_file(ROOT / path, errors)
    for filename in REQUIRED_SERIES_FILES:
        require_file(series_dir / filename, errors)

    if not errors:
        validate_manifest(args.slug, load_yaml(series_dir / "manifest.yml", errors), errors)
        validate_visual_plan(load_yaml(series_dir / "visual_sources.yml", errors), errors, warnings)
        validate_tasks(load_yaml(series_dir / "series_tasks.yml", errors), errors)
        validate_markdown_handoff(series_dir, errors)

    for warning in warnings:
        print(f"[harness-check] warning: {warning}")
    if errors:
        for error in errors:
            print(f"[harness-check] error: {error}", file=sys.stderr)
        print(f"[harness-check] failed: {args.slug}", file=sys.stderr)
        return 1

    print(f"[harness-check] passed: {args.slug}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
