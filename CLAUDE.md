# CLAUDE.md

This file guides AI agents (and humans) working **on the prompt-optimizer repository
itself**.

See [AGENTS.md](AGENTS.md) for the full repo development guidance: the structure map,
the green-bar invariant, and the conventions to keep.

> **Not** to be confused with the `/p` command this plugin ships (`commands/p.md`),
> which is the product — the prompt sent to Claude when a user runs `/p`. This file is
> about developing the plugin, not about using it.

Quick rules:

- Keep it tiny and code-free. One command is the whole product; don't add
  dependencies, hooks, or scripts that execute on the user's machine.
- `bash scripts/validate-plugin.sh` must stay green (CI runs it).
- `assets/architecture.svg` is generated — never hand-edit it; rerun
  `python3 scripts/generate-architecture-svg.py`.
- Bump `version` in both `.claude-plugin/plugin.json` and `marketplace.json` together.
