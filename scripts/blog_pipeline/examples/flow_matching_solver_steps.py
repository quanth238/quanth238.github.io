#!/usr/bin/env python3
"""Generate the Part 2 solver-step sweep for the Flow Matching series."""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ASSET_DIR = ROOT / "assets/img/blog/flow-matching-guide"
DEFAULT_RUN_DIR = ROOT / "_blog_work/flow-matching-guide/remote_runs/fm04_solver_steps"


def randn(rng: random.Random) -> float:
    u1 = max(rng.random(), 1e-12)
    u2 = rng.random()
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


def source_sample(rng: random.Random) -> tuple[float, float]:
    return randn(rng), randn(rng)


def data_sample(rng: random.Random) -> tuple[float, float]:
    center = rng.choice([(-2.0, -0.8), (2.0, 0.8)])
    return center[0] + 0.35 * randn(rng), center[1] + 0.35 * randn(rng)


def features(x: tuple[float, float], t: float) -> tuple[float, float, float, float]:
    return x[0], x[1], t, 1.0


def predict(weights: list[list[float]], x: tuple[float, float], t: float) -> tuple[float, float]:
    feat = features(x, t)
    return (
        sum(weights[0][j] * feat[j] for j in range(4)),
        sum(weights[1][j] * feat[j] for j in range(4)),
    )


def train(
    rng: random.Random,
    steps: int = 640,
    batch_size: int = 128,
    lr: float = 0.035,
) -> tuple[list[list[float]], list[float]]:
    weights = [[0.03 * randn(rng) for _ in range(4)] for _ in range(2)]
    losses: list[float] = []
    for step in range(steps):
        grad = [[0.0 for _ in range(4)] for _ in range(2)]
        loss = 0.0
        for _ in range(batch_size):
            x0 = source_sample(rng)
            x1 = data_sample(rng)
            t = rng.random()
            xt = ((1.0 - t) * x0[0] + t * x1[0], (1.0 - t) * x0[1] + t * x1[1])
            target = (x1[0] - x0[0], x1[1] - x0[1])
            pred = predict(weights, xt, t)
            feat = features(xt, t)
            for dim in range(2):
                err = pred[dim] - target[dim]
                loss += err * err / 2.0
                for j in range(4):
                    grad[dim][j] += err * feat[j] / batch_size
        for dim in range(2):
            for j in range(4):
                weights[dim][j] -= lr * grad[dim][j]
        if step % 20 == 0 or step == steps - 1:
            losses.append(loss / batch_size)
    return weights, losses


def integrate(
    weights: list[list[float]],
    x0: tuple[float, float],
    steps: int,
) -> list[tuple[float, float]]:
    x = x0
    path = [x]
    dt = 1.0 / steps
    for i in range(steps):
        t = i / steps
        v = predict(weights, x, t)
        x = (x[0] + dt * v[0], x[1] + dt * v[1])
        path.append(x)
    return path


def sq_distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def nearest_mode_distance(x: tuple[float, float]) -> float:
    modes = [(-2.0, -0.8), (2.0, 0.8)]
    return math.sqrt(min(sq_distance(x, mode) for mode in modes))


def scale_point(x: float, y: float, left: float, top: float, width: float, height: float) -> tuple[float, float]:
    sx = left + (x + 4.2) / 8.4 * width
    sy = top + height - (y + 3.2) / 6.4 * height
    return sx, sy


def svg_circle(cx: float, cy: float, radius: float, fill: str, opacity: float = 1.0) -> str:
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{radius:.1f}" fill="{fill}" opacity="{opacity:.2f}"/>'


def svg_polyline(points: list[tuple[float, float]], color: str, opacity: float, width: float = 1.4) -> str:
    coords = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="{width:.1f}" opacity="{opacity:.2f}"/>'


def write_sweep_svg(
    target_points: list[tuple[float, float]],
    paths_by_steps: dict[int, list[list[tuple[float, float]]]],
    metrics: list[dict[str, float]],
    path: Path,
) -> None:
    width, height = 1180, 760
    panel_w, panel_h = 500, 255
    panels = {
        4: (55.0, 80.0),
        8: (625.0, 80.0),
        16: (55.0, 405.0),
        32: (625.0, 405.0),
    }
    metric_by_step = {int(row["steps"]): row for row in metrics}
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Euler solver step sweep on a two-dimensional toy flow matching model">',
        '<rect width="100%" height="100%" fill="#fbfbf8"/>',
        '<text x="55" y="38" font-family="Arial, sans-serif" font-size="24" font-weight="700" fill="#222">Same learned field, different Euler step counts</text>',
        '<text x="55" y="62" font-family="Arial, sans-serif" font-size="14" fill="#555">Toy 2D diagnostic: black starts, blue trajectories, teal endpoints, vermillion target cloud</text>',
    ]
    for steps, (left, top) in panels.items():
        parts.append(f'<rect x="{left:.1f}" y="{top:.1f}" width="{panel_w}" height="{panel_h}" fill="#fff" stroke="#ddd" stroke-width="1"/>')
        parts.append(f'<text x="{left + 12:.1f}" y="{top + 24:.1f}" font-family="Arial, sans-serif" font-size="17" font-weight="700" fill="#222">{steps} Euler steps</text>')
        row = metric_by_step[steps]
        metric_text = f"reference drift {row['mean_reference_drift']:.3f}; mode distance {row['mean_nearest_mode_distance']:.3f}"
        parts.append(f'<text x="{left + 12:.1f}" y="{top + 46:.1f}" font-family="Arial, sans-serif" font-size="12" fill="#555">{metric_text}</text>')
        for x, y in target_points:
            sx, sy = scale_point(x, y, left, top + 55, panel_w, panel_h - 72)
            parts.append(svg_circle(sx, sy, 2.0, "#d95f59", 0.25))
        for sample_path in paths_by_steps[steps]:
            scaled = [scale_point(x, y, left, top + 55, panel_w, panel_h - 72) for x, y in sample_path]
            parts.append(svg_polyline(scaled, "#2f6f8f", 0.70))
            parts.append(svg_circle(scaled[0][0], scaled[0][1], 2.4, "#222", 0.90))
            parts.append(svg_circle(scaled[-1][0], scaled[-1][1], 2.8, "#238b8d", 0.92))
    parts.extend(
        [
            '<text x="55" y="724" font-family="Arial, sans-serif" font-size="13" fill="#444">Metric drift is mean endpoint distance from a 128-step Euler reference on the same initial samples.</text>',
            '<text x="55" y="744" font-family="Arial, sans-serif" font-size="13" fill="#444">The comparison isolates integration step count; the trained field and random starts are held fixed.</text>',
            "</svg>\n",
        ]
    )
    path.write_text("\n".join(parts), encoding="utf-8")


def build(run_dir: Path) -> dict[str, object]:
    rng = random.Random(19)
    weights, losses = train(rng)
    target_rng = random.Random(23)
    target_points = [data_sample(target_rng) for _ in range(220)]
    start_rng = random.Random(29)
    starts = [source_sample(start_rng) for _ in range(18)]
    step_counts = [4, 8, 16, 32]
    reference = [integrate(weights, x0, 128)[-1] for x0 in starts]
    paths_by_steps = {steps: [integrate(weights, x0, steps) for x0 in starts] for steps in step_counts}
    metrics: list[dict[str, float]] = []
    for steps in step_counts:
        endpoints = [path[-1] for path in paths_by_steps[steps]]
        drift = sum(math.sqrt(sq_distance(end, ref)) for end, ref in zip(endpoints, reference)) / len(endpoints)
        mode_distance = sum(nearest_mode_distance(end) for end in endpoints) / len(endpoints)
        metrics.append(
            {
                "steps": float(steps),
                "mean_reference_drift": drift,
                "mean_nearest_mode_distance": mode_distance,
            }
        )
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    run_dir.mkdir(parents=True, exist_ok=True)
    figure_path = ASSET_DIR / "flow-matching-solver-steps.svg"
    write_sweep_svg(target_points, paths_by_steps, metrics, figure_path)
    payload: dict[str, object] = {
        "task": "FM-04",
        "seed": 19,
        "training_steps": 640,
        "batch_size": 128,
        "loss_start": losses[0],
        "loss_final": losses[-1],
        "solver": "explicit Euler",
        "step_counts": step_counts,
        "reference_steps": 128,
        "metrics": metrics,
        "asset": str(figure_path.relative_to(ROOT)),
    }
    (run_dir / "solver_step_metrics.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (run_dir / "README.md").write_text(
        "# FM-04 Solver Step Sweep\n\n"
        "Deterministic pure-Python run for Flow Matching Part 2. The script trains a small linear velocity field on the two-cluster toy distribution, then integrates the same initial samples with 4, 8, 16, and 32 explicit Euler steps. Metrics compare each endpoint to a 128-step Euler reference on the same starts.\n",
        encoding="utf-8",
    )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    args = parser.parse_args()
    payload = build(args.run_dir)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
