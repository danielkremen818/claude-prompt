<div align="center">

# claude-prompt

**A Claude Code slash command that rewrites your request into a better prompt — then runs it.**

[![CI](https://github.com/danielkremen818/claude-prompt/actions/workflows/ci.yml/badge.svg)](https://github.com/danielkremen818/claude-prompt/actions/workflows/ci.yml)
[![CodeQL](https://github.com/danielkremen818/claude-prompt/actions/workflows/codeql.yml/badge.svg)](https://github.com/danielkremen818/claude-prompt/actions/workflows/codeql.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/danielkremen818/claude-prompt/badge)](https://scorecard.dev/viewer/?uri=github.com/danielkremen818/claude-prompt)
[![dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](#whats-in-the-box)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-d97757.svg)](https://code.claude.com/docs/en/plugins)

<img src="https://raw.githubusercontent.com/danielkremen818/claude-prompt/main/assets/term-demo.svg" alt="A /p session: the typed request, the rewritten Optimized prompt, then Claude executing it" width="560">

</div>

---

Type `/p <your request>` and Claude **reads it, rewrites it into an optimized prompt** —
adding structure, specificity, and meta-instructions that get more out of extended
thinking — then **carries it out**. You see the rewrite, then you get the work. Clear asks
run in one shot; only genuinely **ambiguous** asks get a quick clarifying question first,
and **high-stakes** (destructive/irreversible) asks get a one-line confirm before anything runs.

It applies four techniques:

1. **Structured context** — explicit reasoning frameworks and step-by-step structure.
2. **Specificity** — vague asks become detailed requirements with clear success criteria.
3. **Meta-instructions** — guidance that leverages extended thinking and planning.
4. **Skip-comments** — literals are reproduced verbatim: `"double quotes"`, `` `inline code` ``,
   fenced code blocks, file paths, URLs, regexes, and error strings survive the rewrite untouched.

It also **types intent** (do a task · answer a question · improve a piece of text) and supports a
**`--dry`** optimize-only mode. No code. No dependencies. No network. No hooks. Just one
auditable command. MIT.

## Install

In Claude Code, add the marketplace and install the plugin:

```
/plugin marketplace add danielkremen818/claude-prompt
/plugin install claude-prompt@claude-prompt
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
<img src="https://raw.githubusercontent.com/danielkremen818/claude-prompt/main/assets/term-demo.svg" alt="claude-prompt rewriting a request into a structured prompt, then executing it" width="560">
</div>

### Example: quoted text is never touched

Anything inside double quotes is preserved exactly — labels, copy, identifiers,
error strings:

```
/p rename the CTA to "Get started — it's free" everywhere
```

The optimizer restructures the task but leaves `"Get started — it's free"` byte-for-byte:

<div align="center">
<img src="https://raw.githubusercontent.com/danielkremen818/claude-prompt/main/assets/term-skip-comments.svg" alt="The skip-comments technique preserving a quoted call-to-action string verbatim" width="520">
</div>

### Just the prompt — `--dry`

Prefix `--dry` to get only the optimized prompt, without executing it — handy when you want to
copy the rewrite somewhere else or review it first:

```
/p --dry migrate the test suite from mocha to vitest
```

### When to use it

- Vague or one-line asks you want Claude to scope properly before acting.
- Tasks where you want explicit success criteria and a plan, not a guess.
- Anything where a sharper prompt would mean a sharper result.

For trivial, well-specified requests, skip it — the rewrite step is overhead you don't need.

## How it works

One command file, two manifests, no runtime code. Your request flows through **read →
optimize → show → execute** — a quick Step 0 classifies it (and clarifies/confirms only when
needed), then the four techniques are applied during the optimize step:

<div align="center">
<img src="https://raw.githubusercontent.com/danielkremen818/claude-prompt/main/assets/architecture.svg" alt="claude-prompt architecture — install surface, the /p run, the four optimize techniques, and the output" width="900">
</div>

Full write-up in [`docs/architecture.md`](docs/architecture.md).

## What's in the box

| Path | Purpose |
| --- | --- |
| `commands/p.md` | The `/p` slash command definition — the whole product. |
| `.claude-plugin/plugin.json` | Plugin manifest. |
| `.claude-plugin/marketplace.json` | Marketplace metadata for one-line install. |
| `scripts/` | The CI validator and the SVG diagram/terminal generators (dev-only). |

The command is invoked as `/p` (or fully qualified, `/claude-prompt:p`).

## Security

claude-prompt ships **no code, no dependencies, and no hooks** — it cannot run
anything on your machine, only add a `/p` command whose body is a prompt. CI pins every
GitHub Action to a commit SHA, runs CodeQL (actions) and OpenSSF Scorecard, and fails
the build if any tracked file leaks an email, token, or private path. See
[`SECURITY.md`](SECURITY.md).

## Contributing

Issues and PRs welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md). The whole plugin is
one markdown file; fork it, tweak the techniques, ship your own variant.

## License

[MIT](./LICENSE) © 2026 Daniel Kremen
