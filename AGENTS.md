# AGENTS.md

Onboarding for an AI agent (or human) working **on the prompt-optimizer repository**.

> This file is about *developing prompt-optimizer*. It is distinct from the `/p`
> command the plugin ships (`commands/p.md`), which is the product.

## Purpose

prompt-optimizer ships a single Claude Code slash command, `/p`, that rewrites the
user's request into an optimized prompt (structured context, specificity,
meta-instructions for extended thinking, and skip-comments that preserve quoted text)
and then immediately executes that optimized prompt.

## Structure map

```
commands/p.md                          the /p command — the whole product
.claude-plugin/plugin.json             plugin manifest
.claude-plugin/marketplace.json        marketplace metadata (one-line install)
scripts/validate-plugin.sh             green-bar check: manifests + command + leak scan
scripts/svgkit.py                      zero-dependency SVG toolkit (palette, nodes, flows)
scripts/generate-architecture-svg.py   regenerates assets/architecture.svg from svgkit
scripts/generate-terminals.py          regenerates assets/term-*.svg (README screenshots)
assets/architecture.svg                generated diagram (do not hand-edit)
assets/term-*.svg                      generated terminal "screenshots" (do not hand-edit)
docs/architecture.md                   how the command flows, embeds the diagram
docs/PUBLISHING.md                     how to publish/update the plugin
.github/workflows/                     ci (validate), codeql (actions), scorecard, release
```

## Invariants (keep green)

```bash
bash scripts/validate-plugin.sh        # manifests valid, versions agree, command ok, no leaks
```

CI runs exactly this. A change that breaks it is not merge-ready.

## Conventions

- **Never hand-edit `assets/architecture.svg`.** It is generated — change
  `scripts/generate-architecture-svg.py` (or `svgkit.py`) and rerun
  `python3 scripts/generate-architecture-svg.py`.
- **Bump `version` in both manifests** for any user-facing change; the two must match.
- **No code, no deps, no hooks.** The plugin's value is being a single, auditable,
  code-free command. Keep it that way.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the PR workflow and
[docs/architecture.md](docs/architecture.md) for the design.
