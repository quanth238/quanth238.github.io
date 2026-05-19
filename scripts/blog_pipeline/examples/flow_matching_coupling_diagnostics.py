#!/usr/bin/env python3
"""Generate endpoint-coupling diagnostics for Flow Matching Part 4."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ASSET_DIR = ROOT / "assets/img/blog/flow-matching-guide"
DEFAULT_RUN_DIR = ROOT / "_blog_work/flow-matching-guide/remote_runs/fm06_coupling_diagnostics"


Point = tuple[float, float]


def randn(rng: random.Random) -> float:
    u1 = max(rng.random(), 1e-12)
    u2 = rng.random()
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


def source_sample(rng: random.Random) -> Point:
    return 0.85 * randn(rng), 0.85 * randn(rng)


def data_sample(rng: random.Random) -> Point:
    center = rng.choice([(-2.2, -0.9), (2.2, 0.9)])
    return center[0] + 0.28 * randn(rng), center[1] + 0.28 * randn(rng)


def squared_distance(a: Point, b: Point) -> float:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def transport_cost(sources: list[Point], targets: list[Point], assignment: list[int]) -> float:
    return sum(squared_distance(sources[i], targets[assignment[i]]) for i in range(len(sources))) / len(sources)


def minibatch_assignment(sources: list[Point], targets: list[Point]) -> list[int]:
    n = len(sources)
    costs = [[squared_distance(sources[i], targets[j]) for j in range(n)] for i in range(n)]
    best: dict[int, tuple[float, tuple[int, ...]]] = {0: (0.0, ())}
    for i in range(n):
        next_best: dict[int, tuple[float, tuple[int, ...]]] = {}
        for mask, (cost, perm) in best.items():
            for j in range(n):
                if mask & (1 << j):
                    continue
                new_mask = mask | (1 << j)
                new_cost = cost + costs[i][j]
                current = next_best.get(new_mask)
                if current is None or new_cost < current[0]:
                    next_best[new_mask] = (new_cost, perm + (j,))
        best = next_best
    return list(best[(1 << n) - 1][1])


def orientation(a: Point, b: Point, c: Point) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def segments_cross(a: Point, b: Point, c: Point, d: Point) -> bool:
    o1 = orientation(a, b, c)
    o2 = orientation(a, b, d)
    o3 = orientation(c, d, a)
    o4 = orientation(c, d, b)
    return o1 * o2 < 0 and o3 * o4 < 0


def crossing_count(sources: list[Point], targets: list[Point], assignment: list[int]) -> int:
    count = 0
    for i, j in itertools.combinations(range(len(sources)), 2):
        if segments_cross(sources[i], targets[assignment[i]], sources[j], targets[assignment[j]]):
            count += 1
    return count


def scale_point(x: float, y: float, left: float, top: float, width: float, height: float) -> Point:
    sx = left + (x + 3.6) / 7.2 * width
    sy = top + height - (y + 2.6) / 5.2 * height
    return sx, sy


def panel(
    title: str,
    sources: list[Point],
    targets: list[Point],
    assignment: list[int],
    left: float,
    top: float,
    width: float,
    height: float,
    metrics: dict[str, float],
) -> list[str]:
    parts = [
        f'<rect x="{left:.1f}" y="{top:.1f}" width="{width:.1f}" height="{height:.1f}" fill="#fff" stroke="#ddd"/>',
        f'<text x="{left + 14:.1f}" y="{top + 26:.1f}" font-family="Arial, sans-serif" font-size="18" font-weight="700" fill="#222">{title}</text>',
        f'<text x="{left + 14:.1f}" y="{top + 48:.1f}" font-family="Arial, sans-serif" font-size="12" fill="#555">mean cost {metrics["cost"]:.3f}; crossings {int(metrics["crossings"])}</text>',
    ]
    plot_top = top + 62
    plot_h = height - 84
    for i, source in enumerate(sources):
        target = targets[assignment[i]]
        sx, sy = scale_point(source[0], source[1], left + 16, plot_top, width - 32, plot_h)
        tx, ty = scale_point(target[0], target[1], left + 16, plot_top, width - 32, plot_h)
        parts.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="#8d8d8d" stroke-width="1.2" opacity="0.55"/>')
    for source in sources:
        sx, sy = scale_point(source[0], source[1], left + 16, plot_top, width - 32, plot_h)
        parts.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="4.0" fill="#222" opacity="0.86"/>')
    for target in targets:
        tx, ty = scale_point(target[0], target[1], left + 16, plot_top, width - 32, plot_h)
        parts.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="4.6" fill="#d95f59" opacity="0.82"/>')
    return parts


def write_svg(
    sources: list[Point],
    targets: list[Point],
    independent: list[int],
    minibatch_ot: list[int],
    metrics: dict[str, dict[str, float]],
    path: Path,
) -> None:
    width, height = 1100, 620
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Endpoint coupling comparison for independent pairing and minibatch optimal transport pairing">',
        '<rect width="100%" height="100%" fill="#fbfbf8"/>',
        '<text x="54" y="38" font-family="Arial, sans-serif" font-size="24" font-weight="700" fill="#222">Endpoint coupling changes the paths the model sees</text>',
        '<text x="54" y="62" font-family="Arial, sans-serif" font-size="14" fill="#555">Black points are source samples, vermillion points are data samples, gray segments are conditional paths inside one batch.</text>',
    ]
    parts.extend(panel("Independent random pairing", sources, targets, independent, 54, 88, 470, 390, metrics["independent"]))
    parts.extend(panel("Minibatch OT assignment", sources, targets, minibatch_ot, 574, 88, 470, 390, metrics["minibatch_ot"]))
    parts.extend(
        [
            '<rect x="54" y="510" width="990" height="68" fill="#fff" stroke="#ddd"/>',
            '<text x="74" y="536" font-family="Arial, sans-serif" font-size="13" fill="#444">This batch assignment minimizes squared endpoint distance only inside the displayed minibatch.</text>',
            '<text x="74" y="558" font-family="Arial, sans-serif" font-size="13" fill="#444">Lower segment cost and fewer crossings are path-geometry diagnostics, not a proof of a global transport plan.</text>',
            "</svg>\n",
        ]
    )
    path.write_text("\n".join(parts), encoding="utf-8")


def build(run_dir: Path) -> dict[str, object]:
    rng = random.Random(61)
    n = 12
    sources = [source_sample(rng) for _ in range(n)]
    targets = [data_sample(rng) for _ in range(n)]
    independent = list(range(n))
    rng.shuffle(independent)
    minibatch_ot = minibatch_assignment(sources, targets)
    metrics = {
        "independent": {
            "cost": transport_cost(sources, targets, independent),
            "crossings": float(crossing_count(sources, targets, independent)),
        },
        "minibatch_ot": {
            "cost": transport_cost(sources, targets, minibatch_ot),
            "crossings": float(crossing_count(sources, targets, minibatch_ot)),
        },
    }
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    run_dir.mkdir(parents=True, exist_ok=True)
    figure_path = ASSET_DIR / "flow-matching-coupling-diagnostics.svg"
    write_svg(sources, targets, independent, minibatch_ot, metrics, figure_path)
    payload: dict[str, object] = {
        "task": "FM-06",
        "seed": 61,
        "batch_size": n,
        "assignment_method": "exact squared-distance assignment within one minibatch",
        "metrics": metrics,
        "asset": str(figure_path.relative_to(ROOT)),
    }
    (run_dir / "coupling_diagnostics.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (run_dir / "README.md").write_text(
        "# FM-06 Coupling Diagnostics\n\n"
        "Deterministic pure-Python comparison of independent random endpoint pairing and a squared-distance minibatch assignment. The diagnostics are batch-local transport cost and line-crossing count.\n",
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
