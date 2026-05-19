#!/usr/bin/env python3
"""Generate the Part 1 Flow Matching overview schematic."""

from __future__ import annotations

import html
import math
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/img/blog/flow-matching-guide/flow-matching-overview.svg"
WIDTH = 1600
HEIGHT = 900
X_MIN, X_MAX = -4.0, 4.0
Y_MIN, Y_MAX = -2.5, 2.5
PLOT_LEFT, PLOT_RIGHT = 150, 1460
PLOT_TOP, PLOT_BOTTOM = 155, 750


def sx(x: float) -> float:
    return PLOT_LEFT + (x - X_MIN) / (X_MAX - X_MIN) * (PLOT_RIGHT - PLOT_LEFT)


def sy(y: float) -> float:
    return PLOT_BOTTOM - (y - Y_MIN) / (Y_MAX - Y_MIN) * (PLOT_BOTTOM - PLOT_TOP)


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def line(x1: float, y1: float, x2: float, y2: float, cls: str, extra: str = "") -> str:
    return (
        f'<line class="{cls}" x1="{x1:.1f}" y1="{y1:.1f}" '
        f'x2="{x2:.1f}" y2="{y2:.1f}" {extra}/>'
    )


def circle(x: float, y: float, r: float, cls: str, extra: str = "") -> str:
    return f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" {extra}/>'


def text(x: float, y: float, value: str, cls: str, anchor: str = "start") -> str:
    return (
        f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}" '
        f'text-anchor="{anchor}">{esc(value)}</text>'
    )


def arrow_between(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    cls: str,
    scale: float = 1.0,
    extra: str = "",
) -> str:
    dx, dy = x2 - x1, y2 - y1
    return line(x1, y1, x1 + dx * scale, y1 + dy * scale, cls, f'marker-end="url(#arrow-{cls})" {extra}')


def point_on_line(a: tuple[float, float], b: tuple[float, float], t: float) -> tuple[float, float]:
    return (a[0] * (1.0 - t) + b[0] * t, a[1] * (1.0 - t) + b[1] * t)


def field_direction(x: float, y: float) -> tuple[float, float]:
    target = (2.45, 1.05) if y >= 0 else (2.55, -1.05)
    dx = target[0] - x
    dy = target[1] - y
    norm = math.hypot(dx, dy) or 1.0
    return dx / norm, dy / norm


def main() -> None:
    random.seed(19)
    source = [
        (random.gauss(-2.75, 0.38), random.gauss(0.0, 0.72))
        for _ in range(54)
    ]
    target = []
    for _ in range(32):
        target.append((random.gauss(2.55, 0.25), random.gauss(1.05, 0.24)))
        target.append((random.gauss(2.60, 0.25), random.gauss(-1.02, 0.25)))

    highlighted_start = (-2.85, -0.75)
    highlighted_end = (2.55, 1.05)
    ode_points = [
        (-2.75, -1.45),
        (-1.85, -1.30),
        (-0.90, -0.95),
        (-0.10, -0.32),
        (0.62, 0.20),
        (1.30, 0.66),
        (2.02, 0.92),
        (2.55, 1.05),
    ]

    parts: list[str] = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc">',
        "<title id=\"title\">Flow matching overview schematic</title>",
        (
            "<desc id=\"desc\">A deterministic schematic showing source samples, target samples, "
            "straight interpolation times, velocity target arrows, a learned vector field, and "
            "one ODE sampling trajectory.</desc>"
        ),
        """
<defs>
  <marker id="arrow-velocity" markerWidth="11" markerHeight="11" refX="8" refY="3.5" orient="auto">
    <path d="M0,0 L8,3.5 L0,7 Z" fill="#0f766e"/>
  </marker>
  <marker id="arrow-field" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L6,3 L0,6 Z" fill="#64748b"/>
  </marker>
  <marker id="arrow-sample" markerWidth="12" markerHeight="12" refX="9" refY="4" orient="auto">
    <path d="M0,0 L9,4 L0,8 Z" fill="#111827"/>
  </marker>
  <filter id="soft-shadow" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0f172a" flood-opacity="0.10"/>
  </filter>
</defs>
<style>
  .bg { fill: #f8fafc; }
  .plot { fill: #ffffff; stroke: #d7dee8; stroke-width: 2; }
  .grid { stroke: #e8edf3; stroke-width: 1; }
  .axis { stroke: #b7c1cf; stroke-width: 1.4; }
  .title { fill: #0f172a; font-family: Inter, Arial, sans-serif; font-size: 34px; font-weight: 760; }
  .subtitle { fill: #475569; font-family: Inter, Arial, sans-serif; font-size: 18px; }
  .section { fill: #0f172a; font-family: Inter, Arial, sans-serif; font-size: 20px; font-weight: 720; }
  .label { fill: #334155; font-family: Inter, Arial, sans-serif; font-size: 16px; font-weight: 650; }
  .small { fill: #475569; font-family: Inter, Arial, sans-serif; font-size: 13px; font-weight: 600; }
  .source { fill: #2563eb; fill-opacity: 0.78; stroke: #1e40af; stroke-width: 1; }
  .target { fill: #dc5a3d; fill-opacity: 0.78; stroke: #9f2d20; stroke-width: 1; }
  .midpoint { fill: #f2b705; stroke: #8a5c00; stroke-width: 1.5; }
  .path-line { stroke: #0f766e; stroke-width: 4; stroke-linecap: round; fill: none; }
  .path-faint { stroke: #0f766e; stroke-width: 1.4; stroke-opacity: 0.28; fill: none; }
  .velocity { stroke: #0f766e; stroke-width: 4; stroke-linecap: round; fill: none; }
  .field { stroke: #64748b; stroke-width: 2.2; stroke-linecap: round; fill: none; opacity: 0.58; }
  .sample { stroke: #111827; stroke-width: 5; stroke-linecap: round; stroke-linejoin: round; fill: none; }
  .step { fill: #ffffff; stroke: #111827; stroke-width: 2; }
  .callout { fill: #ffffff; stroke: #d7dee8; stroke-width: 1.5; filter: url(#soft-shadow); }
</style>
""",
        '<rect class="bg" width="1600" height="900"/>',
        '<rect class="plot" x="115" y="120" width="1370" height="665" rx="18"/>',
        text(115, 72, "Flow matching objects in one pass", "title"),
        text(
            115,
            104,
            "Training uses paired endpoints and velocity targets; sampling integrates the learned field from fresh noise.",
            "subtitle",
        ),
    ]

    for x in [-3, -2, -1, 0, 1, 2, 3]:
        parts.append(line(sx(x), PLOT_TOP, sx(x), PLOT_BOTTOM, "grid"))
    for y in [-2, -1, 0, 1, 2]:
        parts.append(line(PLOT_LEFT, sy(y), PLOT_RIGHT, sy(y), "grid"))
    parts.append(line(PLOT_LEFT, sy(0), PLOT_RIGHT, sy(0), "axis"))
    parts.append(line(sx(0), PLOT_TOP, sx(0), PLOT_BOTTOM, "axis"))

    parts.extend(
        [
            text(190, 835, "1. sample endpoints", "section"),
            text(510, 835, "2. interpolate path", "section"),
            text(870, 835, "3. regress velocity", "section"),
            text(1190, 835, "4. integrate ODE", "section"),
        ]
    )

    pair_indices = [1, 6, 10, 16, 22, 31]
    for index, source_index in enumerate(pair_indices):
        a = source[source_index]
        b = target[(index * 9 + 5) % len(target)]
        parts.append(line(sx(a[0]), sy(a[1]), sx(b[0]), sy(b[1]), "path-faint"))

    for x, y in source:
        parts.append(circle(sx(x), sy(y), 5.0, "source"))
    for x, y in target:
        parts.append(circle(sx(x), sy(y), 5.0, "target"))

    start_svg = (sx(highlighted_start[0]), sy(highlighted_start[1]))
    end_svg = (sx(highlighted_end[0]), sy(highlighted_end[1]))
    parts.append(line(*start_svg, *end_svg, "path-line"))
    for t, name, y_offset in [(0.0, "t=0", 25), (0.5, "t=0.5", -18), (1.0, "t=1", -18)]:
        px, py = point_on_line(highlighted_start, highlighted_end, t)
        cls = "midpoint" if t == 0.5 else ("source" if t == 0.0 else "target")
        parts.append(circle(sx(px), sy(py), 8.0, cls))
        parts.append(text(sx(px), sy(py) + y_offset, name, "small", "middle"))

    for t in [0.24, 0.48, 0.72]:
        px, py = point_on_line(highlighted_start, highlighted_end, t)
        qx, qy = point_on_line(highlighted_start, highlighted_end, min(t + 0.13, 1.0))
        parts.append(arrow_between(sx(px), sy(py), sx(qx), sy(qy), "velocity", 1.0))

    for gx in [-0.8, -0.2, 0.4, 1.0, 1.6]:
        for gy in [-1.55, -0.75, 0.05, 0.85, 1.65]:
            dx, dy = field_direction(gx, gy)
            length = 56
            x1, y1 = sx(gx), sy(gy)
            x2, y2 = x1 + dx * length, y1 - dy * length
            parts.append(arrow_between(x1, y1, x2, y2, "field", 1.0))

    path_d = [f"M {sx(ode_points[0][0]):.1f} {sy(ode_points[0][1]):.1f}"]
    for point in ode_points[1:]:
        path_d.append(f"L {sx(point[0]):.1f} {sy(point[1]):.1f}")
    parts.append(f'<path class="sample" d="{" ".join(path_d)}" marker-end="url(#arrow-sample)"/>')
    for point in ode_points[:-1]:
        parts.append(circle(sx(point[0]), sy(point[1]), 5.5, "step"))

    callouts = [
        (148, 128, 260, 76, "source x0 ~ p0", "easy noise distribution"),
        (1060, 128, 300, 76, "target x1 ~ p1", "observed data samples"),
        (552, 202, 260, 76, "conditional path", "xt lies between endpoints"),
        (748, 505, 290, 76, "velocity target", "arrows point along the path"),
        (1010, 585, 320, 76, "learned field v_theta", "local directions used at sampling"),
        (1118, 690, 292, 76, "ODE trajectory", "fresh noise follows the field"),
    ]
    for x, y, w, h, heading, sub in callouts:
        parts.append(f'<rect class="callout" x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/>')
        parts.append(text(x + 18, y + 30, heading, "label"))
        parts.append(text(x + 18, y + 56, sub, "small"))

    parts.append("</svg>\n")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
