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
    "Path and velocity target",
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
    "Core construction",
]
BANNED_PATTERNS = [
    r"\bcheckpoint draft\b",
    r"\bthis file is a scaffold\b",
    r"\bconcise tutorial note that connects\b",
    r"\bthis tutorial explains\b",
    r"\bthis post explains\b",
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
    r"\bpart 1 established\b",
    r"\bthe remaining question is\b",
    r"\bnot a production implementation\b",
    r"\bfor provenance\b",
    r"\bfigure provenance\b",
    r"\bprompt provenance\b",
]
SCHOLARLY_SOURCE_RE = re.compile(
    r"(arxiv\.org|doi\.org|openreview\.net|semanticscholar\.org|aclanthology\.org|"
    r"proceedings\.mlr\.press|neurips\.cc|icml\.cc|openaccess\.thecvf\.com|"
    r"\.pdf(?:$|[?#]))",
    flags=re.IGNORECASE,
)


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


def front_matter_list(front_matter: str, key: str) -> list[str]:
    lines = front_matter.splitlines()
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


def is_post_path(path: Path) -> bool:
    return "_posts" in path.parts or bool(re.match(r"\d{4}-\d{2}-\d{2}-", path.name))


def has_visual(body: str) -> bool:
    return bool(
        re.search(r"```mermaid\s", body)
        or re.search(r"!\[[^\]]+\]\([^)]+\)", body)
        or re.search(r"{%\s*include\s+figure\.liquid\b", body)
        or re.search(r"```(?:plotly|vega_lite|echarts)\s", body)
    )


def attribute_value(text: str, attr: str) -> str | None:
    pattern = re.compile(rf"\b{re.escape(attr)}\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s>]+))")
    match = pattern.search(text)
    if not match:
        return None
    return next(value for value in match.groups() if value is not None)


def image_alt_errors(body: str) -> list[str]:
    errors: list[str] = []
    for match in re.finditer(r"!\[([^\]]*)\]\(([^)]+)\)", body):
        if not match.group(1).strip():
            errors.append(f"image {match.group(2)} is missing alt text")
    for match in re.finditer(r"{%\s*include\s+figure\.liquid\b([^%]*)%}", body):
        include = match.group(1)
        alt = attribute_value(include, "alt")
        if alt is None or not alt.strip():
            errors.append("figure include is missing alt text")
    for match in re.finditer(r"<img\b([^>]*)>", body, flags=re.IGNORECASE):
        tag = match.group(1)
        src = attribute_value(tag, "src") or "<unknown>"
        alt = attribute_value(tag, "alt")
        if alt is None or not alt.strip():
            errors.append(f"HTML image {src} is missing alt text")
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
        target = attribute_value(include, "path")
        if not target:
            continue
        if re.match(r"https?://", target):
            errors.append(f"external figure hotlink is not allowed: {target}")
            continue
        local_path = ROOT / target.lstrip("/")
        if not local_path.exists():
            errors.append(f"local figure does not exist: {target}")
    return errors


def html_image_errors(body: str) -> list[str]:
    errors: list[str] = []
    for match in re.finditer(r"<img\b([^>]*)>", body, flags=re.IGNORECASE):
        tag = match.group(1)
        target = attribute_value(tag, "src")
        if not target:
            errors.append("HTML image is missing src")
            continue
        if re.match(r"https?://", target):
            errors.append(f"external HTML image hotlink is not allowed: {target}")
            continue
        if target.startswith(("#", "mailto:", "data:")):
            continue
        local = target.split("#", 1)[0].split("?", 1)[0]
        local_path = ROOT / local.lstrip("/")
        if not local_path.exists():
            errors.append(f"local HTML image does not exist: {target}")
    return errors


def mermaid_accessibility_errors(body: str) -> list[str]:
    errors: list[str] = []
    for index, block in enumerate(
        re.findall(r"```mermaid\s*\n(.*?)```", body, flags=re.DOTALL),
        start=1,
    ):
        if not re.search(r"^\s*accTitle:\s+\S", block, flags=re.MULTILINE):
            errors.append(
                f"Mermaid diagram {index} is missing accTitle. "
                "WHY: accessible titles make visual checks recoverable across sessions. "
                "FIX: add an accTitle line near the top of the Mermaid block."
            )
        if not re.search(r"^\s*accDescr:\s+\S", block, flags=re.MULTILINE):
            errors.append(
                f"Mermaid diagram {index} is missing accDescr. "
                "WHY: diagrams need a short text description for accessibility and review. "
                "FIX: add an accDescr line near the top of the Mermaid block."
            )
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


def source_material_errors(front_matter: str) -> list[str]:
    sources = front_matter_list(front_matter, "source_materials")
    scholarly_sources = sorted({source for source in sources if SCHOLARLY_SOURCE_RE.search(source)})
    if len(sources) < 2:
        return ["source_materials should include the primary source plus at least one supporting reference"]
    if len(scholarly_sources) < 2:
        return ["source_materials should include at least two scholarly/core sources such as arXiv, DOI, OpenReview, PMLR, CVF, or PDFs"]
    return []


def reference_link_errors(body: str) -> list[str]:
    errors: list[str] = []
    reference_body = section_body(body, "References and visual resources")
    if not reference_body:
        return errors

    links = re.findall(r"https?://[^\s)>\"]+", reference_body)
    distinct_links = sorted(set(links))
    scholarly_links = sorted({link for link in distinct_links if SCHOLARLY_SOURCE_RE.search(link)})
    if len(distinct_links) < 3:
        errors.append("References and visual resources should include at least three cited external references")
    if len(scholarly_links) < 2:
        errors.append("References and visual resources should include at least two scholarly/core paper links")
    return errors


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


def section_body(body: str, section: str) -> str:
    match = re.search(rf"^##\s+{re.escape(section)}\s*$", body, re.MULTILINE)
    if not match:
        return ""
    next_match = re.search(r"^##\s+.+$", body[match.end() :], re.MULTILINE)
    end = match.end() + next_match.start() if next_match else len(body)
    return body[match.end() : end].strip()


def yaml_section(text: str, section: str) -> str:
    match = re.search(rf"^{re.escape(section)}:\s*(?:\[\])?\s*$", text, flags=re.MULTILINE)
    if not match:
        return ""
    next_match = re.search(r"^[a-z_]+:\s*(?:\[\])?\s*$", text[match.end() :], flags=re.MULTILINE)
    end = match.end() + next_match.start() if next_match else len(text)
    return text[match.end() : end].strip()


def display_math_errors(body: str) -> list[str]:
    errors: list[str] = []
    for block in re.findall(r"\$\$(.*?)\$\$", body, flags=re.DOTALL):
        if r"\qquad" in block or r"\quad" in block:
            errors.append("display math should not use \\quad/\\qquad; split side conditions into prose")
        for line in block.splitlines():
            stripped = line.strip()
            if len(stripped) > 100:
                errors.append("display math line is too long; split it to avoid horizontal scroll")
                break
    return errors


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

    if "visual_contract:" not in plan:
        errors.append(
            "visual plan is missing visual_contract. "
            "WHY: professional figures need a durable quality contract, not only asset paths. "
            "FIX: add visual_contract to the plan or recreate it with new_series.py."
        )
    if "quality_gate:" not in plan:
        errors.append(
            "visual plan is missing quality_gate. "
            "WHY: the Evaluator role needs an explicit visual review checkpoint. "
            "FIX: add quality_gate with required_before_publish and evaluator_status."
        )
    if "evaluator_notes:" not in plan:
        errors.append(
            "visual plan is missing evaluator_notes. "
            "WHY: review decisions should survive context resets and new sessions. "
            "FIX: add evaluator_notes with any visual risks, approvals, or redesign tasks."
        )

    body_local_assets: set[str] = set()
    for match in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", body):
        target = match.group(1).strip()
        if not re.match(r"https?://", target) and not target.startswith(("#", "mailto:", "data:")):
            body_local_assets.add(target.split("#", 1)[0].split("?", 1)[0].lstrip("/"))
    for match in re.finditer(r"{%\s*include\s+figure\.liquid\b([^%]*)%}", body):
        target = attribute_value(match.group(1), "path")
        if target and not re.match(r"https?://", target):
            body_local_assets.add(target.split("#", 1)[0].split("?", 1)[0].lstrip("/"))
    for match in re.finditer(r"<img\b([^>]*)>", body, flags=re.IGNORECASE):
        target = attribute_value(match.group(1), "src")
        if target and not re.match(r"https?://", target) and not target.startswith(("#", "mailto:", "data:")):
            body_local_assets.add(target.split("#", 1)[0].split("?", 1)[0].lstrip("/"))
    for asset in sorted(body_local_assets):
        if asset and asset not in plan:
            errors.append(
                f"reader-facing asset is not registered in visual plan: {asset}. "
                "WHY: figure provenance, alt text, and evaluator status must survive new sessions. "
                "FIX: add the asset under generated_figures or remote_code_figures in the visual plan."
            )

    references_text = yaml_section(plan, "references")
    source_count = len(re.findall(r"^\s*-\s+source:\s+\"?https?://", references_text, flags=re.MULTILINE))
    if source_count < 2:
        errors.append("visual plan must include at least two external visual/blog references")

    figure_briefs_text = yaml_section(plan, "figure_briefs")
    brief_count = len(re.findall(r"^\s*-\s+id:\s+", figure_briefs_text, flags=re.MULTILINE))
    if brief_count < 1:
        errors.append(
            "visual plan is missing figure_briefs. "
            "WHY: a figure brief forces Planner and Generator to decide what a figure teaches before drawing it. "
            "FIX: add a figure_briefs entry with id, kind, reader_question, purpose, must_show, avoid, cited_inspirations, and status."
        )
    for list_key in ("must_show", "avoid", "cited_inspirations"):
        if brief_count and not re.search(rf"^\s+{list_key}:\s*$", figure_briefs_text, flags=re.MULTILINE):
            errors.append(f"figure_briefs entries must include {list_key} items")
    for key in ("kind", "reader_question", "purpose", "status"):
        if brief_count and not re.search(rf"^\s+{key}:\s+\S", figure_briefs_text, flags=re.MULTILINE):
            errors.append(f"figure_briefs entries must include {key}")

    for path in re.findall(r"^\s*-\s+path:\s+\"([^\"]+)\"", plan, flags=re.MULTILINE):
        if re.match(r"https?://", path):
            errors.append(f"visual plan path must be local, not external: {path}")
            continue
        if not (ROOT / path.lstrip("/")).exists():
            errors.append(f"visual plan local asset does not exist: {path}")

    for section in ("generated_figures", "remote_code_figures"):
        section_text = yaml_section(plan, section)
        if re.search(r"^\s*-\s+path:", section_text, flags=re.MULTILINE):
            alt_values = [
                match.group(1).strip().strip('"').strip("'")
                for match in re.finditer(r"^\s+alt:\s+(.+)$", section_text, flags=re.MULTILINE)
            ]
            if not alt_values or any(not alt for alt in alt_values):
                errors.append(f"{section} entries must include alt text")
            if section == "generated_figures" and not re.search(r"^\s+prompt:\s+\|", section_text, flags=re.MULTILINE):
                errors.append("generated_figures entries must include the final image prompt")
            if section == "generated_figures" and "inspiration_sources:" not in section_text:
                errors.append("generated_figures entries must include cited inspiration_sources")

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
    errors.extend(display_math_errors(body))
    errors.extend(source_material_errors(front_matter))
    errors.extend(reference_link_errors(body))

    next_part = section_body(body, "Next part")
    if next_part and len(re.findall(r"\b[\w'-]+\b", next_part)) > 25:
        errors.append("Next part section should be concise: keep it to 25 words or fewer")

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
    errors.extend(html_image_errors(body))
    errors.extend(mermaid_accessibility_errors(body))
    errors.extend(visual_plan_errors(front_matter, body))

    visible_body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    body_without_code = re.sub(r"```.*?```", "", visible_body, flags=re.DOTALL)
    voice_text = front_matter + "\n" + body_without_code
    for pattern in BANNED_PATTERNS:
        if re.search(pattern, voice_text, flags=re.IGNORECASE):
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
