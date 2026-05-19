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
    stroke: str | None = None,
    stroke_width: float = 1.0,
) -> str:
    sx, sy = scale_point(x, y, left, top, width, height)
    stroke_attr = f' stroke="{stroke}" stroke-width="{stroke_width:.1f}"' if stroke else ""
    return f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{radius:.1f}" fill="{fill}" opacity="{opacity:.2f}"{stroke_attr}/>'


def polyline(
    points: list[tuple[float, float]],
    color: str,
    left: float,
    top: float,
    width: float,
    height: float,
    opacity: float = 0.82,
    stroke_width: float = 1.8,
    dash: str | None = None,
) -> str:
    coords = " ".join(f"{scale_point(x, y, left, top, width, height)[0]:.1f},{scale_point(x, y, left, top, width, height)[1]:.1f}" for x, y in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="{stroke_width:.1f}" '
        f'opacity="{opacity:.2f}" stroke-linecap="round" stroke-linejoin="round"{dash_attr}/>'
    )


def screen_arrow(x1: float, y1: float, x2: float, y2: float, color: str = "#777777") -> str:
    angle = math.atan2(y2 - y1, x2 - x1)
    head = 7.0
    left = (x2 - head * math.cos(angle - 0.55), y2 - head * math.sin(angle - 0.55))
    right = (x2 - head * math.cos(angle + 0.55), y2 - head * math.sin(angle + 0.55))
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>'
        f'<path d="M {left[0]:.1f} {left[1]:.1f} L {x2:.1f} {y2:.1f} L {right[0]:.1f} {right[1]:.1f}" '
        f'fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>'
    )


def wiring_box(x: float, y: float, w: float, title: str, detail: str) -> list[str]:
    return [
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="64" fill="#ffffff" stroke="#d8d8d8"/>',
        f'<text x="{x + 14:.1f}" y="{y + 24:.1f}" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#222">{title}</text>',
        f'<text x="{x + 14:.1f}" y="{y + 45:.1f}" font-family="Arial, sans-serif" font-size="11" fill="#555">{detail}</text>',
    ]


def write_svg(
    x0: list[tuple[float, float]],
    x1: list[tuple[float, float]],
    exact_paths: list[list[tuple[float, float]]],
    solver_paths: list[list[tuple[float, float]]],
    metrics: dict[str, Any],
    path: Path,
) -> None:
    width, height = 1120, 700
    left, top, plot_w, plot_h = 62.0, 190.0, 662.0, 370.0
    panel_x, panel_y, panel_w, panel_h = 760.0, 190.0, 300.0, 370.0
    gap_mean = metrics["mean_solver_path_gap_at_final_time"]
    gap_max = metrics["max_solver_path_gap_at_final_time"]
    remaining_mean = metrics["mean_remaining_distance_to_endpoint_at_final_time"]
    residual_px_per_data = 80_000_000.0
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Official flow_matching package check comparing exact CondOTProbPath samples with ODESolver trajectories">',
        '<rect width="100%" height="100%" fill="#fbfbf8"/>',
        '<text x="62" y="38" font-family="Arial, sans-serif" font-size="23" font-weight="700" fill="#222">Official package check: exact path and ODESolver agree</text>',
        '<text x="62" y="63" font-family="Arial, sans-serif" font-size="14" fill="#555">Same endpoints and time grid; dashed exact paths are drawn on top of solver paths so the overlay is inspectable.</text>',
    ]
    box_y = 88.0
    box_w = 212.0
    parts.extend(wiring_box(62.0, box_y, box_w, "CondOTProbPath", "sample exact x_t(t)"))
    parts.extend(wiring_box(310.0, box_y, box_w, "velocity callable", "matching conditional u_t"))
    parts.extend(wiring_box(558.0, box_y, box_w, "ODESolver.sample", "midpoint, t up to 0.98"))
    parts.extend(wiring_box(806.0, box_y, box_w, "verified output", "compare at the same t"))
    parts.append(screen_arrow(274.0, box_y + 32.0, 302.0, box_y + 32.0))
    parts.append(screen_arrow(522.0, box_y + 32.0, 550.0, box_y + 32.0))
    parts.append(screen_arrow(770.0, box_y + 32.0, 798.0, box_y + 32.0))
    parts.extend(
        [
            f'<rect x="{left:.1f}" y="{top:.1f}" width="{plot_w:.1f}" height="{plot_h:.1f}" fill="#fff" stroke="#ddd"/>',
            f'<text x="{left + 14:.1f}" y="{top + 24:.1f}" font-family="Arial, sans-serif" font-size="15" font-weight="700" fill="#222">Path agreement on the same conditional endpoints</text>',
            f'<rect x="{panel_x:.1f}" y="{panel_y:.1f}" width="{panel_w:.1f}" height="{panel_h:.1f}" fill="#ffffff" stroke="#ddd"/>',
            f'<text x="{panel_x + 16:.1f}" y="{panel_y + 26:.1f}" font-family="Arial, sans-serif" font-size="15" font-weight="700" fill="#222">Verified output at t=0.98</text>',
        ]
    )
    for sample_path in solver_paths:
        parts.append(polyline(sample_path, "#2f6f8f", left, top + 34, plot_w, plot_h - 50, 0.72, 2.4))
    for sample_path in exact_paths:
        parts.append(polyline(sample_path, "#d88c2f", left, top + 34, plot_w, plot_h - 50, 0.92, 2.1, "7 5"))
    for x, y in x0:
        parts.append(circle(x, y, 3.4, "#222222", 0.88, left, top + 34, plot_w, plot_h - 50))
    for x, y in x1:
        parts.append(circle(x, y, 4.1, "#d95f59", 0.88, left, top + 34, plot_w, plot_h - 50))
    parts.extend(
        [
            f'<line x1="{left + 18:.1f}" y1="{top + 52:.1f}" x2="{left + 48:.1f}" y2="{top + 52:.1f}" stroke="#2f6f8f" stroke-width="2.4" stroke-linecap="round"/>',
            f'<text x="{left + 58:.1f}" y="{top + 56:.1f}" font-family="Arial, sans-serif" font-size="12" fill="#444">ODESolver trajectory</text>',
            f'<line x1="{left + 212:.1f}" y1="{top + 52:.1f}" x2="{left + 242:.1f}" y2="{top + 52:.1f}" stroke="#d88c2f" stroke-width="2.1" stroke-dasharray="7 5" stroke-linecap="round"/>',
            f'<text x="{left + 252:.1f}" y="{top + 56:.1f}" font-family="Arial, sans-serif" font-size="12" fill="#444">exact CondOTProbPath sample</text>',
            f'<circle cx="{left + 462:.1f}" cy="{top + 52:.1f}" r="3.4" fill="#222222" opacity="0.88"/>',
            f'<text x="{left + 474:.1f}" y="{top + 56:.1f}" font-family="Arial, sans-serif" font-size="12" fill="#444">x0</text>',
            f'<circle cx="{left + 520:.1f}" cy="{top + 52:.1f}" r="4.1" fill="#d95f59" opacity="0.88"/>',
            f'<text x="{left + 532:.1f}" y="{top + 56:.1f}" font-family="Arial, sans-serif" font-size="12" fill="#444">x1</text>',
        ]
    )
    metric_x = panel_x + 18
    parts.extend(
        [
            f'<text x="{metric_x:.1f}" y="{panel_y + 60:.1f}" font-family="Arial, sans-serif" font-size="12" fill="#555">solver[-1] vs exact path[-1]</text>',
            f'<text x="{metric_x:.1f}" y="{panel_y + 94:.1f}" font-family="Arial, sans-serif" font-size="25" font-weight="700" fill="#238b8d">mean gap {gap_mean:.2e}</text>',
            f'<text x="{metric_x:.1f}" y="{panel_y + 118:.1f}" font-family="Arial, sans-serif" font-size="13" fill="#444">max gap {gap_max:.2e}; method {metrics["method"]}, step {metrics["step_size"]:.2f}</text>',
            f'<text x="{metric_x:.1f}" y="{panel_y + 154:.1f}" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#222">terminal residuals, magnified 8e7x</text>',
            f'<rect x="{metric_x:.1f}" y="{panel_y + 166:.1f}" width="250" height="88" fill="#fbfbf8" stroke="#e3e3e3"/>',
        ]
    )
    for idx, (exact_path, solver_path) in enumerate(zip(exact_paths, solver_paths)):
        row = idx // 4
        col = idx % 4
        base_x = metric_x + 32 + col * 58
        base_y = panel_y + 196 + row * 34
        residual = (solver_path[-1][0] - exact_path[-1][0], solver_path[-1][1] - exact_path[-1][1])
        end_x = base_x + residual[0] * residual_px_per_data
        end_y = base_y - residual[1] * residual_px_per_data
        parts.append(f'<line x1="{base_x:.1f}" y1="{base_y:.1f}" x2="{end_x:.1f}" y2="{end_y:.1f}" stroke="#777777" stroke-width="1.0" opacity="0.72"/>')
        parts.append(f'<circle cx="{base_x:.1f}" cy="{base_y:.1f}" r="2.7" fill="#d88c2f" opacity="0.90"/>')
        parts.append(f'<circle cx="{end_x:.1f}" cy="{end_y:.1f}" r="2.6" fill="#2f6f8f" opacity="0.90"/>')
    remaining_bar_w = min(230.0, 230.0 * float(remaining_mean) / 0.10)
    parts.extend(
        [
            f'<text x="{metric_x:.1f}" y="{panel_y + 284:.1f}" font-family="Arial, sans-serif" font-size="12" fill="#555">remaining path segment to endpoint, not solver error</text>',
            f'<rect x="{metric_x:.1f}" y="{panel_y + 298:.1f}" width="230" height="13" fill="#eeeeee"/>',
            f'<rect x="{metric_x:.1f}" y="{panel_y + 298:.1f}" width="{remaining_bar_w:.1f}" height="13" fill="#d95f59" opacity="0.78"/>',
            f'<text x="{metric_x:.1f}" y="{panel_y + 332:.1f}" font-family="Arial, sans-serif" font-size="13" fill="#444">mean remaining distance: {remaining_mean:.4f}</text>',
            '<rect x="62" y="586" width="998" height="62" fill="#fff" stroke="#ddd"/>',
            f'<text x="82" y="612" font-family="Arial, sans-serif" font-size="13" fill="#444">Package: flow_matching {metrics["flow_matching_version"]}; components: CondOTProbPath and ODESolver.</text>',
            '<text x="82" y="632" font-family="Arial, sans-serif" font-size="13" fill="#444">Dashed exact paths are rendered above the solid solver paths; only the residual inset is magnified.</text>',
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
    solver_path_gap = torch.linalg.norm(solved[-1] - exact[-1], dim=1)
    remaining_distance_to_endpoint = torch.linalg.norm(exact[-1] - x1, dim=1)
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
        "mean_solver_path_gap_at_final_time": float(solver_path_gap.mean()),
        "max_solver_path_gap_at_final_time": float(solver_path_gap.max()),
        "mean_remaining_distance_to_endpoint_at_final_time": float(remaining_distance_to_endpoint.mean()),
        "max_remaining_distance_to_endpoint_at_final_time": float(remaining_distance_to_endpoint.max()),
        "visual_encoding": {
            "layout": "api_wiring_path_overlay_and_verified_output_panel",
            "exact_paths_drawn_after_solver": True,
            "exact_path_style": "dashed_orange",
            "solver_path_style": "solid_blue",
            "terminal_residuals": "magnified_in_inset_only",
            "terminal_residual_magnification_px_per_data_unit": 80_000_000.0,
            "paper_figure_extraction": False,
        },
        "asset": str(figure_path.relative_to(ROOT)),
    }
    write_svg(x0_list, x1_list, exact_paths, solver_paths, metrics, figure_path)
    (run_dir / "official_package_smoke_test.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    (run_dir / "README.md").write_text(
        "# FM-08 Official Package Smoke Test\n\n"
        "This run targets `flow_matching==1.0.10` in a temporary venv with system Torch. It imports `CondOTProbPath` and `ODESolver`, samples conditional OT path points, integrates the matching conditional velocity with `ODESolver.sample`, and writes a local SVG output.\n",
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
