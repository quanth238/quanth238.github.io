#!/usr/bin/env python3
"""Create checkpointed research blog series files for the CV site."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[2]
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def join_for_template(lines: list[str], template_indent: int = 8) -> str:
    return ("\n" + " " * template_indent).join(lines)


def slug_to_title(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-"))


def validate_slug(slug: str) -> None:
    if not SLUG_RE.fullmatch(slug):
        raise ValueError("slug must use lowercase letters, digits, and single hyphens")


def read_yaml_scalar(text: str, dotted_key: str) -> str | None:
    parts = dotted_key.split(".")
    lines = text.splitlines()
    indent = 0
    start = 0
    for part in parts[:-1]:
        pattern = re.compile(rf"^ {{{indent}}}{re.escape(part)}:\s*$")
        for idx in range(start, len(lines)):
            if pattern.match(lines[idx]):
                start = idx + 1
                indent += 2
                break
        else:
            return None

    key = parts[-1]
    pattern = re.compile(rf"^ {{{indent}}}{re.escape(key)}:\s*(.+?)\s*$")
    for line in lines[start:]:
        match = pattern.match(line)
        if match:
            return match.group(1).strip().strip('"').strip("'")
    return None


def read_yaml_list(text: str, key: str) -> list[str]:
    lines = text.splitlines()
    values: list[str] = []
    in_block = False
    indent = 0
    for line in lines:
        if not in_block:
            match = re.match(rf"^(\s*){re.escape(key)}:\s*$", line)
            if match:
                in_block = True
                indent = len(match.group(1))
            continue
        if line and not line.startswith(" " * (indent + 2)):
            break
        item = re.match(r"^\s*-\s*(.+?)\s*$", line)
        if item:
            values.append(item.group(1).strip().strip('"').strip("'"))
    return values


def existing_manifest(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def normalize_args(args: argparse.Namespace, manifest_path: Path) -> None:
    manifest = existing_manifest(manifest_path)
    if manifest:
        args.title = args.title or read_yaml_scalar(manifest, "series.title")
        args.audience = args.audience or read_yaml_scalar(manifest, "series.audience") or "CS/ML students"
        args.source = args.source or read_yaml_list(manifest, "source_materials")
    args.audience = args.audience or "CS/ML students"
    if not args.title:
        raise ValueError("--title is required when creating a new series")
    if not args.source:
        raise ValueError("--source is required when creating a new series")


def write_new(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path.relative_to(ROOT)} already exists; use --force to overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def manifest_content(args: argparse.Namespace, today: str) -> str:
    sources = join_for_template([f"  - {yaml_quote(source)}" for source in args.source])
    return dedent(
        f"""\
        series:
          slug: {yaml_quote(args.slug)}
          title: {yaml_quote(args.title)}
          audience: {yaml_quote(args.audience)}
          status: "draft"
          created_at: "{today}"
          updated_at: "{today}"
          default_layout: "distill"
          owner: "Quan Tran Hong"

        source_materials:
        {sources}

        harness:
          bootstrap_contract: "_blog_work/{args.slug}/SESSION_BOOTSTRAP.md"
          task_source_of_truth: "_blog_work/{args.slug}/series_tasks.yml"
          visual_source_of_truth: "_blog_work/{args.slug}/visual_sources.yml"
          handoff: "_blog_work/{args.slug}/HANDOFF.md"
          wip_limit: 1
          cold_start_target: "A fresh agent can recover state and choose one verified task from repo files alone."
          remote_runtime:
            ssh: "Admin@desktop-a4ko83o.tail7cb6d9.ts.net"
            wsl_distro: "Ubuntu-24.04"
            policy: "Use WSL for code examples, training, figure generation, and expensive build/render checks; keep the Mac for editing, git, and lightweight static checks."

        checkpoints:
          intake: "created"
          outline: "created"
          visual_plan: "created"
          draft: "created"
          code_run: "pending"
          human_voice_pass: "pending"
          citation_check: "pending"
          jekyll_render_check: "pending"
          publish_approval: "pending"

        approval:
          outline: false
          final_draft: false
          publish: false

        notes:
          personal_angle: "Explain the topic directly with concise theory, visual structure, and code."
          visual_default: "Plan visual sources first; write figure briefs; prefer Mermaid and local plots for precise technical objects; use AI figures only when they improve intuition."
          style_reference: "Robot Learning: A Tutorial style: scoped tutorial, named topic sections, concise theory, code examples."
          publication_rule: "Keep drafts in _drafts until explicit approval."
        """
    )


def visual_sources_content(args: argparse.Namespace, today: str) -> str:
    sources = "\n".join(
        (
            f"  - source: {yaml_quote(source)}\n"
            '    idea: "Primary source to cite; extract conceptual guidance only, not image pixels."\n'
            '    use: "citation"'
        )
        for source in args.source
    )
    return (
        f"series: {yaml_quote(args.slug)}\n"
        f'created_at: "{today}"\n'
        f'updated_at: "{today}"\n'
        "visual_contract:\n"
        '  standard: "Plan the visual before drawing it; every reader-facing figure needs a brief, local asset or editable source, alt text, and evaluator decision."\n'
        '  evidence: "Store source references, figure briefs, prompts, generated paths, code-result paths, and evaluator notes in this file."\n'
        '  approval_rule: "A weak or generic figure is marked redesign and is not described as professional."\n\n'
        "policy:\n"
        '  external_images: "Do not copy, trace, or hotlink external diagrams."\n'
        '  generated_images: "Create original figures from cited ideas; store prompt, asset path, and alt text."\n'
        '  mermaid: "Use Mermaid for editable structural diagrams."\n\n'
        "references:\n"
        f"{sources}\n\n"
        "figure_briefs: []\n"
        "generated_figures: []\n"
        "mermaid_figures: []\n"
        "remote_code_figures: []\n"
        "quality_gate:\n"
        '  required_before_publish: "Evaluator checks conceptual correctness, reader flow, label quality, originality, accessibility, and Jekyll rendering."\n'
        '  evaluator_status: "pending"\n'
        "evaluator_notes: []\n"
    )


def draft_content(args: argparse.Namespace, today: str) -> str:
    title = f"{args.title}, part {args.part}"
    description = yaml_quote(
        f"A practical first pass at {args.title}: the object to learn, the smallest example, and the result to inspect."
    )
    source_lines = join_for_template([f"- [{source}]({source})" for source in args.source])
    front_matter_sources = join_for_template([f"  - {yaml_quote(source)}" for source in args.source])
    topic_label = slug_to_title(args.slug)
    return dedent(
        f"""\
        ---
        layout: distill
        title: {yaml_quote(title)}
        description: {description}
        date: {today}
        author: "Quan Tran Hong"
        tags: ["tutorial", "reading-notes", "generative-modeling"]
        categories: ["tutorial"]
        series: {yaml_quote(args.slug)}
        part: {args.part}
        draft_stage: "draft"
        publish_ready: false
        mermaid:
          enabled: true
          zoomable: true
        chart:
          plotly: false
          vega_lite: false
        visual_plan: "_blog_work/{args.slug}/visual_sources.yml"
        source_materials:
        {front_matter_sources}
        ---

        ## Introduction

        <!-- Write the practical entry point first: the object being learned, the path from input to output, and the first quantity the reader should compute. -->

        ## Problem setup

        <!-- Define the smallest notation needed for this topic. Keep the first equation close to the first implementation target. -->

        ## Path and velocity target

        <!-- Explain the path and target quantity that turn the source material into something a student can run or draw. -->

        ```mermaid
        flowchart LR
            accTitle: {topic_label} Working Diagram
            accDescr: The diagram connects the input assumptions to the quantity being optimized or computed.

            source["Source material"]
            setup["Problem setup"]
            construction["Path and target"]
            objective["Objective or computation"]
            result["Result to inspect"]

            source --> setup
            setup --> construction
            construction --> objective
            objective --> result
        ```

        ## Training objective

        <!-- State the objective in the same symbols introduced above. Explain what each term does before moving to code. -->

        ## Minimal implementation

        <!-- Add the smallest runnable fragment that matches the notation above. Keep imports and helper functions only when they are needed. -->

        ## Code result

        <!-- Describe what the result shows, not how the pipeline produced it. Add local figures from assets/img/blog/<series-slug>/. -->

        ## Sampling procedure

        <!-- Describe how the trained or computed object is used. Put theory here after the reader has seen the loss, code, and result. -->

        ## Next part

        <!-- State only what the next part will cover, ideally in one short sentence. -->

        ## References and visual resources

        Primary source:

        {source_lines}

        """
    )


def series_tasks_content(args: argparse.Namespace, today: str) -> str:
    draft_path = f"_drafts/{args.slug}-part-{args.part}.md"
    return dedent(
        f"""\
        series: {yaml_quote(args.slug)}
        updated_at: {yaml_quote(today)}
        wip_limit: 1
        current_state: "initialized"
        active_task: "H-00"
        state_policy:
          valid_states: ["not_started", "active", "blocked", "passing"]
          transition_rule: "A task can move to passing only after its verification commands pass and evidence is recorded."
          source_of_truth: "_blog_work/{args.slug}/series_tasks.yml"

        tasks:
          - id: "H-00"
            title: "Verify series harness"
            behavior: "Confirm a fresh agent can recover instructions, state, visual plan, task list, handoff, and verification commands from repo files alone."
            state: "active"
            verification:
              - "python3 scripts/blog_pipeline/check_harness.py {args.slug}"
            evidence:
              - "_blog_work/{args.slug}/SESSION_BOOTSTRAP.md"
              - "_blog_work/{args.slug}/manifest.yml"
              - "_blog_work/{args.slug}/visual_sources.yml"
              - "_blog_work/{args.slug}/series_tasks.yml"
              - "_blog_work/{args.slug}/HANDOFF.md"
          - id: "P{args.part:02d}-01"
            title: "Plan Part {args.part}"
            behavior: "Choose one practical reader question, source map, visual references, figure briefs, and code-result target for Part {args.part}."
            state: "not_started"
            verification:
              - "python3 scripts/blog_pipeline/check_harness.py {args.slug}"
            acceptance:
              - "manifest.yml and visual_sources.yml contain the source and visual decisions."
              - "Each planned reader-facing visual has a figure brief before creation."
          - id: "P{args.part:02d}-02"
            title: "Draft Part {args.part}"
            behavior: "Write the draft around the approved plan without process prose or uncited technical claims."
            state: "not_started"
            depends_on: ["P{args.part:02d}-01"]
            verification:
              - "python3 scripts/blog_pipeline/check_post.py {draft_path}"
            acceptance:
              - "Draft has required sections, source links, local visuals or Mermaid, and non-empty alt text."
          - id: "P{args.part:02d}-03"
            title: "Run Part {args.part} example"
            behavior: "Generate inspectable code-result figures on the WSL server and import run metadata for the draft's claimed result."
            state: "not_started"
            depends_on: ["P{args.part:02d}-02"]
            verification:
              - "python3 scripts/blog_pipeline/run_remote_example.py --slug {args.slug} --script scripts/blog_pipeline/examples/<example>.py"
            acceptance:
              - "Figures are saved under assets/img/blog/{args.slug}/."
              - "Run metadata is saved under _blog_work/{args.slug}/remote_runs/."
              - "Remote metadata records ssh Admin@desktop-a4ko83o.tail7cb6d9.ts.net or the approved WSL target."
          - id: "P{args.part:02d}-04"
            title: "Review and publish-check Part {args.part}"
            behavior: "Evaluate citations, visual quality, local assets, equation width, human voice, Jekyll rendering, and handoff readiness."
            state: "not_started"
            depends_on: ["P{args.part:02d}-03"]
            verification:
              - "python3 scripts/blog_pipeline/check_post.py {draft_path}"
              - "BUNDLE_GEMFILE=/Users/quan238/personal/cv/Gemfile bundle exec jekyll build --drafts"
            acceptance:
              - "Evaluator notes are recorded in visual_sources.yml or HANDOFF.md."
              - "User approval is recorded before moving a draft into _posts/."

        completion_evidence_required:
          - "python3 scripts/blog_pipeline/check_harness.py {args.slug}"
          - "python3 scripts/blog_pipeline/check_post.py <draft-or-post>"
          - "python3 -m py_compile scripts/blog_pipeline/*.py scripts/blog_pipeline/examples/*.py"
          - "Run code examples and figure-generation scripts on WSL through scripts/blog_pipeline/run_remote_example.py."
          - "Run Jekyll/browser or screenshot verification on WSL when the render check is compute-heavy."
        """
    )


def bootstrap_content(args: argparse.Namespace) -> str:
    draft_path = f"_drafts/{args.slug}-part-{args.part}.md"
    return dedent(
        f"""\
        # {args.title} Session Bootstrap

        Use this file as the cold-start contract for a fresh agent session. The
        session should recover the current blog state from repository files,
        choose one task, and verify it without relying on chat history.

        ## Read Order

        1. `AGENTS.md`
        2. `codex/skills/cv-research-blogger/SKILL.md`
        3. `codex/skills/cv-research-blogger/visual_quality.md`
        4. `_blog_work/{args.slug}/manifest.yml`
        5. `_blog_work/{args.slug}/visual_sources.yml`
        6. `_blog_work/{args.slug}/series_tasks.yml`
        7. `_blog_work/{args.slug}/HANDOFF.md`
        8. `_blog_work/{args.slug}/series_prompt.md`

        ## Cold-Start Questions

        - What is the active series and current draft/post state?
        - Which file is the task source of truth?
        - Which visual assets are planned, created, approved, or marked redesign?
        - What verification commands prove the active task is acceptable?
        - What is the next single task under the WIP limit?

        ## Harness Subsystems

        - Instructions: `AGENTS.md`, the CV blogger skill, and `visual_quality.md`.
        - Environment: Docker/Jekyll, Python scripts under `scripts/blog_pipeline/`,
          and local assets under `assets/img/blog/{args.slug}/`.
        - State: `manifest.yml`, `series_tasks.yml`, `HANDOFF.md`, run logs, and git history.
        - Tools: `new_series.py`, `plan_visuals.py`, `run_remote_example.py`,
          `check_post.py`, and `check_harness.py`.
        - Feedback: blog checker, Python compile check, Jekyll build,
          browser/screenshot visual review, and evaluator notes.

        ## Remote Runtime

        Use the Mac as the control and editing machine. Run code examples,
        training, figure-generation scripts, and expensive build/render checks on
        the WSL server:

        ```bash
        ssh Admin@desktop-a4ko83o.tail7cb6d9.ts.net
        python3 scripts/blog_pipeline/run_remote_example.py --slug {args.slug} --script scripts/blog_pipeline/examples/<example>.py
        ```

        `run_remote_example.py` defaults to
        `Admin@desktop-a4ko83o.tail7cb6d9.ts.net` and `Ubuntu-24.04`. Local Mac
        commands are acceptable for file inspection, git, `check_harness.py`,
        `check_post.py`, and Python syntax checks because they are lightweight.

        ## Start Commands

        ```bash
        python3 scripts/blog_pipeline/check_harness.py {args.slug}
        python3 scripts/blog_pipeline/check_post.py {draft_path}
        python3 -m py_compile scripts/blog_pipeline/*.py scripts/blog_pipeline/examples/*.py
        ```

        The draft check may fail before Planner and Generator complete their work.
        Record that failure in `HANDOFF.md` instead of treating the draft as ready.

        ## Task Rules

        - Keep `wip_limit: 1`.
        - Treat `_blog_work/{args.slug}/series_tasks.yml` as the only task source of truth.
        - Valid task states are `not_started`, `active`, `blocked`, and `passing`.
        - A task moves to `passing` only after verification passes and evidence is recorded.
        - Write visual decisions to `visual_sources.yml`, not into the reader-facing post body.

        ## Clean Exit

        - Update `series_tasks.yml` with state and evidence.
        - Update `HANDOFF.md` with current branch, changed files, checks run, blockers, and next task.
        - Leave generated assets either referenced in `visual_sources.yml` or removed.
        - Record failed checks explicitly if any remain.
        """
    )


def handoff_content(args: argparse.Namespace, today: str) -> str:
    draft_path = f"_drafts/{args.slug}-part-{args.part}.md"
    return dedent(
        f"""\
        # {args.title} Handoff

        State date: {today}

        ## Current State

        - Worktree: `{ROOT}`
        - Series slug: `{args.slug}`
        - Draft: `{draft_path}`
        - Task source of truth: `_blog_work/{args.slug}/series_tasks.yml`
        - Visual source of truth: `_blog_work/{args.slug}/visual_sources.yml`
        - Cold-start contract: `_blog_work/{args.slug}/SESSION_BOOTSTRAP.md`
        - Remote runtime: `ssh Admin@desktop-a4ko83o.tail7cb6d9.ts.net`, WSL `Ubuntu-24.04`
        - Keep WIP to one active task.

        ## Harness Files To Read First

        - `AGENTS.md`
        - `codex/skills/cv-research-blogger/SKILL.md`
        - `codex/skills/cv-research-blogger/visual_quality.md`
        - `_blog_work/{args.slug}/SESSION_BOOTSTRAP.md`
        - `_blog_work/{args.slug}/manifest.yml`
        - `_blog_work/{args.slug}/visual_sources.yml`
        - `_blog_work/{args.slug}/series_tasks.yml`
        - `_blog_work/{args.slug}/series_prompt.md`

        ## Bootstrap Check

        ```bash
        python3 scripts/blog_pipeline/check_harness.py {args.slug}
        python3 scripts/blog_pipeline/check_post.py {draft_path}
        python3 -m py_compile scripts/blog_pipeline/*.py scripts/blog_pipeline/examples/*.py
        ```

        The draft check is expected to fail until the visual plan, draft prose,
        local visuals, and references are complete.

        ## Remote Runtime

        Use the Mac for editing, git, and lightweight static checks only. Run
        code examples, training, figure generation, and expensive build/render
        checks on the WSL server:

        ```bash
        python3 scripts/blog_pipeline/run_remote_example.py --slug {args.slug} --script scripts/blog_pipeline/examples/<example>.py
        ```

        The script defaults to `Admin@desktop-a4ko83o.tail7cb6d9.ts.net` and
        `Ubuntu-24.04`, imports remote outputs into `_blog_work/{args.slug}/`,
        and copies figures into `assets/img/blog/{args.slug}/`.

        ## Next Recommended Session

        Start with the Planner role. Complete `H-00` by running the harness check,
        then activate `P{args.part:02d}-01` to plan Part {args.part}. Do not draft
        until `visual_sources.yml` contains cited visual references and figure briefs.

        ## Clean Exit Requirements

        - Update `series_tasks.yml` with the active task state and evidence.
        - Update this handoff with checks run, unresolved blockers, and next action.
        - Keep all generated assets local and registered in `visual_sources.yml`.
        - Record failed checks explicitly instead of marking a task complete.
        """
    )


def series_prompt_content(args: argparse.Namespace) -> str:
    source_lines = "\n".join(f"- {source}" for source in args.source)
    return dedent(
        f"""\
        # {args.title} Series Prompt

        Use this prompt to continue the {args.title} tutorial series.

        ```text
        Use $cv-research-blogger for the {args.title} series.

        Workspace:
        - Work only in {ROOT}.
        - Use the current codex/* branch unless the user asks for a new branch.
        - Do not edit /Users/quan238/personal/cv directly.
        - Before writing, read AGENTS.md, codex/skills/cv-research-blogger/SKILL.md,
          codex/skills/cv-research-blogger/visual_quality.md, SESSION_BOOTSTRAP.md,
          manifest.yml, visual_sources.yml, series_tasks.yml, HANDOFF.md, and this prompt.
        - Run python3 scripts/blog_pipeline/check_harness.py {args.slug} before
          changing a post, visual, or pipeline file.

        Source:
        {source_lines}

        Goal:
        Write the tutorial for {args.audience} in a clear, technical, concise voice.
        Each part should answer one practical question first, then add only the
        theory needed to understand it.

        Three-role workflow:
        1. Planner: choose the practical question, map sources, collect visual/blog
           references, plan original figures, and define the code result. Write
           figure briefs before any figure is generated or drawn.
        2. Generator: write the outline and prose, create Mermaid diagrams or local
           figures, and build the runnable example around the Planner target.
        3. Evaluator: check citations, visual metadata, local assets, equation width,
           human voice, code-result presence, professional visual quality, Jekyll
           build, browser rendering, and handoff readiness.

        Harness rules:
        - Treat series_tasks.yml as the only source of truth for active work.
        - Keep WIP to one task. Valid states are not_started, active, blocked, and passing.
        - Do not mark a task passing until verification commands pass and evidence is recorded.
        - Run code examples, training, figure-generation scripts, and expensive
          build/render checks on the WSL server through
          ssh Admin@desktop-a4ko83o.tail7cb6d9.ts.net or run_remote_example.py.
          Use the Mac only for editing, git, and lightweight static checks.
        - Store visual decisions in visual_sources.yml and final assets under assets/img/blog/{args.slug}/.
        - End every session by updating HANDOFF.md and task evidence.

        Writing constraints:
        - No pipeline/process prose in the article body.
        - Use direct topic sections, not generic labels.
        - Put the practical target before large derivations.
        - Keep equations narrow; avoid display math that scrolls.
        - Cite core papers for core claims and related papers for design choices.
        - Use original local figures or Mermaid diagrams; do not copy or hotlink images.
        - Every major visual needs a figure brief in visual_sources.yml before creation.
        - Prefer local SVG/matplotlib plots for precise technical objects.
        - Code-result prose should explain what the result shows, not how the pipeline ran.
        - End each part with one short sentence saying what the next part covers.

        First, inspect the handoff and task list. Implement only one active part
        or visual redesign at a time.
        ```
        """
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", required=True, help="Series slug, e.g. flow-matching-guide")
    parser.add_argument("--title", help="Human-readable series title; optional when the series manifest already exists")
    parser.add_argument("--source", action="append", help="Source URL or path; repeat for multiple sources")
    parser.add_argument("--audience", help="Target reader; optional when the series manifest already exists")
    parser.add_argument("--part", type=int, default=1, help="Draft part number")
    parser.add_argument("--date", default=date.today().isoformat(), help="ISO date for draft front matter")
    parser.add_argument("--force", action="store_true", help="Overwrite generated files")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        validate_slug(args.slug)
        if args.part < 1:
            raise ValueError("--part must be >= 1")
        series_dir = ROOT / "_blog_work" / args.slug
        asset_dir = ROOT / "assets" / "img" / "blog" / args.slug
        draft_path = ROOT / "_drafts" / f"{args.slug}-part-{args.part}.md"
        manifest_path = series_dir / "manifest.yml"
        visual_sources_path = series_dir / "visual_sources.yml"
        series_tasks_path = series_dir / "series_tasks.yml"
        bootstrap_path = series_dir / "SESSION_BOOTSTRAP.md"
        handoff_path = series_dir / "HANDOFF.md"
        series_prompt_path = series_dir / "series_prompt.md"
        normalize_args(args, manifest_path)

        if not manifest_path.exists() or args.force:
            write_new(manifest_path, manifest_content(args, args.date), args.force)
        if not visual_sources_path.exists() or args.force:
            write_new(visual_sources_path, visual_sources_content(args, args.date), args.force)
        if not series_tasks_path.exists() or args.force:
            write_new(series_tasks_path, series_tasks_content(args, args.date), args.force)
        if not bootstrap_path.exists() or args.force:
            write_new(bootstrap_path, bootstrap_content(args), args.force)
        if not handoff_path.exists() or args.force:
            write_new(handoff_path, handoff_content(args, args.date), args.force)
        if not series_prompt_path.exists() or args.force:
            write_new(series_prompt_path, series_prompt_content(args), args.force)
        asset_dir.mkdir(parents=True, exist_ok=True)
        (asset_dir / ".gitkeep").touch(exist_ok=True)
        write_new(draft_path, draft_content(args, args.date), args.force)
    except (FileExistsError, ValueError) as exc:
        print(f"new_series: {exc}", file=sys.stderr)
        return 1

    print(f"Ready {manifest_path.relative_to(ROOT)}")
    print(f"Ready {visual_sources_path.relative_to(ROOT)}")
    print(f"Ready {series_tasks_path.relative_to(ROOT)}")
    print(f"Ready {bootstrap_path.relative_to(ROOT)}")
    print(f"Ready {handoff_path.relative_to(ROOT)}")
    print(f"Ready {series_prompt_path.relative_to(ROOT)}")
    print(f"Created {draft_path.relative_to(ROOT)}")
    print(f"Created {asset_dir.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
