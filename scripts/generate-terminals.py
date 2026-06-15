#!/usr/bin/env python3
"""
Render polished "mac-window" terminal SVGs of a /claude-prompt:p session for the README.

claude-prompt has no CLI to capture (the product is a prompt, not a program), so the
panels below are authored content — a faithful mock of what a `/claude-prompt:p` run looks like in
Claude Code. The window chrome (gradient frame, traffic lights, titlebar, glow) mirrors
the terminal images in the author's ultracost project, retinted to the warm clay/amber
brand used by assets/architecture.svg.

Offline + zero-dependency (pure Python stdlib). Run from the repo root:
    python3 scripts/generate-terminals.py

Output: assets/term-demo.svg, assets/term-skip-comments.svg
"""
from __future__ import annotations

import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "assets"

# ── terminal geometry / theme ─────────────────────────────────────────────────
FONT = 13
CELL_W = 8.0       # ui-monospace advance at 13px, with a hair of slack
LINE_H = 19
PADX = 22
TITLEBAR_H = 36
BODY_TOP_PAD = 16
BODY_BOT_PAD = 16

BG = "#100a07"          # warm near-black canvas
TITLEBAR = "#1c1410"
BASE_TEXT = "#e7d8c9"
TITLE_TEXT = "#c4a78f"
DOT_RED = "#fb7185"
DOT_AMBER = "#fbbf24"
DOT_GREEN = "#34d399"

# content palette
GREEN = "#34d399"
CLAY = "#d97757"
GOLD = "#f4b860"
AMBER = "#fbbf24"
CYAN = "#22d3ee"
TEAL = "#2dd4bf"
PINK = "#f472b6"
DIM = "#8c7257"

# frame gradient (warm brand)
FRAME_A, FRAME_B, FRAME_C = "#d97757", "#fbbf24", "#f4b860"


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        .replace('"', "&quot;").replace("'", "&#39;")
    )


def r(text, color=None, bold=False, dim=False, italic=False):
    """A styled run."""
    return {"text": text, "fg": color, "bold": bold, "dim": dim, "italic": italic}


def run_span(run) -> str:
    attrs = [f'fill="{run["fg"] or BASE_TEXT}"']
    if run["bold"]:
        attrs.append('font-weight="700"')
    if run["italic"]:
        attrs.append('font-style="italic"')
    if run["dim"]:
        attrs.append('opacity="0.62"')
    return f'<tspan {" ".join(attrs)}>{esc(run["text"])}</tspan>'


def build_svg(title: str, lines: list[list[dict]]) -> str:
    plain = ["".join(run["text"] for run in ln) for ln in lines]
    cols = max(34, max((len(s) for s in plain), default=0), len(title) + 6)
    W = round(PADX * 2 + cols * CELL_W)
    body_top = TITLEBAR_H + BODY_TOP_PAD
    H = round(body_top + len(lines) * LINE_H + BODY_BOT_PAD)

    P = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, '
        f"'Liberation Mono', monospace\" "
        f'role="img" aria-label="claude-prompt terminal: {esc(title)}">'
    ]
    P.append(
        "<defs>"
        f'<linearGradient id="frame" x1="0%" y1="0%" x2="100%" y2="100%">'
        f'<stop offset="0%" stop-color="{FRAME_A}"/>'
        f'<stop offset="55%" stop-color="{FRAME_B}"/>'
        f'<stop offset="100%" stop-color="{FRAME_C}"/></linearGradient>'
        f'<radialGradient id="glow" cx="22%" cy="0%" r="90%">'
        f'<stop offset="0%" stop-color="{CLAY}" stop-opacity="0.16"/>'
        f'<stop offset="60%" stop-color="{CLAY}" stop-opacity="0"/></radialGradient>'
        f'<clipPath id="screen"><rect x="1.5" y="1.5" width="{W - 3}" '
        f'height="{H - 3}" rx="11"/></clipPath>'
        "</defs>"
    )
    P.append(
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="11.5" '
        f'fill="{BG}" stroke="url(#frame)" stroke-width="1.5"/>'
    )
    P.append('<g clip-path="url(#screen)">')
    P.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#glow)"/>')
    P.append(f'<rect x="1.5" y="1.5" width="{W - 3}" height="{TITLEBAR_H}" rx="11" fill="{TITLEBAR}"/>')
    P.append(f'<rect x="1.5" y="{TITLEBAR_H - 8}" width="{W - 3}" height="10" fill="{TITLEBAR}"/>')
    P.append(f'<line x1="0" y1="{TITLEBAR_H + 1.5}" x2="{W}" y2="{TITLEBAR_H + 1.5}" stroke="#000" stroke-opacity="0.35"/>')
    P.append(f'<circle cx="24" cy="{TITLEBAR_H / 2 + 1}" r="5.5" fill="{DOT_RED}"/>')
    P.append(f'<circle cx="44" cy="{TITLEBAR_H / 2 + 1}" r="5.5" fill="{DOT_AMBER}"/>')
    P.append(f'<circle cx="64" cy="{TITLEBAR_H / 2 + 1}" r="5.5" fill="{DOT_GREEN}"/>')
    P.append(
        f'<text x="{W / 2}" y="{TITLEBAR_H / 2 + 5}" text-anchor="middle" '
        f'font-size="11" fill="{TITLE_TEXT}" letter-spacing="0.04em">{esc(title)}</text>'
    )
    P.append(f'<text font-size="{FONT}" xml:space="preserve">')
    for i, runs in enumerate(lines):
        y = body_top + i * LINE_H + 13
        content = "".join(run_span(run) for run in runs) if runs else " "
        P.append(f'<tspan x="{PADX}" y="{y}">{content}</tspan>')
    P.append("</text></g></svg>")
    return "\n".join(P)


# ── panels ────────────────────────────────────────────────────────────────────
def demo_panel() -> list[list[dict]]:
    return [
        [r("> ", GREEN, bold=True), r("/claude-prompt:p add rate limiting to the login endpoint", GOLD)],
        [],
        [r("Optimized prompt:", GOLD, bold=True)],
        [r("Add rate limiting to the ", ), r("POST /login", CYAN), r(" endpoint.")],
        [r("1. ", CYAN), r("Pick a strategy (fixed-window vs token-bucket); justify it.")],
        [r("2. ", CYAN), r("Write a failing test: 6 hits / 60s -> 429.  "), r("verify:", TEAL), r(" red")],
        [r("3. ", CYAN), r("Add middleware so the test passes.          "), r("verify:", TEAL), r(" green")],
        [r("4. ", CYAN), r("Return Retry-After; log throttled attempts.")],
        [r("Success: ", DIM), r("brute force capped, valid logins unaffected.", dim=True)],
        [],
        [r("●", CLAY), r(" Executing the optimized prompt…", CLAY)],
        [r("✓ ", GREEN), r("tests/login.rate.test.ts"), r("   6/min -> 429", dim=True)],
        [r("✓ ", GREEN), r("middleware/rateLimit.ts"), r("    token-bucket", dim=True)],
        [r("✓ ", GREEN), r("12 passed", bold=True), r("   valid login flow unchanged", dim=True)],
    ]


def skip_comments_panel() -> list[list[dict]]:
    return [
        [r("> ", GREEN, bold=True), r('/claude-prompt:p rename the CTA to ', GOLD),
         r('"Get started — it’s free"', PINK), r(" everywhere", GOLD)],
        [],
        [r("Optimized prompt:", GOLD, bold=True)],
        [r("Replace the call-to-action label across the app.")],
        [r("• ", CLAY), r("Find every render of the CTA (button, hero, nav).")],
        [r("• ", CLAY), r("Set the label to exactly "), r('"Get started — it’s free"', PINK),
         r(".")],
        [r("• ", CLAY), r("Leave behavior and styling untouched.")],
        [],
        [r("skip-comments: ", TEAL, bold=True),
         r('the quoted string is preserved verbatim', dim=True)],
        [r('— em dash, curly apostrophe and all.', dim=True)],
    ]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    panels = [
        ("term-demo.svg", "claude — /claude-prompt:p prompt optimizer", demo_panel()),
        ("term-skip-comments.svg", "claude — /claude-prompt:p skip-comments", skip_comments_panel()),
    ]
    for fname, title, lines in panels:
        out = OUT_DIR / fname
        svg = build_svg(title, lines)
        out.write_text(svg + "\n")
        print(f"wrote {out} ({len(svg)} bytes)", file=sys.stderr)


if __name__ == "__main__":
    main()
