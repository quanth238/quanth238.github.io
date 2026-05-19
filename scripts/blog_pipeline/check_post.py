#!/usr/bin/env python3
"""Validate a CV research blog draft or post before review/publishing."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REQUIRED_FRONT_MATTER = {
    "layout",
    "title",
    "description",
    "date",
    "tags",
    "categories",
    "series",
    "part",
    "draft_stage",
    "publish_ready",
    "mermaid",
    "visual_plan",
    "source_materials",
}
REQUIRED_SECTIONS = [
    "Introduction",
    "Problem setup",
    "Core construction",
    "Training objective",
    "Minimal implementation",
    "Code result",
    "Sampling procedure",
    "Next part",
    "References and visual resources",
]
FORBIDDEN_SECTION_NAMES = [
    "What problem this solves",
    "My mental model",
    "Minimum math",
    "Visual explanation",
    "Toy code",
    "Common confusions",
    "References and next reading",
]
BANNED_PATTERNS = [
    r"\bcheckpoint draft\b",
    r"\bthis file is a scaffold\b",
    r"\bshould help a student answer\b",
    r"\bnotebook written after\b",
    r"\bthe reader should see\b",
    r"\breplace with\b",
    r"\bTODO\b",
    r"\bFIXME\b",
    r"\bdelve\b",
    r"\btapestry\b",
    r"\bvibrant\b",
    r"\bcrucial\b",
    r"\bmeticulous\b",
    r"\brobust\b",
    r"\bseamless\b",
    r"\bgroundbreaking\b",
    r"\bleverage\b",
    r"\bsynergy\b",
    r"\btransformative\b",
    r"\bparamount\b",
    r"\bmultifaceted\b",
    r"\bmyriad\b",
    r"\bcornerstone\b",
    r"\breimagine\b",
    r"\bempower\b",
    r"\bcatalyst\b",
    r"\binvaluable\b",
    r"\brealm\b",
    r"\bdeep dive\b",
    r"\bactionable\b",
    r"\bimpactful\b",
    r"\blearnings\b",
    r"\bfurthermore\b",
    r"\bmoreover\b",
    r"\bholistic\b",
    r"\butilize\b",
    r"\bfacilitate\b",
    r"\bit is worth noting\b",
    r"\bin today's digital age\b",
    r"\bplays a crucial role\b",
    r"\bserves as a testament\b",
    r"\blet's dive in\b",
    r"\bkey takeaways\b",
    r"\bgreat question\b",
    r"\bi hope this helps\b",
    r"\bthe figure is original\b",
    r"\bthis figure is original\b",
    r"\bthis diagram is original\b",
    r"\boriginal (?:figure|diagram|visual)\b",
    r"\bvisual plan is based\b",
    r"\bdo not copy\b",
    r"\bnot copied diagrams\b",
    r"\bi generated (?:this|the) (?:figure|diagram|image|visual)\b",
    r"\bgenerated (?:with|by) (?:AI|ChatGPT|image generation)\b",
    r"\bi ran a small\b",
    r"\bi ran (?:a|the) (?:small|minimal|toy)\b",
    r"\bdependency-light\b",
    r"\bremote WSL server\b",
    r"\bscripts/blog_pipeline\b",
    r"\bthis code does not implement\b",
    r"\bthe code does not implement\b",
    r"\bdoes not implement the full\b",
    r"\bthis is not a full implementation\b",
    r"\bnot a production implementation\b",
    r"\bfor provenance\b",
    r"\bfigure provenance\b",
    r"\bprompt provenance\b",
]


def split_front_matter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("file must start with YAML front matter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("front matter closing '---' not found")
    return text[4:end], text[end + 5 :]


def front_matter_keys(front_matter: str) -> set[str]:
    keys: set[str] = set()
    for line in front_matter.splitlines():
        if not line or line.startswith(" ") or line.startswith("-"):
            continue
        if ":" in line:
            keys.add(line.split(":", 1)[0].strip())
    return keys


def front_matter_value(front_matter: str, key: str) -> str | None:
    pattern = re.compile(rf"^{re.escape(key)}:\s*(.*)$", re.MULTILINE)
    match = pattern.search(front_matter)
    if not match:
        return None
    return match.group(1).strip().strip('"').strip("'")


def is_post_path(path: Path) -> bool:
    return "_posts" in path.parts or bool(re.match(r"\d{4}-\d{2}-\d{2}-", path.name))


def has_visual(body: str) -> bool:
    return bool(
        re.search(r"```mermaid\s", body)
        or re.search(r"!\[[^\]]+\]\([^)]+\)", body)
        or re.search(r"{%\s*include\s+figure\.liquid\b", body)
        or re.search(r"```(?:plotly|vega_lite|echarts)\s", body)
    )


def image_alt_errors(body: str) -> list[str]:
    errors: list[str] = []
    for match in re.finditer(r"!\[([^\]]*)\]\(([^)]+)\)", body):
        if not match.group(1).strip():
            errors.append(f"image {match.group(2)} is missing alt text")
    for match in re.finditer(r"{%\s*include\s+figure\.liquid\b([^%]*)%}", body):
        include = match.group(0)
        if " alt=" not in include and " alt='" not in include and ' alt="' not in include:
            errors.append("figure include is missing alt text")
    return errors


def markdown_image_errors(body: str) -> list[str]:
    errors: list[str] = []
    for match in re.finditer(r"!\[([^\]]*)\]\(([^)]+)\)", body):
        target = match.group(2).strip()
        if re.match(r"https?://", target):
            errors.append(f"external image hotlink is not allowed: {target}")
            continue
        if target.startswith("#") or target.startswith("mailto:"):
            continue
        local = target.split("#", 1)[0].split("?", 1)[0]
        local_path = ROOT / local.lstrip("/")
        if not local_path.exists():
            errors.append(f"local image does not exist: {target}")
    return errors


def liquid_figure_errors(body: str) -> list[str]:
    errors: list[str] = []
    for match in re.finditer(r"{%\s*include\s+figure\.liquid\b([^%]*)%}", body):
        include = match.group(1)
        path_match = re.search(r'\bpath=(?:"([^"]+)"|\'([^\']+)\'|([^\s]+))', include)
        if not path_match:
            continue
        target = next(value for value in path_match.groups() if value)
        if re.match(r"https?://", target):
            errors.append(f"external figure hotlink is not allowed: {target}")
            continue
        local_path = ROOT / target.lstrip("/")
        if not local_path.exists():
            errors.append(f"local figure does not exist: {target}")
    return errors


def local_asset_errors(value: str | None, label: str) -> list[str]:
    if not value:
        return [f"missing {label}"]
    if re.match(r"https?://", value):
        return [f"{label} must be a local asset, not an external URL: {value}"]
    local_path = ROOT / value.lstrip("/")
    if not local_path.exists():
        return [f"{label} does not exist: {value}"]
    return []


def section_order_errors(body: str) -> list[str]:
    positions: dict[str, int] = {}
    for section in REQUIRED_SECTIONS:
        match = re.search(rf"^##\s+{re.escape(section)}\s*$", body, re.MULTILINE)
        if match:
            positions[section] = match.start()

    ordered = [section for section in REQUIRED_SECTIONS if section in positions]
    for left, right in zip(ordered, ordered[1:]):
        if positions[left] > positions[right]:
            return [
                "sections are out of order; expected: "
                + " -> ".join(REQUIRED_SECTIONS)
            ]
    return []


def visual_plan_errors(front_matter: str, body: str) -> list[str]:
    errors: list[str] = []
    plan_value = front_matter_value(front_matter, "visual_plan")
    series = front_matter_value(front_matter, "series")
    if not plan_value and series:
        plan_value = f"_blog_work/{series}/visual_sources.yml"
    if not plan_value:
        return ["missing visual_plan front matter or series-derived visual plan"]

    plan_path = ROOT / plan_value.lstrip("/")
    if not plan_path.exists():
        return [f"visual plan not found: {plan_value}"]

    plan = plan_path.read_text(encoding="utf-8")
    if "Do not copy" not in plan or "hotlink" not in plan:
        errors.append("visual plan must include no-copy/no-hotlink policy")

    references_block = re.search(
        r"^references:\s*(.*?)(?:\n[a-z_]+:\s*(?:\[\])?\s*$|\Z)",
        plan,
        flags=re.DOTALL | re.MULTILINE,
    )
    references_text = references_block.group(1) if references_block else ""
    source_count = len(re.findall(r"^\s*-\s+source:\s+\"?https?://", references_text, flags=re.MULTILINE))
    if source_count < 2:
        errors.append("visual plan must include at least two external visual/blog references")

    for path in re.findall(r"^\s*-\s+path:\s+\"([^\"]+)\"", plan, flags=re.MULTILINE):
        if re.match(r"https?://", path):
            errors.append(f"visual plan path must be local, not external: {path}")
            continue
        if not (ROOT / path.lstrip("/")).exists():
            errors.append(f"visual plan local asset does not exist: {path}")

    for section in ("generated_figures", "remote_code_figures"):
        block = re.search(
            rf"^{section}:\s*(.*?)(?:\n[a-z_]+:\s*(?:\[\])?\s*$|\Z)",
            plan,
            flags=re.DOTALL | re.MULTILINE,
        )
        section_text = block.group(1) if block else ""
        if re.search(r"^\s*-\s+path:", section_text, flags=re.MULTILINE):
            if not re.search(r"^\s+alt:\s+\".+\"", section_text, flags=re.MULTILINE):
                errors.append(f"{section} entries must include alt text")
            if section == "generated_figures" and not re.search(r"^\s+prompt:\s+\|", section_text, flags=re.MULTILINE):
                errors.append("generated_figures entries must include the final image prompt")

    has_mermaid = bool(re.search(r"```mermaid\s", body))
    has_local_image = bool(re.search(r"!\[[^\]]+\]\((?!https?://)[^)]+\)", body))
    has_liquid_figure = bool(re.search(r"{%\s*include\s+figure\.liquid\b", body))
    if not (has_mermaid or has_local_image or has_liquid_figure):
        errors.append("post must include an original local visual asset or Mermaid diagram")

    return errors


def validate(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    try:
        front_matter, body = split_front_matter(text)
    except ValueError as exc:
        return [str(exc)], warnings

    keys = front_matter_keys(front_matter)
    missing = sorted(REQUIRED_FRONT_MATTER - keys)
    if missing:
        errors.append(f"missing front matter keys: {', '.join(missing)}")

    layout = front_matter_value(front_matter, "layout")
    if layout != "distill":
        warnings.append("layout is not distill; math-heavy tutorial drafts should usually use distill")

    for section in REQUIRED_SECTIONS:
        if not re.search(rf"^##\s+{re.escape(section)}\s*$", body, re.MULTILINE):
            errors.append(f"missing required section: {section}")
    errors.extend(section_order_errors(body))

    for section in FORBIDDEN_SECTION_NAMES:
        if re.search(rf"^##\s+{re.escape(section)}\s*$", body, re.MULTILINE):
            errors.append(f"forbidden generic section name: {section}")

    if not has_visual(body):
        errors.append("missing visual content: add Mermaid, image, Plotly, Vega-Lite, or ECharts")

    if not re.search(r"https?://", text):
        errors.append("missing external source or citation link")

    errors.extend(image_alt_errors(body))
    errors.extend(markdown_image_errors(body))
    errors.extend(liquid_figure_errors(body))
    errors.extend(visual_plan_errors(front_matter, body))

    visible_body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    body_without_code = re.sub(r"```.*?```", "", visible_body, flags=re.DOTALL)
    for pattern in BANNED_PATTERNS:
        if re.search(pattern, body_without_code, flags=re.IGNORECASE):
            errors.append(f"human voice check failed: banned phrase matched /{pattern}/")

    if is_post_path(path):
        publish_ready = front_matter_value(front_matter, "publish_ready")
        draft_stage = front_matter_value(front_matter, "draft_stage")
        if publish_ready != "true":
            errors.append("_posts entries must set publish_ready: true")
        if draft_stage != "published":
            errors.append('_posts entries must set draft_stage: "published"')
        if re.search(r"\b(TODO|FIXME|Checkpoint draft|scaffold)\b", body, flags=re.IGNORECASE):
            errors.append("_posts entries must not contain draft placeholders")
        errors.extend(local_asset_errors(front_matter_value(front_matter, "thumbnail"), "thumbnail"))
    else:
        if front_matter_value(front_matter, "publish_ready") == "true":
            warnings.append("draft has publish_ready: true but is not in _posts")

    return errors, warnings


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("Usage: check_post.py <draft-or-post>", file=sys.stderr)
        return 2

    path = Path(argv[0])
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        print(f"check_post: file not found: {path}", file=sys.stderr)
        return 2

    errors, warnings = validate(path)
    rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
    for warning in warnings:
        print(f"[blog-check] warning: {warning}")
    if errors:
        for error in errors:
            print(f"[blog-check] error: {error}", file=sys.stderr)
        print(f"[blog-check] failed: {rel}", file=sys.stderr)
        return 1

    print(f"[blog-check] passed: {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
