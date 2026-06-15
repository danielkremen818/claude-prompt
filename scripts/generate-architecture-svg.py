#!/usr/bin/env python3
"""
Generate assets/architecture.svg — the animated "live architecture" diagram for the
README and docs/architecture.md.

Hand-crafted (not mermaid) so we get a living system map:
  - SMIL data-flow animation on every edge (stroke-dashoffset)
  - pulsing endpoint dots on every active node
  - subtle radial-gradient subsystem backdrops in the warm clay/amber theme
  - lightweight Feather-style glyphs (MIT), stroke-rendered
  - dark + light rendering via prefers-color-scheme

What it depicts (precise to the actual plugin):
  - the INSTALL SURFACE: the two manifests in .claude-plugin/ + commands/p.md, installed
    via the marketplace into a live /p command
  - the /p RUN: your request ($ARGUMENTS) -> Step 1 Optimize -> Step 2 Show -> Step 3 Execute
  - the four OPTIMIZE techniques applied during Step 1 (structured context, specificity,
    meta-instructions, skip-comments) feeding the optimize step
  - the OUTPUT: the shown "Optimized prompt:" block, then the executed result

Offline by design: no network, no third-party packages, no external icon files.

The brand primitives (palette, node cards, flows, subsystem boxes, CSS) live in
scripts/svgkit.py.

Run from the repo root:
    python3 scripts/generate-architecture-svg.py

Output: assets/architecture.svg
"""
from __future__ import annotations

import pathlib
import sys

from svgkit import (
    ALL_COLORS,
    AMBER,
    CLAY,
    CYAN,
    GOLD,
    GREEN,
    INK,
    PINK,
    SLATE,
    TEAL,
    VIOLET,
    canvas,
    curve,
    defs,
    flow,
    footer,
    node,
    subsystem_box,
    svg_open,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_PATH = REPO_ROOT / "assets" / "architecture.svg"

W, H = 1500, 920


def build_svg() -> str:
    P = [svg_open(W, H, "claude-prompt architecture diagram")]

    P.append(
        defs(
            ALL_COLORS,
            gradients=[
                ("bg-install", "#2a2018", "#140e09"),
                ("bg-run", "#3a2417", "#1b0f08"),
                ("bg-tech", "#2d2620", "#161009"),
                ("bg-out", "#142a20", "#08160f"),
            ],
        )
    )

    P.append(canvas(W, H))
    P.append('<text x="40" y="50" class="h1">CLAUDE-PROMPT &#183; LIVE ARCHITECTURE</text>')
    P.append(
        '<text x="40" y="76" class="legend">'
        "One command (commands/p.md) &#8594; read &amp; gate the request &#8226; rewrite with four "
        "techniques &#8226; show the optimized prompt &#8226; then carry it out &#8226; dots are live"
        "</text>"
    )

    # ── subsystem boxes ───────────────────────────────────────────────
    P.append(subsystem_box(x=40, y=110, w=300, h=560, title="Install surface · the plugin",
                           fill_id="bg-install", stroke="#b08968"))
    P.append(subsystem_box(x=380, y=110, w=420, h=700, title="PROMPT OPTIMIZER mode · /p",
                           fill_id="bg-run", stroke=CLAY))
    P.append(subsystem_box(x=840, y=110, w=620, h=300, title="Step 1 · optimize with 4 techniques",
                           fill_id="bg-tech", stroke=AMBER))
    P.append(subsystem_box(x=840, y=450, w=620, h=220, title="Output",
                           fill_id="bg-out", stroke=GREEN))

    # ── nodes ──────────────────────────────────────────────────────────
    # Install surface (left column)
    LX = 190
    P.append(node(cx=LX, cy=200, glyph="package", label=".claude-plugin/",
                  sublabel="plugin.json · marketplace.json", accent=SLATE))
    P.append(node(cx=LX, cy=340, glyph="command", label="commands/p.md",
                  sublabel="the /p definition", accent=CLAY))
    P.append(node(cx=LX, cy=480, glyph="zap", label="/plugin install",
                  sublabel="claude-prompt", accent=AMBER))

    # The /p run (center column)
    CX = 590
    P.append(node(cx=CX, cy=185, glyph="user", label="your request", w=240,
                  sublabel="/p [--dry] <request>", accent=INK))
    P.append(node(cx=CX, cy=315, glyph="filter", label="Step 0 · Read", w=240,
                  sublabel="type · clarity · stakes", accent=PINK))
    P.append(node(cx=CX, cy=445, glyph="edit", label="Step 1 · Optimize", w=240,
                  sublabel="rewrite for reasoning", accent=AMBER))
    P.append(node(cx=CX, cy=575, glyph="eye", label="Step 2 · Show", w=240,
                  sublabel="Optimized prompt:", accent=GOLD))
    P.append(node(cx=CX, cy=705, glyph="play", label="Step 3 · Execute", w=240,
                  sublabel="clear asks run one-shot", accent=CLAY))

    # The four techniques (right-top)
    P.append(node(cx=985, cy=200, glyph="layers", label="structured context", w=270,
                  sublabel="frameworks · step-by-step", accent=CYAN))
    P.append(node(cx=985, cy=320, glyph="cpu", label="meta-instructions", w=270,
                  sublabel="extended thinking + plan", accent=VIOLET))
    P.append(node(cx=1300, cy=200, glyph="target", label="specificity", w=270,
                  sublabel="success criteria", accent=TEAL))
    P.append(node(cx=1300, cy=320, glyph="quote", label="skip-comments", w=270,
                  sublabel='"quoted" text untouched', accent=PINK))

    # Output (right-bottom)
    P.append(node(cx=985, cy=560, glyph="check-circle", label="optimized prompt", w=270,
                  sublabel="shown to you", accent=GOLD))
    P.append(node(cx=1300, cy=560, glyph="zap", label="the result", w=270,
                  sublabel="work, done", accent=GREEN))

    # ── flows ───────────────────────────────────────────────────────────
    # install surface internal
    P.append(flow(d="M 190 244 L 190 310", color=SLATE, label="ships", label_pos=(190, 280), dur="2.4s"))
    P.append(flow(d="M 190 384 L 190 450", color=CLAY, label="install", label_pos=(190, 420), dur="2.2s"))
    # install -> /p available (enables the run)
    P.append(flow(d=curve(300, 470, 470, 190, 0.55), color=AMBER,
                  label="enables /p", label_pos=(388, 300), dur="2.8s"))

    # center vertical chain
    P.append(flow(d="M 590 229 L 590 285", color=INK, label="read", label_pos=(590, 257), dur="2.0s"))
    P.append(flow(d="M 590 359 L 590 415", color=PINK, dur="2.0s"))
    P.append(flow(d="M 590 489 L 590 545", color=AMBER, label="rewrite", label_pos=(590, 517), dur="2.0s"))
    P.append(flow(d="M 590 619 L 590 675", color=GOLD, label="then run", label_pos=(590, 647), dur="2.0s"))
    # Step 0 gate — clarify/confirm loops back to the user only when warranted
    P.append(flow(d="M 470 315 C 432 280, 432 220, 470 185", color=PINK,
                  label="clarify / confirm", label_pos=(432, 250), dur="2.6s"))

    # the four techniques feed Step 1 Optimize (converge on the optimize node, x=710)
    P.append(flow(d=curve(850, 200, 712, 435, 0.5), color=CYAN, label="applied", label_pos=(800, 300), dur="2.6s"))
    P.append(flow(d=curve(850, 320, 712, 447, 0.5), color=VIOLET, dur="2.4s"))
    P.append(flow(d=curve(1165, 210, 716, 441, 0.7), color=TEAL, dur="3.0s"))
    P.append(flow(d=curve(1165, 330, 716, 453, 0.7), color=PINK, dur="3.2s"))

    # Step 2 Show -> optimized prompt block
    P.append(flow(d=curve(710, 575, 850, 558, 0.5), color=GOLD, label="reveal", label_pos=(782, 552), dur="2.2s"))
    # Step 3 Execute -> the result
    P.append(flow(d="M 710 705 C 980 705, 1180 660, 1290 600", color=CLAY,
                  label="carry out", label_pos=(1010, 706), dur="2.8s"))
    # optimized prompt -> result (the same optimized prompt is what gets executed)
    P.append(flow(d="M 1120 560 L 1166 560", color=GREEN, dur="2.0s"))

    # ── flow legend ─────────────────────────────────────────────────────
    ly = 892
    P.append(f'<text x="40" y="{ly}" class="legend-h">FLOW</text>')
    items = [
        (SLATE, "ship / install"),
        (PINK, "read / gate"),
        (AMBER, "optimize"),
        (CYAN, "techniques applied"),
        (GOLD, "show"),
        (CLAY, "execute"),
        (GREEN, "result"),
    ]
    lx = 120
    for color, txt in items:
        P.append(
            f'<line x1="{lx}" y1="{ly - 4}" x2="{lx + 26}" y2="{ly - 4}" '
            f'stroke="{color}" stroke-width="3" stroke-linecap="round"/>'
        )
        P.append(f'<text x="{lx + 33}" y="{ly}" class="legend">{txt}</text>')
        lx += max(150, len(txt) * 7 + 64)

    P.append(footer(W, H, "architecture.svg", script="scripts/generate-architecture-svg.py"))
    P.append("</svg>")
    return "\n".join(P)


def main() -> None:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(build_svg())
    print(f"wrote {OUT_PATH} ({OUT_PATH.stat().st_size} bytes)", file=sys.stderr)


if __name__ == "__main__":
    main()
