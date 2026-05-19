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


def scale_point(x: float, y: float, width: int, height: int) -> tuple[float, float]:
    sx = 58.0 + (x + 4.2) / 8.4 * (width - 116.0)
    sy = height - (52.0 + (y + 3.2) / 6.4 * (height - 112.0))
    return sx, sy


def unit(v: tuple[float, float]) -> tuple[float, float]:
    norm = math.sqrt(v[0] * v[0] + v[1] * v[1])
    if norm < 1e-12:
        return 0.0, 0.0
    return v[0] / norm, v[1] / norm


def arrow(
    start: tuple[float, float],
    vector: tuple[float, float],
    width: int,
    height: int,
    length: float,
    stroke: str,
    stroke_width: float,
    opacity: float,
) -> str:
    direction = unit(vector)
    end = (start[0] + length * direction[0], start[1] + length * direction[1])
    sx, sy = scale_point(start[0], start[1], width, height)
    ex, ey = scale_point(end[0], end[1], width, height)
    angle = math.atan2(ey - sy, ex - sx)
    head = 8.0 + stroke_width
    left = (ex - head * math.cos(angle - 0.45), ey - head * math.sin(angle - 0.45))
    right = (ex - head * math.cos(angle + 0.45), ey - head * math.sin(angle + 0.45))
    return (
        f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
        f'stroke="{stroke}" stroke-width="{stroke_width:.1f}" opacity="{opacity:.2f}" stroke-linecap="round"/>'
        f'<path d="M {left[0]:.1f} {left[1]:.1f} L {ex:.1f} {ey:.1f} L {right[0]:.1f} {right[1]:.1f}" '
        f'fill="none" stroke="{stroke}" stroke-width="{stroke_width:.1f}" opacity="{opacity:.2f}" stroke-linecap="round"/>'
    )


def circle(x: float, y: float, radius: float, fill: str, opacity: float, width: int, height: int) -> str:
    sx, sy = scale_point(x, y, width, height)
    return f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{radius:.1f}" fill="{fill}" opacity="{opacity:.2f}"/>'


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
    target_rng = random.Random(41)
    source_rng = random.Random(43)
    target_points = [data_sample(target_rng) for _ in range(130)]
    source_points = [source_sample(source_rng) for _ in range(90)]
    width, height = 920, 640
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Conditional endpoint velocity arrows averaged into a marginal direction">',
        '<rect width="100%" height="100%" fill="#fbfbf8"/>',
        '<text x="58" y="38" font-family="Arial, sans-serif" font-size="23" font-weight="700" fill="#222">Conditional arrows near one point average into a marginal direction</text>',
        '<text x="58" y="62" font-family="Arial, sans-serif" font-size="14" fill="#555">Fixed time t = 0.55; arrows come from endpoint pairs whose interpolated point lies near the marked query location.</text>',
    ]
    for x, y in source_points:
        parts.append(circle(x, y, 2.0, "#333333", 0.15, width, height))
    for x, y in target_points:
        parts.append(circle(x, y, 2.2, "#d95f59", 0.22, width, height))
    for idx, row in enumerate(selected):
        xt = row["xt"]  # type: ignore[assignment]
        velocity = row["velocity"]  # type: ignore[assignment]
        jitter = (0.06 * math.cos(idx * 1.7), 0.06 * math.sin(idx * 1.7))
        start = (xt[0] + jitter[0], xt[1] + jitter[1])  # type: ignore[index]
        parts.append(arrow(start, velocity, width, height, 0.58, "#8d8d8d", 1.4, 0.62))
        parts.append(circle(start[0], start[1], 1.8, "#777777", 0.35, width, height))
    parts.append(circle(query[0], query[1], 6.0, "#111111", 0.95, width, height))
    parts.append(arrow(query, avg, width, height, 1.05, "#238b8d", 4.0, 0.95))
    qx, qy = scale_point(query[0], query[1], width, height)
    parts.append(f'<text x="{qx + 14:.1f}" y="{qy - 11:.1f}" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#222">query (x,t)</text>')
    parts.append(f'<text x="{qx + 14:.1f}" y="{qy + 9:.1f}" font-family="Arial, sans-serif" font-size="13" fill="#238b8d">averaged direction</text>')
    parts.extend(
        [
            '<rect x="58" y="546" width="560" height="54" rx="0" fill="#ffffff" stroke="#ddd"/>',
            '<text x="74" y="570" font-family="Arial, sans-serif" font-size="13" fill="#444">gray: conditional velocities from sampled endpoint pairs near the same x_t</text>',
            '<text x="74" y="590" font-family="Arial, sans-serif" font-size="13" fill="#444">teal: empirical average used as a local marginal-field estimate</text>',
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
        "nearest_radius": max(float(row["dist"]) for row in selected),
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
