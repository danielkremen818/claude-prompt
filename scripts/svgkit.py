#!/usr/bin/env python3
"""
svgkit — the shared, zero-dependency brand-SVG toolkit for prompt-optimizer's docs.

Pure Python standard library (string building only — no XML/jinja/etc.) so it runs with
`python3` and adds no dependencies. It is the single home for the prompt-optimizer visual
language used by the generated architecture diagram:

  - the brand palette (warm clay/amber accents on an ink canvas — the "rewrite then run" feel)
  - rounded node cards (accent stroke + pulsing dot) drawn with stroke-only Feather glyphs
  - subsystem boxes (radial-gradient backdrops)
  - curved + straight animated data-flow edges (arrow markers + a moving dash overlay)
  - the dark radial canvas + prefers-color-scheme light/dark CSS
  - the standard heading and "regenerate via scripts/..." footer

One generator imports from here:
  - scripts/generate-architecture-svg.py  -> assets/architecture.svg

Offline by design: no network, no third-party packages, no external icon files (glyphs are
inline below).
"""
from __future__ import annotations

# ── brand palette ───────────────────────────────────────────────────────────
CLAY = "#d97757"     # Claude / the execute step — the warm signature accent
AMBER = "#fbbf24"    # the "optimize" transform
GOLD = "#f4b860"     # show / reveal
CYAN = "#22d3ee"     # structured context
TEAL = "#2dd4bf"     # specificity
VIOLET = "#a78bfa"   # meta-instructions / extended thinking
PINK = "#f472b6"     # skip-comments (preserve quotes)
GREEN = "#34d399"    # result
SLATE = "#94a3b8"    # neutral / support / install surface
INK = "#e7d8c9"      # request text

ALL_COLORS = (CLAY, AMBER, GOLD, CYAN, TEAL, VIOLET, PINK, GREEN, SLATE, INK)

NODE_FILL = "rgba(28, 16, 10, 0.62)"

# Feather-style glyphs (MIT), stroke-rendered.
GLYPHS = {
    "user": (
        '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>'
        '<circle cx="12" cy="7" r="4"/>'
    ),
    "edit": (
        '<path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>'
        '<path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>'
    ),
    "eye": (
        '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>'
        '<circle cx="12" cy="12" r="3"/>'
    ),
    "play": '<polygon points="5 3 19 12 5 21 5 3"/>',
    "layers": (
        '<polygon points="12 2 2 7 12 12 22 7 12 2"/>'
        '<polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>'
    ),
    "target": (
        '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/>'
        '<circle cx="12" cy="12" r="2"/>'
    ),
    "cpu": (
        '<rect x="4" y="4" width="16" height="16" rx="2" ry="2"/>'
        '<rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/>'
        '<line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/>'
        '<line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/>'
        '<line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/>'
        '<line x1="1" y1="14" x2="4" y2="14"/>'
    ),
    "quote": (
        '<path d="M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 '
        '1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1z"/>'
        '<path d="M15 21c3 0 7-1 7-8V5c0-1.25-.757-2.017-2-2h-4c-1.25 0-2 .75-2 '
        '1.972V11c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3c0 1 0 1 1 1z"/>'
    ),
    "command": (
        '<path d="M18 3a3 3 0 0 0-3 3v12a3 3 0 1 0 3-3H6a3 3 0 1 0 3 3V6a3 3 0 1 '
        '0-3 3h12a3 3 0 0 0 0-6z"/>'
    ),
    "package": (
        '<line x1="16.5" y1="9.4" x2="7.5" y2="4.21"/>'
        '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 '
        '2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>'
        '<polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/>'
    ),
    "check-circle": (
        '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>'
        '<polyline points="22 4 12 14.01 9 11.01"/>'
    ),
    "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
}


def esc(s: str) -> str:
    """Escape text for use in SVG text nodes."""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def glyph_markup(kind: str, *, x: float, y: float, size: float, color: str) -> str:
    s = size / 24.0
    return (
        f'<g transform="translate({x} {y}) scale({s:.4f})" fill="none" '
        f'stroke="{color}" stroke-width="2" stroke-linecap="round" '
        f'stroke-linejoin="round">{GLYPHS[kind]}</g>'
    )


# ── geometry helpers ─────────────────────────────────────────────────────────
def subsystem_box(*, x, y, w, h, title, fill_id, stroke) -> str:
    return (
        f'<g class="subsystem">'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" '
        f'fill="url(#{fill_id})" stroke="{stroke}" stroke-width="1.5"/>'
        f'<text x="{x + 18}" y="{y + 28}" class="title">{esc(title)}</text></g>'
    )


def node(*, cx, cy, label, sublabel, accent, glyph, w=210) -> str:
    """A node card: 34px stroke glyph + bold label + dim sublabel + pulsing dot."""
    left = cx - w / 2
    icon = glyph_markup(glyph, x=left + 8, y=cy - 17, size=34, color=accent)
    return (
        f"<g>"
        f'<rect x="{left}" y="{cy - 30}" width="{w}" height="74" rx="11" '
        f'fill="{NODE_FILL}" stroke="{accent}" stroke-width="1" stroke-opacity="0.5"/>'
        f"{icon}"
        f'<text x="{left + 54}" y="{cy - 3}" class="node-label">{esc(label)}</text>'
        f'<text x="{left + 54}" y="{cy + 16}" class="node-sub">{esc(sublabel)}</text>'
        f'<g transform="translate({cx + w / 2 - 10}, {cy - 20})">'
        f'<circle r="4" fill="{accent}">'
        f'<animate attributeName="r" values="3;7;3" dur="2.4s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="1;0.35;1" dur="2.4s" repeatCount="indefinite"/>'
        f'</circle><circle r="3" fill="{accent}"/></g>'
        f"</g>"
    )


def curve(x1, y1, x2, y2, bend=0.5) -> str:
    """A horizontal-leaning cubic between two points (control points on a vertical seam)."""
    mx = x1 + (x2 - x1) * bend
    return f"M {x1} {y1} C {mx} {y1}, {mx} {y2}, {x2} {y2}"


def vcurve(x1, y1, x2, y2, bend=0.5) -> str:
    """A vertical-leaning cubic between two points (control points on a horizontal seam)."""
    my = y1 + (y2 - y1) * bend
    return f"M {x1} {y1} C {x1} {my}, {x2} {my}, {x2} {y2}"


def flow(*, d, color, label=None, label_pos=None, dashed=False, dur="2.2s") -> str:
    dash = 'stroke-dasharray="6 6"' if dashed else ""
    base = (
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2" '
        f'stroke-opacity="0.5" stroke-linecap="round" {dash} '
        f'marker-end="url(#arrow-{color.strip("#")})"/>'
    )
    overlay = (
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2" '
        f'stroke-linecap="round" stroke-dasharray="2 14" stroke-opacity="0.95">'
        f'<animate attributeName="stroke-dashoffset" values="0;-32" dur="{dur}" '
        f'repeatCount="indefinite"/></path>'
    )
    out = base + overlay
    if label and label_pos:
        out += edge_label(label, label_pos[0], label_pos[1], color)
    return out


def edge_label(label: str, lx: float, ly: float, color: str) -> str:
    w = max(54, len(label) * 6.6 + 16)
    return (
        f'<g transform="translate({lx} {ly})">'
        f'<rect x="{-w/2:.1f}" y="-11" width="{w:.1f}" height="22" rx="6" '
        f'fill="rgba(12, 7, 4, 0.88)" stroke="{color}" stroke-opacity="0.45"/>'
        f'<text x="0" y="4" class="edge-label" text-anchor="middle">{esc(label)}</text></g>'
    )


def gradient(id_, c0, c1) -> str:
    return (
        f'<linearGradient id="{id_}" x1="0%" y1="0%" x2="0%" y2="100%">'
        f'<stop offset="0%" stop-color="{c0}" stop-opacity="0.9"/>'
        f'<stop offset="100%" stop-color="{c1}" stop-opacity="0.55"/></linearGradient>'
    )


def arrow_marker(color) -> str:
    cid = color.strip("#")
    return (
        f'<marker id="arrow-{cid}" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>'
    )


# ── the shared CSS (dark default + prefers-color-scheme light) ────────────────
CSS = """
    .title      { font: 700 13px "Iosevka", ui-monospace, SFMono-Regular, Menlo, monospace;
                  fill: #f6c89a; letter-spacing: 0.09em; text-transform: uppercase; }
    .h1         { font: 700 20px "Iosevka", ui-monospace, Menlo, monospace; fill: #fbeee4; letter-spacing: 0.14em; }
    .node-label { font: 600 13.5px ui-monospace, SFMono-Regular, Menlo, monospace; fill: #fdf6ef; }
    .node-sub   { font: 500 10.5px -apple-system, system-ui, sans-serif; fill: #c4a78f; }
    .edge-label { font: 600 10px -apple-system, system-ui, sans-serif; fill: #fdf6ef; }
    .legend     { font: 500 12px -apple-system, system-ui, sans-serif; fill: #c4a78f; }
    .legend-h   { font: 700 12px ui-monospace, Menlo, monospace; fill: #f6c89a; letter-spacing: 0.06em; text-transform: uppercase; }
    .footer     { font: 500 10px ui-monospace, Menlo, monospace; fill: #8c7257; }

    @media (prefers-color-scheme: light) {
      .title      { fill: #b45309; }
      .h1         { fill: #7c2d12; }
      .node-label { fill: #431407; }
      .node-sub   { fill: #9a3412; }
      .edge-label { fill: #431407; }
      .legend     { fill: #9a3412; }
      .legend-h   { fill: #b45309; }
      .footer     { fill: #a16207; }
    }
"""


# ── document scaffolding (canvas, defs, heading, footer) ──────────────────────
def svg_open(w, h, aria) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{esc(aria)}">'
        f"<style>{CSS}</style>"
    )


def defs(colors=ALL_COLORS, *, gradients=None) -> str:
    P = ["<defs>"]
    P.append(
        '<radialGradient id="bg-canvas" cx="50%" cy="0%" r="120%">'
        '<stop offset="0%" stop-color="#241310"/>'
        '<stop offset="100%" stop-color="#0c0705"/></radialGradient>'
    )
    if gradients:
        for gid, c0, c1 in gradients:
            P.append(gradient(gid, c0, c1))
    for c in colors:
        P.append(arrow_marker(c))
    P.append("</defs>")
    return "".join(P)


def canvas(w, h) -> str:
    return f'<rect width="{w}" height="{h}" fill="url(#bg-canvas)"/>'


def footer(w, h, out_name, *, script) -> str:
    return (
        f'<text x="{w - 16}" y="{h - 8}" text-anchor="end" class="footer">'
        f"assets/{out_name} · regenerate via {script}</text>"
    )
