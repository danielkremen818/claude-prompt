# Summary

<!-- What does this change and why? Link any related issue. -->

## Checklist

- [ ] `bash scripts/validate-plugin.sh` passes (manifests valid, versions agree, no leaks)
- [ ] Bumped `version` in **both** `.claude-plugin/plugin.json` and `marketplace.json` (if user-facing)
- [ ] `CHANGELOG.md` updated under `## [Unreleased]` (if user-facing)
- [ ] Regenerated `assets/architecture.svg` + `assets/term-*.svg` if the command flow changed (`python3 scripts/generate-architecture-svg.py && python3 scripts/generate-terminals.py`)
- [ ] Stays in scope: a focused prompt-optimizer command, no scope creep

## Notes for the reviewer

<!-- Anything non-obvious: trade-offs, follow-ups, things you're unsure about. -->
