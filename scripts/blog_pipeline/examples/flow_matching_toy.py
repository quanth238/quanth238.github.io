#!/usr/bin/env python3
"""Pure-Python 2D flow-matching toy example for remote blog checks."""

from __future__ import annotations

import json
import math
import random
from pathlib import Path


random.seed(7)


def randn() -> float:
    u1 = max(random.random(), 1e-12)
    u2 = random.random()
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


def source_sample() -> tuple[float, float]:
    return randn(), randn()


def data_sample() -> tuple[float, float]:
    center = random.choice([(-2.0, -0.8), (2.0, 0.8)])
    return center[0] + 0.35 * randn(), center[1] + 0.35 * randn()


def features(x: tuple[float, float], t: float) -> tuple[float, float, float, float]:
    return x[0], x[1], t, 1.0


def predict(weights: list[list[float]], x: tuple[float, float], t: float) -> tuple[float, float]:
    feat = features(x, t)
    return (
        sum(weights[0][j] * feat[j] for j in range(4)),
        sum(weights[1][j] * feat[j] for j in range(4)),
    )


def train(steps: int = 520, batch_size: int = 96, lr: float = 0.035) -> tuple[list[list[float]], list[float]]:
    weights = [[0.03 * randn() for _ in range(4)] for _ in range(2)]
    losses: list[float] = []
    for step in range(steps):
        grad = [[0.0 for _ in range(4)] for _ in range(2)]
        loss = 0.0
        for _ in range(batch_size):
            x0 = source_sample()
            x1 = data_sample()
            t = random.random()
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
        if step % 10 == 0 or step == steps - 1:
            losses.append(loss / batch_size)
    return weights, losses


def integrate(weights: list[list[float]], x0: tuple[float, float], steps: int = 48) -> list[tuple[float, float]]:
    x = x0
    path = [x]
    dt = 1.0 / steps
    for i in range(steps):
        t = i / steps
        v = predict(weights, x, t)
        x = (x[0] + dt * v[0], x[1] + dt * v[1])
        path.append(x)
    return path


def scale_point(x: float, y: float, width: int, height: int) -> tuple[float, float]:
    sx = 40.0 + (x + 4.0) / 8.0 * (width - 80.0)
    sy = height - (34.0 + (y + 3.0) / 6.0 * (height - 68.0))
    return sx, sy


def write_loss_svg(losses: list[float], path: Path) -> None:
    width, height = 760, 360
    min_loss, max_loss = min(losses), max(losses)
    denom = max(max_loss - min_loss, 1e-9)
    points = []
    for i, loss in enumerate(losses):
        x = 58 + i / max(len(losses) - 1, 1) * (width - 100)
        y = height - 48 - (loss - min_loss) / denom * (height - 96)
        points.append(f"{x:.1f},{y:.1f}")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Flow matching toy loss curve">
<rect width="100%" height="100%" fill="#fbfbf8"/>
<line x1="58" y1="{height-48}" x2="{width-42}" y2="{height-48}" stroke="#222" stroke-width="1"/>
<line x1="58" y1="42" x2="58" y2="{height-48}" stroke="#222" stroke-width="1"/>
<polyline points="{' '.join(points)}" fill="none" stroke="#2f6f8f" stroke-width="3"/>
<text x="58" y="28" font-family="Arial, sans-serif" font-size="18" fill="#222">Toy velocity-regression loss</text>
<text x="{width-245}" y="{height-18}" font-family="Arial, sans-serif" font-size="13" fill="#444">training checkpoints</text>
<text x="64" y="64" font-family="Arial, sans-serif" font-size="13" fill="#444">start {losses[0]:.3f}</text>
<text x="{width-160}" y="64" font-family="Arial, sans-serif" font-size="13" fill="#444">final {losses[-1]:.3f}</text>
</svg>
"""
    path.write_text(svg, encoding="utf-8")


def write_paths_svg(weights: list[list[float]], path: Path) -> None:
    width, height = 760, 460
    target_points = [data_sample() for _ in range(160)]
    paths = [integrate(weights, source_sample()) for _ in range(16)]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Flow matching toy paths">',
        '<rect width="100%" height="100%" fill="#fbfbf8"/>',
        '<text x="40" y="30" font-family="Arial, sans-serif" font-size="18" fill="#222">Noise samples move along the learned velocity field</text>',
    ]
    for x, y in target_points:
        sx, sy = scale_point(x, y, width, height)
        parts.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="2.4" fill="#d95f59" opacity="0.35"/>')
    for sample_path in paths:
        points = " ".join(f"{scale_point(x, y, width, height)[0]:.1f},{scale_point(x, y, width, height)[1]:.1f}" for x, y in sample_path)
        start = scale_point(*sample_path[0], width, height)
        end = scale_point(*sample_path[-1], width, height)
        parts.append(f'<polyline points="{points}" fill="none" stroke="#2f6f8f" stroke-width="1.8" opacity="0.78"/>')
        parts.append(f'<circle cx="{start[0]:.1f}" cy="{start[1]:.1f}" r="2.6" fill="#333"/>')
        parts.append(f'<circle cx="{end[0]:.1f}" cy="{end[1]:.1f}" r="3.2" fill="#2f6f8f"/>')
    parts.append('<text x="40" y="436" font-family="Arial, sans-serif" font-size="13" fill="#444">black: source noise, blue: integrated samples, red: target data cloud</text>')
    parts.append("</svg>\n")
    path.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    weights, losses = train()
    write_loss_svg(losses, Path("flow-matching-loss.svg"))
    write_paths_svg(weights, Path("flow-matching-paths.svg"))
    Path("flow_matching_metrics.json").write_text(
        json.dumps(
            {
                "steps": 520,
                "loss_start": losses[0],
                "loss_final": losses[-1],
                "weights": weights,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"final_loss={losses[-1]:.6f}")
    print("wrote flow-matching-loss.svg")
    print("wrote flow-matching-paths.svg")


if __name__ == "__main__":
    main()
