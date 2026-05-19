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
          visual_default: "Plan visual sources first; use Mermaid for editable structure and original AI figures when they improve intuition."
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
        "policy:\n"
        '  external_images: "Do not copy, trace, or hotlink external diagrams."\n'
        '  generated_images: "Create original figures from cited ideas; store prompt, asset path, and alt text."\n'
        '  mermaid: "Use Mermaid for editable structural diagrams."\n\n'
        "references:\n"
        f"{sources}\n\n"
        "generated_figures: []\n"
        "mermaid_figures: []\n"
        "remote_code_figures: []\n"
    )


def draft_content(args: argparse.Namespace, today: str) -> str:
    title = f"{args.title}, part {args.part}"
    source_lines = join_for_template([f"- [{source}]({source})" for source in args.source])
    front_matter_sources = join_for_template([f"  - {yaml_quote(source)}" for source in args.source])
    topic_label = slug_to_title(args.slug)
    return dedent(
        f"""\
        ---
        layout: distill
        title: {yaml_quote(title)}
        description: "A concise tutorial note that connects the idea, math, diagram, and code."
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

        ## Core construction

        <!-- Explain the construction step that turns the source material into something a student can run or draw. -->

        ```mermaid
        flowchart LR
            accTitle: {topic_label} Working Diagram
            accDescr: The diagram should show the practical path from input assumptions to the quantity being optimized or computed.

            source["Source material"]
            setup["Problem setup"]
            construction["Core construction"]
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

        <!-- State what this part established, what question remains, and what the next part will cover. -->

        ## References and visual resources

        Primary source:

        {source_lines}

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
        normalize_args(args, manifest_path)

        if not manifest_path.exists() or args.force:
            write_new(manifest_path, manifest_content(args, args.date), args.force)
        if not visual_sources_path.exists() or args.force:
            write_new(visual_sources_path, visual_sources_content(args, args.date), args.force)
        asset_dir.mkdir(parents=True, exist_ok=True)
        (asset_dir / ".gitkeep").touch(exist_ok=True)
        write_new(draft_path, draft_content(args, args.date), args.force)
    except (FileExistsError, ValueError) as exc:
        print(f"new_series: {exc}", file=sys.stderr)
        return 1

    print(f"Ready {manifest_path.relative_to(ROOT)}")
    print(f"Ready {visual_sources_path.relative_to(ROOT)}")
    print(f"Created {draft_path.relative_to(ROOT)}")
    print(f"Created {asset_dir.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
