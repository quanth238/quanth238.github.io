#!/usr/bin/env python3
"""Generate probability-path family snapshots for Flow Matching Part 5."""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ASSET_DIR = ROOT / "assets/img/blog/flow-matching-guide"
DEFAULT_RUN_DIR = ROOT / "_blog_work/flow-matching-guide/remote_runs/fm07_path_families"


Point = tuple[float, float]


def randn(rng: random.Random) -> float:
    u1 = max(rng.random(), 1e-12)
    u2 = rng.random()
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


def source_sample(rng: random.Random) -> Point:
    return randn(rng), randn(rng)


def data_sample(rng: random.Random) -> Point:
    center = rng.choice([(-2.1, -0.8), (2.1, 0.8)])
    return center[0] + 0.32 * randn(rng), center[1] + 0.32 * randn(rng)


def cond_ot(x0: Point, x1: Point, t: float) -> tuple[Point, Point]:
    xt = ((1.0 - t) * x0[0] + t * x1[0], (1.0 - t) * x0[1] + t * x1[1])
    velocity = (x1[0] - x0[0], x1[1] - x0[1])
    return xt, velocity


def linear_vp(x0: Point, x1: Point, t: float) -> tuple[Point, Point]:
    sigma = math.sqrt(max(1.0 - t * t, 1e-8))
    xt = (sigma * x0[0] + t * x1[0], sigma * x0[1] + t * x1[1])
    sigma_dot = -t / sigma
    velocity = (x1[0] + sigma_dot * x0[0], x1[1] + sigma_dot * x0[1])
    return xt, velocity


def scale_point(x: float, y: float, left: float, top: float, width: float, height: float) -> Point:
    sx = left + (x + 4.2) / 8.4 * width
    sy = top + height - (y + 3.1) / 6.2 * height
    return sx, sy


def color_for_mag(mag: float, max_mag: float) -> str:
    ratio = min(max(mag / max_mag, 0.0), 1.0)
    r = int(47 + ratio * (217 - 47))
    g = int(111 + ratio * (95 - 111))
    b = int(143 + ratio * (89 - 143))
    return f"#{r:02x}{g:02x}{b:02x}"


def panel(
    label: str,
    samples: list[Point],
    left: float,
    top: float,
    width: float,
    height: float,
    fill: str,
) -> list[str]:
    parts = [
        f'<rect x="{left:.1f}" y="{top:.1f}" width="{width:.1f}" height="{height:.1f}" fill="#fff" stroke="#ddd"/>',
        f'<text x="{left + 10:.1f}" y="{top + 19:.1f}" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#222">{label}</text>',
        f'<line x1="{left + width - 52:.1f}" y1="{top + height - 20:.1f}" x2="{left + width - 18:.1f}" y2="{top + height - 20:.1f}" stroke="#9a9a9a" stroke-width="1.0" opacity="0.55"/>',
        f'<line x1="{left + width - 52:.1f}" y1="{top + height - 20:.1f}" x2="{left + width - 52:.1f}" y2="{top + height - 48:.1f}" stroke="#9a9a9a" stroke-width="1.0" opacity="0.55"/>',
    ]
    for x, y in samples:
        sx, sy = scale_point(x, y, left + 8, top + 26, width - 16, height - 34)
        parts.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="1.9" fill="{fill}" opacity="0.35"/>')
    return parts


def magnitude_row(
    label: str,
    magnitudes: list[float],
    left: float,
    top: float,
    width: float,
    max_mag: float,
) -> list[str]:
    parts = [
        f'<text x="{left:.1f}" y="{top + 14:.1f}" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#222">{label}</text>',
    ]
    bar_w = width / len(magnitudes)
    for i, mag in enumerate(magnitudes):
        x = left + i * bar_w
        h = 68 * mag / max_mag
        parts.append(f'<rect x="{x + 8:.1f}" y="{top + 92 - h:.1f}" width="{bar_w - 16:.1f}" height="{h:.1f}" fill="{color_for_mag(mag, max_mag)}" opacity="0.82"/>')
        parts.append(f'<text x="{x + 12:.1f}" y="{top + 110:.1f}" font-family="Arial, sans-serif" font-size="11" fill="#555">{mag:.2f}</text>')
    return parts


def build(run_dir: Path) -> dict[str, object]:
    rng = random.Random(73)
    pairs = [(source_sample(rng), data_sample(rng)) for _ in range(240)]
    times = [0.0, 0.33, 0.66, 0.9]
    families = [
        ("Conditional OT", cond_ot, "#2f6f8f"),
        ("Linear VP", linear_vp, "#238b8d"),
    ]
    width, height = 1180, 760
    panel_w, panel_h = 240, 180
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Probability path snapshots comparing Conditional OT and Linear VP schedules">',
        '<rect width="100%" height="100%" fill="#fbfbf8"/>',
        '<text x="54" y="38" font-family="Arial, sans-serif" font-size="24" font-weight="700" fill="#222">Same endpoints, different probability paths</text>',
        '<text x="54" y="62" font-family="Arial, sans-serif" font-size="14" fill="#555">All eight snapshots share the same x-y scale; only the scheduler changes between rows.</text>',
    ]
    metrics: dict[str, object] = {}
    all_mags: list[float] = []
    for row, (name, path_fn, color) in enumerate(families):
        y = 92 + row * 222
        parts.append(f'<text x="54" y="{y - 12:.1f}" font-family="Arial, sans-serif" font-size="17" font-weight="700" fill="#222">{name}</text>')
        mags: list[float] = []
        for col, t in enumerate(times):
            samples: list[Point] = []
            velocities: list[Point] = []
            for x0, x1 in pairs:
                xt, velocity = path_fn(x0, x1, t)
                samples.append(xt)
                velocities.append(velocity)
            mag = sum(math.sqrt(v[0] * v[0] + v[1] * v[1]) for v in velocities) / len(velocities)
            mags.append(mag)
            all_mags.append(mag)
            x = 54 + col * (panel_w + 28)
            parts.extend(panel(f"t={t:.2f}", samples, x, y, panel_w, panel_h, color))
        metrics[name] = {"mean_velocity_magnitude": dict(zip([str(t) for t in times], mags))}
    max_mag = max(all_mags)
    parts.append('<text x="54" y="560" font-family="Arial, sans-serif" font-size="17" font-weight="700" fill="#222">Mean conditional velocity magnitude</text>')
    parts.extend(magnitude_row("Conditional OT", list(metrics["Conditional OT"]["mean_velocity_magnitude"].values()), 54, 584, 500, max_mag))  # type: ignore[index, union-attr]
    parts.extend(magnitude_row("Linear VP", list(metrics["Linear VP"]["mean_velocity_magnitude"].values()), 604, 584, 500, max_mag))  # type: ignore[index, union-attr]
    parts.append('<text x="54" y="730" font-family="Arial, sans-serif" font-size="13" fill="#444">The Linear VP schedule keeps more noise at middle times and has larger late-time velocity magnitudes in this toy draw.</text>')
    parts.append("</svg>\n")
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    run_dir.mkdir(parents=True, exist_ok=True)
    figure_path = ASSET_DIR / "flow-matching-path-family-snapshots.svg"
    figure_path.write_text("\n".join(parts), encoding="utf-8")
    payload: dict[str, object] = {
        "task": "FM-07",
        "seed": 73,
        "times": times,
        "families": {
            "conditional_ot": {"alpha": "t", "sigma": "1-t"},
            "linear_vp": {"alpha": "t", "sigma": "sqrt(1-t^2)"},
        },
        "metrics": metrics,
        "visual_encoding": {
            "same_endpoint_pairs": True,
            "same_axes_across_snapshots": True,
            "same_axes_cue": "shared-axis note in subtitle plus repeated L-shaped axis glyphs",
            "paper_figure_extraction": False,
        },
        "asset": str(figure_path.relative_to(ROOT)),
    }
    (run_dir / "path_family_metrics.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (run_dir / "README.md").write_text(
        "# FM-07 Path Family Snapshots\n\n"
        "Deterministic pure-Python comparison of two Flow Matching Guide affine schedulers: Conditional OT and Linear VP. The figure uses the same endpoint pairs and reports mean conditional velocity magnitude at matched times.\n",
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
