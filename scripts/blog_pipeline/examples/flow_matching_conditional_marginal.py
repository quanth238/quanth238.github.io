#!/usr/bin/env python3
"""Generate the Part 3 conditional-to-marginal arrow figure."""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ASSET_DIR = ROOT / "assets/img/blog/flow-matching-guide"
DEFAULT_RUN_DIR = ROOT / "_blog_work/flow-matching-guide/remote_runs/fm05_conditional_marginal"


def randn(rng: random.Random) -> float:
    u1 = max(rng.random(), 1e-12)
    u2 = rng.random()
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


def source_sample(rng: random.Random) -> tuple[float, float]:
    return randn(rng), randn(rng)


def data_sample(rng: random.Random) -> tuple[float, float]:
    center = rng.choice([(-2.0, -0.8), (2.0, 0.8)])
    return center[0] + 0.35 * randn(rng), center[1] + 0.35 * randn(rng)


def interpolate(x0: tuple[float, float], x1: tuple[float, float], t: float) -> tuple[float, float]:
    return (1.0 - t) * x0[0] + t * x1[0], (1.0 - t) * x0[1] + t * x1[1]


def scale_point(
    x: float,
    y: float,
    left: float,
    top: float,
    width: float,
    height: float,
    domain: tuple[float, float, float, float],
) -> tuple[float, float]:
    xmin, xmax, ymin, ymax = domain
    sx = left + (x - xmin) / (xmax - xmin) * width
    sy = top + height - (y - ymin) / (ymax - ymin) * height
    return sx, sy


def unit(v: tuple[float, float]) -> tuple[float, float]:
    norm = math.sqrt(v[0] * v[0] + v[1] * v[1])
    if norm < 1e-12:
        return 0.0, 0.0
    return v[0] / norm, v[1] / norm


def arrow(
    start: tuple[float, float],
    vector: tuple[float, float],
    left: float,
    top: float,
    width: float,
    height: float,
    domain: tuple[float, float, float, float],
    length: float,
    stroke: str,
    stroke_width: float,
    opacity: float,
    dash: str | None = None,
) -> str:
    direction = unit(vector)
    end = (start[0] + length * direction[0], start[1] + length * direction[1])
    sx, sy = scale_point(start[0], start[1], left, top, width, height, domain)
    ex, ey = scale_point(end[0], end[1], left, top, width, height, domain)
    angle = math.atan2(ey - sy, ex - sx)
    head = 8.0 + stroke_width
    left = (ex - head * math.cos(angle - 0.45), ey - head * math.sin(angle - 0.45))
    right = (ex - head * math.cos(angle + 0.45), ey - head * math.sin(angle + 0.45))
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
        f'stroke="{stroke}" stroke-width="{stroke_width:.1f}" opacity="{opacity:.2f}" stroke-linecap="round"{dash_attr}/>'
        f'<path d="M {left[0]:.1f} {left[1]:.1f} L {ex:.1f} {ey:.1f} L {right[0]:.1f} {right[1]:.1f}" '
        f'fill="none" stroke="{stroke}" stroke-width="{stroke_width:.1f}" opacity="{opacity:.2f}" stroke-linecap="round"{dash_attr}/>'
    )


def circle(
    x: float,
    y: float,
    radius: float,
    fill: str,
    opacity: float,
    left: float,
    top: float,
    width: float,
    height: float,
    domain: tuple[float, float, float, float],
    stroke: str | None = None,
    stroke_width: float = 1.0,
) -> str:
    sx, sy = scale_point(x, y, left, top, width, height, domain)
    stroke_attr = f' stroke="{stroke}" stroke-width="{stroke_width:.1f}"' if stroke else ""
    return f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{radius:.1f}" fill="{fill}" opacity="{opacity:.2f}"{stroke_attr}/>'


def radius_circle(
    x: float,
    y: float,
    radius_data: float,
    left: float,
    top: float,
    width: float,
    height: float,
    domain: tuple[float, float, float, float],
    stroke: str,
    fill: str,
    opacity: float,
) -> str:
    sx, sy = scale_point(x, y, left, top, width, height, domain)
    xmin, xmax, _, _ = domain
    radius_px = radius_data / (xmax - xmin) * width
    return (
        f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{radius_px:.1f}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1.8" opacity="{opacity:.2f}"/>'
    )


def panel_frame(left: float, top: float, width: float, height: float, label: str, subtitle: str) -> list[str]:
    return [
        f'<rect x="{left:.1f}" y="{top:.1f}" width="{width:.1f}" height="{height:.1f}" fill="#ffffff" stroke="#d8d8d8"/>',
        f'<text x="{left + 14:.1f}" y="{top + 24:.1f}" font-family="Arial, sans-serif" font-size="15" font-weight="700" fill="#222">{label}</text>',
        f'<text x="{left + 14:.1f}" y="{top + 44:.1f}" font-family="Arial, sans-serif" font-size="12" fill="#555">{subtitle}</text>',
    ]


def build(run_dir: Path) -> dict[str, object]:
    rng = random.Random(37)
    t = 0.55
    query = (0.05, 0.00)
    candidates: list[dict[str, object]] = []
    for _ in range(5000):
        x0 = source_sample(rng)
        x1 = data_sample(rng)
        xt = interpolate(x0, x1, t)
        velocity = (x1[0] - x0[0], x1[1] - x0[1])
        dist = math.sqrt((xt[0] - query[0]) ** 2 + (xt[1] - query[1]) ** 2)
        candidates.append({"x0": x0, "x1": x1, "xt": xt, "velocity": velocity, "dist": dist})
    selected = sorted(candidates, key=lambda row: float(row["dist"]))[:26]
    avg = (
        sum(row["velocity"][0] for row in selected) / len(selected),  # type: ignore[index]
        sum(row["velocity"][1] for row in selected) / len(selected),  # type: ignore[index]
    )
    midpoint_cloud = [row["xt"] for row in candidates[::13]][:360]
    target_rng = random.Random(41)
    source_rng = random.Random(43)
    target_points = [data_sample(target_rng) for _ in range(90)]
    source_points = [source_sample(source_rng) for _ in range(70)]
    width, height = 1120, 680
    global_box = (58.0, 118.0, 470.0, 392.0)
    zoom_box = (608.0, 118.0, 454.0, 392.0)
    global_domain = (-4.2, 4.2, -3.2, 3.2)
    zoom_domain = (query[0] - 0.62, query[0] + 0.62, query[1] - 0.58, query[1] + 0.58)
    nearest_radius = max(float(row["dist"]) for row in selected)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Conditional endpoint velocity arrows averaged into an empirical local marginal-field estimate">',
        '<rect width="100%" height="100%" fill="#fbfbf8"/>',
        '<text x="58" y="38" font-family="Arial, sans-serif" font-size="23" font-weight="700" fill="#222">Local conditional arrows form an empirical field estimate</text>',
        '<text x="58" y="63" font-family="Arial, sans-serif" font-size="14" fill="#555">At t = 0.55, keep endpoint pairs whose interpolated point falls near the query, then average their velocities locally.</text>',
    ]
    parts.extend(panel_frame(*global_box, "A. Select endpoint pairs near the query", "Global view of interpolated points at the fixed time."))
    parts.extend(panel_frame(*zoom_box, "B. Average the nearby conditional directions", "Zoomed query neighborhood; arrow lengths are scaled for readability."))
    left, top, plot_w, plot_h = global_box
    for x, y in midpoint_cloud:
        parts.append(circle(x, y, 1.8, "#9b9b9b", 0.22, left + 12, top + 56, plot_w - 24, plot_h - 76, global_domain))
    for idx, row in enumerate(selected):
        xt = row["xt"]  # type: ignore[assignment]
        parts.append(circle(xt[0], xt[1], 3.2, "#444444", 0.62, left + 12, top + 56, plot_w - 24, plot_h - 76, global_domain))  # type: ignore[index]
    for x, y in source_points:
        parts.append(circle(x, y, 1.7, "#333333", 0.14, left + 12, top + 56, plot_w - 24, plot_h - 76, global_domain))
    for x, y in target_points:
        parts.append(circle(x, y, 2.0, "#d95f59", 0.20, left + 12, top + 56, plot_w - 24, plot_h - 76, global_domain))
    parts.append(radius_circle(query[0], query[1], nearest_radius, left + 12, top + 56, plot_w - 24, plot_h - 76, global_domain, "#238b8d", "#238b8d", 0.18))
    parts.append(circle(query[0], query[1], 5.5, "#111111", 0.95, left + 12, top + 56, plot_w - 24, plot_h - 76, global_domain))
    qx, qy = scale_point(query[0], query[1], left + 12, top + 56, plot_w - 24, plot_h - 76, global_domain)
    parts.append(f'<text x="{qx + 12:.1f}" y="{qy - 12:.1f}" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#222">query (x,t)</text>')

    left, top, plot_w, plot_h = zoom_box
    parts.append(radius_circle(query[0], query[1], nearest_radius, left + 18, top + 58, plot_w - 36, plot_h - 80, zoom_domain, "#238b8d", "#238b8d", 0.16))
    for idx, row in enumerate(selected):
        xt = row["xt"]  # type: ignore[assignment]
        velocity = row["velocity"]  # type: ignore[assignment]
        jitter = (0.018 * math.cos(idx * 1.7), 0.018 * math.sin(idx * 1.7))
        start = (xt[0] + jitter[0], xt[1] + jitter[1])  # type: ignore[index]
        parts.append(arrow(start, velocity, left + 18, top + 58, plot_w - 36, plot_h - 80, zoom_domain, 0.28, "#777777", 1.5, 0.62))
        parts.append(circle(start[0], start[1], 2.0, "#777777", 0.42, left + 18, top + 58, plot_w - 36, plot_h - 80, zoom_domain))
    parts.append(circle(query[0], query[1], 6.2, "#111111", 0.95, left + 18, top + 58, plot_w - 36, plot_h - 80, zoom_domain))
    parts.append(arrow(query, avg, left + 18, top + 58, plot_w - 36, plot_h - 80, zoom_domain, 0.46, "#238b8d", 4.2, 0.96))
    qx, qy = scale_point(query[0], query[1], left + 18, top + 58, plot_w - 36, plot_h - 80, zoom_domain)
    parts.append(f'<text x="{qx + 15:.1f}" y="{qy - 12:.1f}" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#222">query (x,t)</text>')
    parts.append(f'<text x="{qx + 15:.1f}" y="{qy + 10:.1f}" font-family="Arial, sans-serif" font-size="13" fill="#238b8d">empirical local estimate</text>')
    parts.extend(
        [
            '<rect x="58" y="538" width="1004" height="84" rx="0" fill="#ffffff" stroke="#ddd"/>',
            '<circle cx="80" cy="562" r="4" fill="#444" opacity="0.70"/>',
            '<text x="96" y="567" font-family="Arial, sans-serif" font-size="13" fill="#444">black dots: the 26 nearest interpolated points among 5,000 sampled endpoint pairs</text>',
            '<line x1="68" y1="589" x2="91" y2="589" stroke="#777777" stroke-width="2.0" opacity="0.70" stroke-linecap="round"/>',
            '<text x="96" y="594" font-family="Arial, sans-serif" font-size="13" fill="#444">gray arrows: endpoint-conditioned velocity directions near the same local state</text>',
            '<line x1="68" y1="611" x2="91" y2="611" stroke="#238b8d" stroke-width="4.0" opacity="0.95" stroke-linecap="round"/>',
            '<text x="96" y="616" font-family="Arial, sans-serif" font-size="13" fill="#444">teal arrow: empirical local average, a finite-sample estimate rather than an exact marginal oracle</text>',
            "</svg>\n",
        ]
    )
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    run_dir.mkdir(parents=True, exist_ok=True)
    figure_path = ASSET_DIR / "flow-matching-conditional-marginal-arrows.svg"
    figure_path.write_text("\n".join(parts), encoding="utf-8")
    payload: dict[str, object] = {
        "task": "FM-05",
        "seed": 37,
        "time": t,
        "query": query,
        "candidate_pairs": len(candidates),
        "selected_pairs": len(selected),
        "average_velocity": avg,
        "nearest_radius": nearest_radius,
        "visual_encoding": {
            "layout": "two_panel_global_selection_and_zoom",
            "query_neighborhood_visible": True,
            "conditional_arrows": "gray normalized directions in zoom panel",
            "empirical_average": "teal local finite-sample estimate",
            "paper_figure_extraction": False,
        },
        "asset": str(figure_path.relative_to(ROOT)),
    }
    (run_dir / "conditional_marginal_metrics.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (run_dir / "README.md").write_text(
        "# FM-05 Conditional-To-Marginal Arrows\n\n"
        "Deterministic pure-Python figure for Flow Matching Part 3. It samples endpoint pairs, keeps pairs whose interpolated point is near one query location at a fixed time, and draws their endpoint-conditioned velocities plus the local empirical average.\n",
        encoding="utf-8",
    )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    args = parser.parse_args()
    print(json.dumps(build(args.run_dir), indent=2))


if __name__ == "__main__":
    main()
