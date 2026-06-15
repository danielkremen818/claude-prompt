# Security Policy

## Supported versions

claude-prompt follows [Semantic Versioning](https://semver.org/). Fixes land on
the latest minor release line.

| Version | Supported |
| ------- | --------- |
| 0.1.x   | ✅        |

## Reporting a vulnerability

Please report security issues **privately** via this repository's
**GitHub Security Advisories** → **"Report a vulnerability"**
(the *Security* tab → *Advisories* → *Report a vulnerability*). This opens a private
channel with the maintainer; do **not** open a public issue for a suspected
vulnerability.

You should expect an initial acknowledgement within a few days. Once a fix is
prepared, the advisory is published alongside the patched release.

## Trust model

claude-prompt is one of the smallest things you can install in Claude Code: a
**single slash-command definition** (`commands/p.md`) plus two JSON manifests. There
is intentionally very little to vet.

- **No code.** The plugin ships no JavaScript, no binary, no install script, and no
  hooks. It cannot execute anything on your machine on its own — it only adds a
  `/p` command whose body is a prompt sent to Claude.
- **No telemetry, no network.** Nothing is collected, logged off-machine, or phoned
  home. The plugin makes no network requests of its own.
- **No dependencies.** There is no package manifest and no dependency tree, so there
  is no supply chain to compromise.
- **Reads only what you pass it.** The command operates solely on the request text you
  type after `/p`. It does not read your filesystem or environment.

The only executable surface in this repository is its **GitHub Actions workflows**,
which is why CodeQL (the `actions` pack) and OpenSSF Scorecard run in CI.

## Supply-chain posture

- **Pinned CI.** Every GitHub Action is pinned to a full commit SHA. CodeQL and
  OpenSSF Scorecard run on a schedule and on every push to `main`.
- **No release artifact to tamper with.** Releases are validated, tagged GitHub
  Releases (`release.yml`) — there is no published binary or npm tarball.
- **Leak scan in CI.** `scripts/validate-plugin.sh` (run by CI) fails the build if any
  tracked file contains an email, token, private path, or key-shaped string.
- **Branch & tag protection.** `main` and `v*` tags are protected via GitHub Rulesets
  (see [MAINTAINING.md](MAINTAINING.md)).
