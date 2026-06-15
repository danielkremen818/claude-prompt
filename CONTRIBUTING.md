# Contributing to prompt-optimizer

Thanks for your interest. prompt-optimizer is deliberately tiny — one slash command
that rewrites a request, then runs it. Contributions that keep it small and focused
are very welcome.

## Project layout

```
commands/p.md              the /p command — the whole product
.claude-plugin/            plugin.json + marketplace.json (manifests)
scripts/validate-plugin.sh the green-bar check (manifests, command, leak scan)
scripts/svgkit.py          zero-dependency SVG toolkit for the docs diagram
scripts/generate-architecture-svg.py  regenerates assets/architecture.svg
assets/architecture.svg    the generated architecture diagram
docs/                      architecture, publishing
```

`commands/p.md` is the product. Everything else is packaging, docs, and CI.

## The green-bar invariant

Every change must keep this green:

```bash
bash scripts/validate-plugin.sh
```

That checks the manifests are valid JSON, the two version strings agree, the command
file is well-formed, and **no private data has leaked** into a tracked file. CI runs
exactly this script; a PR that breaks it won't be merged.

If you change the command flow, regenerate the diagram and commit it:

```bash
python3 scripts/generate-architecture-svg.py   # writes assets/architecture.svg
```

## Trying it locally

Point Claude Code at your working copy:

```
/plugin marketplace add /path/to/your/clone/prompt-optimizer
/plugin install prompt-optimizer@prompt-optimizer
```

Then run `/p <something>` and confirm the two-part (optimize → execute) behavior.

## Scope

prompt-optimizer does one thing. Please don't grow it into a general prompt toolkit,
add dependencies, or add hooks/scripts that run code on the user's machine — the
plugin's value is that it's a single, auditable, code-free command. See the README's
intro for the boundary.

## Pull requests

- Fork the repo and open a PR against `main`. **PRs from forks are welcome.**
- Only the maintainer (**@danielkremen818**) merges to `main`.
- Keep the PR focused; bump `version` in **both** manifests for user-facing changes,
  update `CHANGELOG.md` under `## [Unreleased]`, and make sure the green-bar check
  passes before requesting review.
