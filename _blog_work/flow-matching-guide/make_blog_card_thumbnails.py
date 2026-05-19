#!/usr/bin/env python3
"""Generate card-sized Flow Matching thumbnails for the blog index."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/img/blog/flow-matching-guide"

INK = "#111827"
PANEL = "#172033"
TEXT = "#F8FAFC"
MUTED = "#AEB8C8"
BLUE = "#60A5FA"
TEAL = "#2DD4BF"
ORANGE = "#FB923C"
ROSE = "#FB7185"
YELLOW = "#FACC15"
PURPLE = "#A78BFA"


def header(part: int, kicker: str, title: str, desc: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" role="img" aria-labelledby="title desc">
  <title id="title">Flow Matching Part {part}: {title}</title>
  <desc id="desc">{desc}</desc>
  <rect width="1200" height="675" rx="34" fill="{INK}"/>
  <rect x="34" y="34" width="1132" height="607" rx="28" fill="{PANEL}" stroke="#2B3548" stroke-width="2"/>
  <text x="72" y="96" fill="{MUTED}" font-family="Inter, Arial, sans-serif" font-size="28" font-weight="700" letter-spacing="1.5">PART {part} / {kicker}</text>
  <text x="72" y="154" fill="{TEXT}" font-family="Inter, Arial, sans-serif" font-size="47" font-weight="760">{title}</text>
"""


def footer() -> str:
    return "</svg>\n"


def dots(points: list[tuple[int, int]], color: str, r: int = 8, opacity: float = 1.0) -> str:
    return "\n".join(
        f'  <circle cx="{x}" cy="{y}" r="{r}" fill="{color}" opacity="{opacity}"/>'
        for x, y in points
    )


def arrow_defs() -> str:
    return f"""  <defs>
    <marker id="arrow" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
      <path d="M2,2 L10,6 L2,10 Z" fill="{TEXT}"/>
    </marker>
    <marker id="arrow-teal" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
      <path d="M2,2 L10,6 L2,10 Z" fill="{TEAL}"/>
    </marker>
    <marker id="arrow-orange" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
      <path d="M2,2 L10,6 L2,10 Z" fill="{ORANGE}"/>
    </marker>
  </defs>
"""


def part1() -> str:
    src = [(170, 395), (212, 363), (230, 430), (185, 475), (265, 385), (275, 462)]
    tgt = [(936, 348), (992, 382), (1018, 318), (910, 424), (1050, 420), (962, 472)]
    mid = [(420, 390), (520, 360), (610, 338), (710, 346), (805, 382)]
    return (
        header(1, "TRAINING TARGET", "Train a velocity field", "Source samples move along a path; velocity arrows define the regression target.")
        + arrow_defs()
        + dots(src, BLUE, 13, 0.95)
        + dots(tgt, ORANGE, 13, 0.95)
        + dots(mid, TEAL, 10, 0.95)
        + '  <path d="M205 430 C345 330 465 340 585 355 C720 375 820 340 985 382" fill="none" stroke="#E5E7EB" stroke-width="8" stroke-linecap="round" marker-end="url(#arrow)"/>\n'
        + '  <path d="M425 458 l88 -58 M565 430 l95 -55 M705 424 l98 -52" stroke="#FDE68A" stroke-width="6" stroke-linecap="round" marker-end="url(#arrow-orange)"/>\n'
        + f'  <text x="160" y="544" fill="{MUTED}" font-family="Inter, Arial, sans-serif" font-size="28">source noise</text>\n'
        + f'  <text x="886" y="544" fill="{MUTED}" font-family="Inter, Arial, sans-serif" font-size="28">data cloud</text>\n'
        + f'  <text x="470" y="535" fill="{TEXT}" font-family="Inter, Arial, sans-serif" font-size="34" font-weight="700">path + velocity target</text>\n'
        + footer()
    )


def part2() -> str:
    return (
        header(2, "SAMPLER", "Sampling is an ODE", "Coarse and fine solver paths are compared against the same learned field.")
        + arrow_defs()
        + '  <path d="M140 505 C295 450 380 335 510 360 C640 390 700 300 840 300 C930 302 990 260 1080 218" fill="none" stroke="#344155" stroke-width="12" stroke-linecap="round"/>\n'
        + '  <path d="M140 505 L292 452 L440 382 L590 368 L740 317 L890 284 L1080 218" fill="none" stroke="#FDE68A" stroke-width="6" stroke-linecap="round" marker-end="url(#arrow-orange)"/>\n'
        + '  <path d="M140 505 C285 454 377 342 510 361 C641 380 708 305 840 300 C932 300 997 262 1080 218" fill="none" stroke="#60A5FA" stroke-width="5" stroke-linecap="round" marker-end="url(#arrow)"/>\n'
        + f'  <text x="150" y="250" fill="{ORANGE}" font-family="Inter, Arial, sans-serif" font-size="34" font-weight="760">4 steps</text>\n'
        + f'  <text x="780" y="184" fill="{BLUE}" font-family="Inter, Arial, sans-serif" font-size="32" font-weight="760">128-step reference</text>\n'
        + f'  <circle cx="140" cy="505" r="18" fill="{BLUE}"/>\n'
        + f'  <circle cx="1080" cy="218" r="18" fill="{TEAL}"/>\n'
        + f'  <text x="415" y="560" fill="{TEXT}" font-family="Inter, Arial, sans-serif" font-size="35" font-weight="700">same field, different numerical path</text>\n'
        + footer()
    )


def part3() -> str:
    arrows = ""
    starts = [(300, 390), (335, 455), (365, 330), (412, 418), (455, 350), (486, 456)]
    ends = [(420, 335), (470, 420), (520, 300), (565, 380), (600, 325), (650, 430)]
    for (x1, y1), (x2, y2) in zip(starts, ends):
        arrows += f'  <path d="M{x1} {y1} L{x2} {y2}" stroke="{MUTED}" stroke-width="5" stroke-linecap="round" opacity="0.72" marker-end="url(#arrow)"/>\n'
    return (
        header(3, "POPULATION VIEW", "Average local velocities", "Many endpoint-conditioned arrows become the marginal direction used by sampling.")
        + arrow_defs()
        + f'  <circle cx="470" cy="390" r="165" fill="#22304A" stroke="{PURPLE}" stroke-width="4" stroke-dasharray="10 12"/>\n'
        + arrows
        + f'  <circle cx="470" cy="390" r="16" fill="{ROSE}"/>\n'
        + f'  <path d="M735 392 L970 318" stroke="{TEAL}" stroke-width="16" stroke-linecap="round" marker-end="url(#arrow-teal)"/>\n'
        + f'  <text x="710" y="460" fill="{TEAL}" font-family="Inter, Arial, sans-serif" font-size="36" font-weight="760">local average field</text>\n'
        + f'  <text x="252" y="575" fill="{MUTED}" font-family="Inter, Arial, sans-serif" font-size="28">conditional samples near x,t</text>\n'
        + footer()
    )


def part4() -> str:
    left_a = [(150, 360), (170, 435), (205, 500), (245, 392)]
    left_b = [(430, 345), (460, 472), (506, 398), (520, 535)]
    right_a = [(685, 360), (705, 435), (740, 500), (780, 392)]
    right_b = [(940, 355), (958, 425), (1000, 488), (1025, 542)]
    lines = ""
    for i, j in [(0, 2), (1, 0), (2, 3), (3, 1)]:
        lines += f'  <path d="M{left_a[i][0]} {left_a[i][1]} L{left_b[j][0]} {left_b[j][1]}" stroke="{ROSE}" stroke-width="5" opacity="0.8"/>\n'
    for i, j in [(0, 0), (1, 1), (2, 2), (3, 3)]:
        lines += f'  <path d="M{right_a[i][0]} {right_a[i][1]} L{right_b[j][0]} {right_b[j][1]}" stroke="{TEAL}" stroke-width="5" opacity="0.9"/>\n'
    return (
        header(4, "COUPLING", "Pairing shapes paths", "Endpoint assignment controls path length, crossings, and transport cost.")
        + f'  <rect x="105" y="240" width="470" height="350" rx="22" fill="#111827" stroke="#344155"/>\n'
        + f'  <rect x="625" y="240" width="470" height="350" rx="22" fill="#111827" stroke="#344155"/>\n'
        + lines
        + dots(left_a, BLUE, 12)
        + dots(left_b, ORANGE, 12)
        + dots(right_a, BLUE, 12)
        + dots(right_b, ORANGE, 12)
        + f'  <text x="145" y="305" fill="{ROSE}" font-family="Inter, Arial, sans-serif" font-size="34" font-weight="760">random pairing</text>\n'
        + f'  <text x="675" y="305" fill="{TEAL}" font-family="Inter, Arial, sans-serif" font-size="34" font-weight="760">minibatch OT</text>\n'
        + footer()
    )


def part5() -> str:
    row = ""
    for y, color in [(305, TEAL), (465, PURPLE)]:
        for x in [225, 390, 555, 720, 885]:
            row += f'  <circle cx="{x}" cy="{y}" r="34" fill="{color}" opacity="0.18" stroke="{color}" stroke-width="4"/>\n'
        row += f'  <path d="M225 {y} C390 {y-75} 555 {y+75} 720 {y-35} C790 {y-60} 850 {y-18} 885 {y}" fill="none" stroke="{color}" stroke-width="7" stroke-linecap="round"/>\n'
    return (
        header(5, "PATH DESIGN", "Choose the path", "The same endpoints can travel through different intermediate distributions.")
        + row
        + f'  <text x="110" y="316" fill="{TEAL}" font-family="Inter, Arial, sans-serif" font-size="32" font-weight="760">CondOT</text>\n'
        + f'  <text x="110" y="476" fill="{PURPLE}" font-family="Inter, Arial, sans-serif" font-size="32" font-weight="760">Linear VP</text>\n'
        + f'  <text x="290" y="570" fill="{MUTED}" font-family="Inter, Arial, sans-serif" font-size="29">matched t slices on shared axes</text>\n'
        + footer()
    )


def part6() -> str:
    blocks = [(135, "path"), (335, "scheduler"), (565, "loss"), (735, "model"), (930, "solver")]
    body = ""
    for x, label in blocks:
        body += f'  <rect x="{x}" y="300" width="155" height="92" rx="18" fill="#101827" stroke="#40506A" stroke-width="3"/>\n'
        body += f'  <text x="{x+78}" y="357" text-anchor="middle" fill="{TEXT}" font-family="Inter, Arial, sans-serif" font-size="27" font-weight="760">{label}</text>\n'
    for x1, x2 in [(290, 335), (490, 565), (720, 735), (890, 930)]:
        body += f'  <path d="M{x1} 346 L{x2} 346" stroke="{MUTED}" stroke-width="5" marker-end="url(#arrow)"/>\n'
    return (
        header(6, "OFFICIAL API", "Official API, explained", "The tutorial objects map cleanly to path, scheduler, loss, model, and solver components.")
        + arrow_defs()
        + body
        + f'  <path d="M300 490 C445 555 730 555 915 480" fill="none" stroke="{TEAL}" stroke-width="8" stroke-linecap="round"/>\n'
        + f'  <circle cx="980" cy="470" r="44" fill="#052E2B" stroke="{TEAL}" stroke-width="5"/>\n'
        + f'  <path d="M958 470 L977 489 L1010 445" fill="none" stroke="{TEAL}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>\n'
        + f'  <text x="350" y="565" fill="{TEAL}" font-family="Inter, Arial, sans-serif" font-size="34" font-weight="760">verified continuous smoke test</text>\n'
        + footer()
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    svgs = {
        "flow-matching-card-part-1.svg": part1(),
        "flow-matching-card-part-2.svg": part2(),
        "flow-matching-card-part-3.svg": part3(),
        "flow-matching-card-part-4.svg": part4(),
        "flow-matching-card-part-5.svg": part5(),
        "flow-matching-card-part-6.svg": part6(),
    }
    for name, svg in svgs.items():
        (OUT / name).write_text(svg)
        print(OUT / name)


if __name__ == "__main__":
    main()
