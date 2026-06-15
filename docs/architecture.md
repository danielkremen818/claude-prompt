# Architecture

prompt-optimizer is about as simple as a Claude Code plugin gets: one slash command,
two manifests, and the packaging/CI around them. There is no runtime code.

<div align="center">

<img src="../assets/architecture.svg" alt="prompt-optimizer architecture — install surface, the /p run, the four optimize techniques, and the output" width="960">

</div>

## The two surfaces

**Install surface.** The marketplace reads `.claude-plugin/marketplace.json`, which
points at this repo as a plugin. `.claude-plugin/plugin.json` is the manifest, and
`commands/p.md` is the command body. Installing the plugin makes `/p` (fully qualified
`/prompt-optimizer:p`) available in the session.

**The `/p` run.** When you type `/p <request>`, Claude Code substitutes your text for
`$ARGUMENTS` in `commands/p.md` and runs the resulting prompt. That prompt puts Claude
into "PROMPT OPTIMIZER" mode with three steps:

1. **Optimize** — rewrite the request into a sharper prompt using four techniques:
   - **Structured context** — explicit reasoning frameworks and step-by-step structure.
   - **Specificity** — vague asks become detailed requirements with success criteria.
   - **Meta-instructions** — guidance that leverages extended thinking and planning.
   - **Skip-comments** — text inside double quotes (`"like this"`) is preserved verbatim.
2. **Show** — print the rewrite under an `**Optimized prompt:**` heading so you see it.
3. **Execute** — immediately carry out the optimized prompt in full.

That's the entire system. The diagram above is the live version (animated in the SVG).

## Why no code?

Keeping the plugin to a single command file means there is nothing to audit beyond the
prompt itself, nothing to run on your machine, and no dependency surface. The
[security model](../SECURITY.md) leans entirely on that simplicity.

## Regenerating the diagram

`assets/architecture.svg` is generated, not hand-written:

```bash
python3 scripts/generate-architecture-svg.py
```

The brand primitives (palette, node cards, animated flows, the dark/light CSS) live in
`scripts/svgkit.py`. If you change the command flow, edit the generator and rerun it,
then commit the regenerated SVG.
