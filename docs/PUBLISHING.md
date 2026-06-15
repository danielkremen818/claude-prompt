# Publishing

claude-prompt is distributed as a Claude Code plugin straight from this GitHub repo
— there is no npm package and no registry to push to. "Publishing" means the repo is
public and the marketplace manifest resolves.

## How users install

```text
/plugin marketplace add danielkremen818/claude-prompt
/plugin install claude-prompt@claude-prompt
```

Claude Code reads `.claude-plugin/marketplace.json` from the default branch, finds the
`claude-prompt` plugin (`"source": "./"`), and installs the command from
`commands/p.md`.

## Cutting a new version

See [MAINTAINING.md](../MAINTAINING.md) for the full runbook. In short:

1. Bump `"version"` in **both** `.claude-plugin/plugin.json` and
   `.claude-plugin/marketplace.json` (they must match — `scripts/validate-plugin.sh`
   enforces it).
2. Update `CHANGELOG.md`.
3. `bash scripts/validate-plugin.sh` (must pass).
4. Commit, tag `vX.Y.Z`, and push the tag — `release.yml` validates and creates the
   GitHub Release.

> Always bump the version. Claude Code skips re-install when the resolved version is
> unchanged, so without a bump, existing users won't pick up your changes.

## Pre-publish checklist

- [ ] `bash scripts/validate-plugin.sh` passes (includes the private-data leak scan).
- [ ] `git log --format='%ae'` shows only the public maintainer email (no work address).
- [ ] Versions in both manifests match and `CHANGELOG.md` has an entry.
- [ ] `assets/architecture.svg` is up to date if the command flow changed.
