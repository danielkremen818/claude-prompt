<div align="center">

# prompt-optimizer

**A Claude Code slash command that rewrites your request into a better prompt — then runs it.**

[![CI](https://github.com/danielkremen818/prompt-optimizer/actions/workflows/ci.yml/badge.svg)](https://github.com/danielkremen818/prompt-optimizer/actions/workflows/ci.yml)
[![CodeQL](https://github.com/danielkremen818/prompt-optimizer/actions/workflows/codeql.yml/badge.svg)](https://github.com/danielkremen818/prompt-optimizer/actions/workflows/codeql.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/danielkremen818/prompt-optimizer/badge)](https://scorecard.dev/viewer/?uri=github.com/danielkremen818/prompt-optimizer)
[![dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](#whats-in-the-box)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-d97757.svg)](https://docs.claude.com/en/docs/claude-code/plugins)

<img src="https://raw.githubusercontent.com/danielkremen818/prompt-optimizer/main/assets/architecture.svg" alt="prompt-optimizer architecture — install surface, the /p run, the four optimize techniques, and the output" width="900">

</div>

---

Type `/p <your request>` and Claude first **rewrites it into an optimized prompt** —
adding structure, specificity, and meta-instructions that get more out of extended
thinking — then **immediately carries that optimized prompt out**. You see the rewrite,
then you get the work. No extra round-trip.

It applies four techniques:

1. **Structured context** — explicit reasoning frameworks and step-by-step structure.
2. **Specificity** — vague asks become detailed requirements with clear success criteria.
3. **Meta-instructions** — guidance that leverages extended thinking and planning.
4. **Skip-comments** — text inside double quotes (`"like this"`) is preserved verbatim, so
   exact strings, names, and copy survive the rewrite untouched.

No code. No dependencies. No network. No hooks. Just one auditable command. MIT.

## Install

In Claude Code:

```
/plugin marketplace add danielkremen818/prompt-optimizer
/plugin install prompt-optimizer@prompt-optimizer
```

That's it — the command is now available.

## Usage

```
/p add input validation to the signup form
```

Claude responds in two parts:

> **Optimized prompt:**
> *(the rewritten, structured version of your request)*
>
> *(then it executes that prompt in full)*

Skip-comments in action — anything you quote is left exactly as written:

```
/p rename the button label to "Get started — it's free" everywhere
```

The optimizer will restructure the task but never touch `"Get started — it's free"`.

### When to use it

- Vague or one-line asks you want Claude to scope properly before acting.
- Tasks where you want explicit success criteria and a plan, not a guess.
- Anything where a sharper prompt would mean a sharper result.

For trivial, well-specified requests, skip it — the rewrite step is overhead you don't need.

## What's in the box

| Path | Purpose |
| --- | --- |
| `commands/p.md` | The `/p` slash command definition — the whole product. |
| `.claude-plugin/plugin.json` | Plugin manifest. |
| `.claude-plugin/marketplace.json` | Marketplace metadata for one-line install. |
| `scripts/` | The CI validator and the SVG diagram generator (dev-only). |

The command is invoked as `/p` (or fully qualified, `/prompt-optimizer:p`). See
[`docs/architecture.md`](docs/architecture.md) for the full flow.

## Security

prompt-optimizer ships **no code, no dependencies, and no hooks** — it cannot run
anything on your machine, only add a `/p` command whose body is a prompt. CI pins every
GitHub Action to a commit SHA, runs CodeQL (actions) and OpenSSF Scorecard, and fails
the build if any tracked file leaks an email, token, or private path. See
[`SECURITY.md`](SECURITY.md).

## Contributing

Issues and PRs welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md). The whole plugin is
one markdown file; fork it, tweak the techniques, ship your own variant.

## License

[MIT](./LICENSE) © 2026 Daniel Kremen
