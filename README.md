<div align="center">

# prompt-optimizer

**A Claude Code slash command that rewrites your request into a better prompt — then runs it.**

[![CI](https://github.com/danielkremen818/prompt-optimizer/actions/workflows/ci.yml/badge.svg)](https://github.com/danielkremen818/prompt-optimizer/actions/workflows/ci.yml)
[![CodeQL](https://github.com/danielkremen818/prompt-optimizer/actions/workflows/codeql.yml/badge.svg)](https://github.com/danielkremen818/prompt-optimizer/actions/workflows/codeql.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/danielkremen818/prompt-optimizer/badge)](https://scorecard.dev/viewer/?uri=github.com/danielkremen818/prompt-optimizer)
[![dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](#whats-in-the-box)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-d97757.svg)](https://code.claude.com/docs/en/plugins)

<img src="https://raw.githubusercontent.com/danielkremen818/prompt-optimizer/main/assets/term-demo.svg" alt="A /p session: the typed request, the rewritten Optimized prompt, then Claude executing it" width="560">

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

In Claude Code, add the marketplace and install the plugin:

```
/plugin marketplace add danielkremen818/prompt-optimizer
/plugin install prompt-optimizer@prompt-optimizer
```

That's it — the `/p` command is now available in your session. To update later, bump
happens automatically on the next `/plugin` sync once a new version is published.

> Requires Claude Code with plugin support. See the
> [official plugin docs](https://code.claude.com/docs/en/plugins) if `/plugin` isn't
> recognized.

## Usage

Run `/p` followed by whatever you'd normally ask:

```
/p add input validation to the signup form
```

Claude responds in two parts — the rewritten prompt, then the work:

<div align="center">
<img src="https://raw.githubusercontent.com/danielkremen818/prompt-optimizer/main/assets/term-demo.svg" alt="prompt-optimizer rewriting a request into a structured prompt, then executing it" width="560">
</div>

### Example: quoted text is never touched

Anything inside double quotes is preserved exactly — labels, copy, identifiers,
error strings:

```
/p rename the CTA to "Get started — it's free" everywhere
```

The optimizer restructures the task but leaves `"Get started — it's free"` byte-for-byte:

<div align="center">
<img src="https://raw.githubusercontent.com/danielkremen818/prompt-optimizer/main/assets/term-skip-comments.svg" alt="The skip-comments technique preserving a quoted call-to-action string verbatim" width="520">
</div>

### When to use it

- Vague or one-line asks you want Claude to scope properly before acting.
- Tasks where you want explicit success criteria and a plan, not a guess.
- Anything where a sharper prompt would mean a sharper result.

For trivial, well-specified requests, skip it — the rewrite step is overhead you don't need.

## How it works

One command file, two manifests, no runtime code. Your request flows through three steps
— optimize, show, execute — with the four techniques applied during the optimize step:

<div align="center">
<img src="https://raw.githubusercontent.com/danielkremen818/prompt-optimizer/main/assets/architecture.svg" alt="prompt-optimizer architecture — install surface, the /p run, the four optimize techniques, and the output" width="900">
</div>

Full write-up in [`docs/architecture.md`](docs/architecture.md).

## What's in the box

| Path | Purpose |
| --- | --- |
| `commands/p.md` | The `/p` slash command definition — the whole product. |
| `.claude-plugin/plugin.json` | Plugin manifest. |
| `.claude-plugin/marketplace.json` | Marketplace metadata for one-line install. |
| `scripts/` | The CI validator and the SVG diagram/terminal generators (dev-only). |

The command is invoked as `/p` (or fully qualified, `/prompt-optimizer:p`).

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
