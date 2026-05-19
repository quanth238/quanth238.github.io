#!/usr/bin/env python3
"""Run a minimal official-package bridge for Flow Matching Part 6."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
ASSET_DIR = ROOT / "assets/img/blog/flow-matching-guide"
DEFAULT_RUN_DIR = ROOT / "_blog_work/flow-matching-guide/remote_runs/fm08_official_package"


def scale_point(x: float, y: float, left: float, top: float, width: float, height: float) -> tuple[float, float]:
    sx = left + (x + 3.5) / 7.0 * width
    sy = top + height - (y + 2.8) / 5.6 * height
    return sx, sy


def circle(x: float, y: float, radius: float, fill: str, opacity: float, left: float, top: float, width: float, height: float) -> str:
    sx, sy = scale_point(x, y, left, top, width, height)
    return f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{radius:.1f}" fill="{fill}" opacity="{opacity:.2f}"/>'


def polyline(points: list[tuple[float, float]], color: str, left: float, top: float, width: float, height: float, opacity: float = 0.82) -> str:
    coords = " ".join(f"{scale_point(x, y, left, top, width, height)[0]:.1f},{scale_point(x, y, left, top, width, height)[1]:.1f}" for x, y in points)
    return f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="1.8" opacity="{opacity:.2f}"/>'


def write_svg(
    x0: list[tuple[float, float]],
    x1: list[tuple[float, float]],
    exact_paths: list[list[tuple[float, float]]],
    solver_paths: list[list[tuple[float, float]]],
    metrics: dict[str, Any],
    path: Path,
) -> None:
    width, height = 980, 620
    left, top, plot_w, plot_h = 62.0, 86.0, 856.0, 420.0
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Official flow_matching package smoke test with CondOTProbPath and ODESolver">',
        '<rect width="100%" height="100%" fill="#fbfbf8"/>',
        '<text x="62" y="38" font-family="Arial, sans-serif" font-size="24" font-weight="700" fill="#222">Official package smoke test: path object plus ODE solver</text>',
        '<text x="62" y="62" font-family="Arial, sans-serif" font-size="14" fill="#555">Dotted exact conditional paths from CondOTProbPath; solid solver paths from ODESolver using the matching conditional velocity.</text>',
        f'<rect x="{left:.1f}" y="{top:.1f}" width="{plot_w:.1f}" height="{plot_h:.1f}" fill="#fff" stroke="#ddd"/>',
    ]
    for sample_path in exact_paths:
        parts.append(polyline(sample_path, "#8d8d8d", left, top, plot_w, plot_h, 0.45).replace('stroke-width="1.8"', 'stroke-width="1.2" stroke-dasharray="4 4"'))
    for sample_path in solver_paths:
        parts.append(polyline(sample_path, "#2f6f8f", left, top, plot_w, plot_h, 0.86))
    for x, y in x0:
        parts.append(circle(x, y, 3.4, "#222222", 0.88, left, top, plot_w, plot_h))
    for x, y in x1:
        parts.append(circle(x, y, 4.0, "#d95f59", 0.88, left, top, plot_w, plot_h))
    parts.extend(
        [
            '<rect x="62" y="532" width="856" height="52" fill="#fff" stroke="#ddd"/>',
            f'<text x="82" y="558" font-family="Arial, sans-serif" font-size="13" fill="#444">Package: flow_matching {metrics["flow_matching_version"]}; components: CondOTProbPath, ODESolver.</text>',
            f'<text x="82" y="578" font-family="Arial, sans-serif" font-size="13" fill="#444">Mean endpoint error at t=0.98 against the conditional target: {metrics["mean_endpoint_error"]:.4f}.</text>',
            "</svg>\n",
        ]
    )
    path.write_text("\n".join(parts), encoding="utf-8")


def build(run_dir: Path) -> dict[str, Any]:
    import torch
    import flow_matching
    from flow_matching.path import CondOTProbPath
    from flow_matching.solver import ODESolver

    class ConditionalOTVelocity:
        def __call__(self, x: torch.Tensor, t: torch.Tensor, x_1: torch.Tensor) -> torch.Tensor:
            while t.ndim < x.ndim:
                t = t.unsqueeze(-1)
            return (x_1 - x) / torch.clamp(1.0 - t, min=1e-4)

    torch.manual_seed(83)
    x0 = torch.randn(8, 2)
    centers = torch.tensor([[-2.2, -0.8], [2.2, 0.8]], dtype=torch.float32)
    choices = torch.tensor([0, 1, 0, 1, 0, 1, 0, 1])
    x1 = centers[choices] + 0.22 * torch.randn(8, 2)
    time_grid = torch.linspace(0.0, 0.98, 18)
    path = CondOTProbPath()
    exact_by_time = []
    for t_value in time_grid:
        t = torch.full((x0.shape[0],), float(t_value))
        sample = path.sample(x0, x1, t)
        exact_by_time.append(sample.x_t)
    exact = torch.stack(exact_by_time, dim=0)
    solver = ODESolver(velocity_model=ConditionalOTVelocity())
    solved = solver.sample(
        x_init=x0,
        x_1=x1,
        step_size=0.02,
        method="midpoint",
        time_grid=time_grid,
        return_intermediates=True,
    )
    endpoint_error = torch.linalg.norm(solved[-1] - x1, dim=1)
    x0_list = [tuple(map(float, row)) for row in x0.tolist()]
    x1_list = [tuple(map(float, row)) for row in x1.tolist()]
    exact_paths = [
        [tuple(map(float, exact[t_idx, sample_idx].tolist())) for t_idx in range(exact.shape[0])]
        for sample_idx in range(x0.shape[0])
    ]
    solver_paths = [
        [tuple(map(float, solved[t_idx, sample_idx].tolist())) for t_idx in range(solved.shape[0])]
        for sample_idx in range(x0.shape[0])
    ]
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    run_dir.mkdir(parents=True, exist_ok=True)
    figure_path = ASSET_DIR / "flow-matching-official-package-bridge.svg"
    metrics: dict[str, Any] = {
        "task": "FM-08",
        "flow_matching_version": "1.0.10",
        "flow_matching_module": getattr(flow_matching, "__file__", None),
        "torch_version": torch.__version__,
        "components": ["CondOTProbPath", "ODESolver"],
        "method": "midpoint",
        "step_size": 0.02,
        "time_grid_end": 0.98,
        "mean_endpoint_error": float(endpoint_error.mean()),
        "max_endpoint_error": float(endpoint_error.max()),
        "asset": str(figure_path.relative_to(ROOT)),
    }
    write_svg(x0_list, x1_list, exact_paths, solver_paths, metrics, figure_path)
    (run_dir / "official_package_smoke_test.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    (run_dir / "README.md").write_text(
        "# FM-08 Official Package Smoke Test\n\n"
        "Verified `flow_matching==1.0.10` in a temporary venv with system Torch. The run imports `CondOTProbPath` and `ODESolver`, samples conditional OT path points, integrates the matching conditional velocity with `ODESolver.sample`, and writes a local SVG output.\n",
        encoding="utf-8",
    )
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    args = parser.parse_args()
    print(json.dumps(build(args.run_dir), indent=2))


if __name__ == "__main__":
    main()
