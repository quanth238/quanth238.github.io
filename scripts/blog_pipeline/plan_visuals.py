#!/usr/bin/env python3
"""Create or update visual-source plans for CV research blog posts."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def yaml_literal(value: str, indent: str = "    ") -> str:
    lines = value.rstrip().splitlines() or [""]
    return "|\n" + "\n".join(f"{indent}{line}" for line in lines)


def validate_slug(slug: str) -> None:
    if not SLUG_RE.fullmatch(slug):
        raise ValueError("slug must use lowercase letters, digits, and single hyphens")


def default_plan(slug: str, today: str) -> str:
    return (
        f"series: {yaml_quote(slug)}\n"
        f"created_at: {yaml_quote(today)}\n"
        f"updated_at: {yaml_quote(today)}\n"
        "policy:\n"
        "  external_images: \"Do not copy, trace, or hotlink external diagrams.\"\n"
        "  generated_images: \"Create original figures from cited ideas; store prompt, asset path, and alt text.\"\n"
        "  mermaid: \"Use Mermaid for editable structural diagrams.\"\n\n"
        "references: []\n"
        "generated_figures: []\n"
        "mermaid_figures: []\n"
        "remote_code_figures: []\n"
    )


def ensure_plan(path: Path, slug: str) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(default_plan(slug, date.today().isoformat()), encoding="utf-8")


def append_to_section(text: str, section: str, block: str) -> str:
    empty = f"{section}: []"
    if empty in text:
        return text.replace(empty, f"{section}:\n{block.rstrip()}", 1)

    section_match = re.search(rf"^{re.escape(section)}:\s*$", text, flags=re.MULTILINE)
    if not section_match:
        return text.rstrip() + f"\n{section}:\n{block.rstrip()}\n"

    next_section = re.search(r"^[a-z_]+:\s*(?:\[\])?\s*$", text[section_match.end() :], flags=re.MULTILINE)
    insert_at = len(text)
    if next_section:
        insert_at = section_match.end() + next_section.start()
    prefix = text[:insert_at].rstrip()
    suffix = text[insert_at:]
    return f"{prefix}\n{block.rstrip()}\n{suffix.lstrip()}"


def update_timestamp(text: str) -> str:
    today = date.today().isoformat()
    if re.search(r'^updated_at:\s*".*"$', text, flags=re.MULTILINE):
        return re.sub(r'^updated_at:\s*".*"$', f'updated_at: "{today}"', text, count=1, flags=re.MULTILINE)
    return text.rstrip() + f'\nupdated_at: "{today}"\n'


def add_reference(text: str, source: str, idea: str, title: str | None, use: str) -> str:
    if source in text and idea in text:
        return text
    title_line = f"\n    title: {yaml_quote(title)}" if title else ""
    block = (
        f"  - source: {yaml_quote(source)}{title_line}\n"
        f"    idea: {yaml_quote(idea)}\n"
        f"    use: {yaml_quote(use)}\n"
    )
    return append_to_section(text, "references", block)


def add_generated_figure(
    text: str,
    asset: str,
    alt: str,
    prompt: str,
    inspiration_sources: list[str],
) -> str:
    if re.match(r"https?://", asset):
        raise ValueError("--asset must be a local project path, not an external URL")
    if asset in text:
        return text
    sources = inspiration_sources or []
    source_lines = "\n".join(f"      - {yaml_quote(source)}" for source in sources) or "      []"
    block = (
        f"  - path: {yaml_quote(asset)}\n"
        f"    alt: {yaml_quote(alt)}\n"
        f"    prompt: {yaml_literal(prompt, indent='      ')}\n"
        "    inspiration_sources:\n"
        f"{source_lines}\n"
        '    status: "created"\n'
    )
    return append_to_section(text, "generated_figures", block)


def add_mermaid(text: str, mermaid_id: str, purpose: str) -> str:
    if mermaid_id in text:
        return text
    block = (
        f"  - id: {yaml_quote(mermaid_id)}\n"
        f"    purpose: {yaml_quote(purpose)}\n"
        '    status: "created"\n'
    )
    return append_to_section(text, "mermaid_figures", block)


def add_remote_code_figure(text: str, asset: str, alt: str, run_id: str | None) -> str:
    if re.match(r"https?://", asset):
        raise ValueError("--remote-asset must be a local project path, not an external URL")
    if asset in text:
        return text
    run_line = f"\n    run_id: {yaml_quote(run_id)}" if run_id else ""
    block = (
        f"  - path: {yaml_quote(asset)}\n"
        f"    alt: {yaml_quote(alt)}{run_line}\n"
        '    status: "created"\n'
    )
    return append_to_section(text, "remote_code_figures", block)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", required=True, help="Series slug, e.g. flow-matching-guide")
    parser.add_argument("--source", required=True, help="External source URL or local source path")
    parser.add_argument("--idea", required=True, help="Visual idea to cite from the source")
    parser.add_argument("--title", help="Optional source title")
    parser.add_argument("--use", default="visual-reference", help="How this source should be used")
    parser.add_argument("--asset", help="Generated local image path to register")
    parser.add_argument("--alt", help="Alt text for --asset or --remote-asset")
    parser.add_argument("--prompt", help="Final image-generation prompt for --asset")
    parser.add_argument("--inspiration-source", action="append", default=[], help="Source that inspired --asset")
    parser.add_argument("--mermaid-id", help="Mermaid diagram id to register")
    parser.add_argument("--mermaid-purpose", default="Editable structural diagram")
    parser.add_argument("--remote-asset", help="Remote-code-generated local figure path to register")
    parser.add_argument("--run-id", help="Remote run id for --remote-asset")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        validate_slug(args.slug)
        plan_path = ROOT / "_blog_work" / args.slug / "visual_sources.yml"
        ensure_plan(plan_path, args.slug)
        text = plan_path.read_text(encoding="utf-8")
        text = add_reference(text, args.source, args.idea, args.title, args.use)
        if args.asset:
            if not args.alt or not args.prompt:
                raise ValueError("--asset requires --alt and --prompt")
            text = add_generated_figure(text, args.asset, args.alt, args.prompt, args.inspiration_source)
        if args.mermaid_id:
            text = add_mermaid(text, args.mermaid_id, args.mermaid_purpose)
        if args.remote_asset:
            if not args.alt:
                raise ValueError("--remote-asset requires --alt")
            text = add_remote_code_figure(text, args.remote_asset, args.alt, args.run_id)
        plan_path.write_text(update_timestamp(text), encoding="utf-8")
    except ValueError as exc:
        print(f"plan_visuals: {exc}", file=sys.stderr)
        return 1

    print(f"Updated {plan_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
