# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Documentation
- Clarified that the installed command is invoked as `/claude-prompt:p` — Claude Code
  namespaces every plugin command, so the bare `/p` isn't recognized after a plain
  install. README and architecture examples now use `/claude-prompt:p`, and a new
  **Shorten to `/p`** section explains how to alias it to a bare `/p` via a personal
  command (a copy, refreshed after each plugin update).

## [0.2.0] - 2026-06-16

### Added
- **Clarify/confirm gate** — `/p` now reads the request first and, only when warranted,
  asks 1–3 targeted questions (ambiguous) or confirms the blast radius (high-stakes,
  mutating) before executing. Clear, low-stakes asks still run one-shot.
- **Intent typing** — TASK (do it), QUESTION (answer it), and IMPROVE-THIS (the rewrite is
  the deliverable) are handled distinctly.
- **`--dry` optimize-only mode** — prefix `--dry` to get just the optimized prompt without
  executing.
- **Injection boundary** — a data/instruction fence before the request so its text can't
  override the command's own steps.
- Empty/flag-only and compound requests, and context references, are handled explicitly.

### Changed
- **Robust skip-comments** — preserve verbatim not just `"double quotes"` but also
  `` `inline code` ``, fenced code blocks, file paths, URLs, regexes/globs, and error
  strings (bare `'single quotes'` dropped — they collide with apostrophes).
- **Right-sizing** — trivial/already-strong asks get a light touch instead of an inflated
  prompt or a near-duplicate echo.

## [0.1.0] - 2026-06-15

### Added
- Initial release.
- `/p` (`/claude-prompt:p`) slash command: rewrite a request into an optimized,
  reasoning-maximizing prompt, then immediately carry it out.
- Marketplace metadata for one-line install.

[Unreleased]: https://github.com/danielkremen818/claude-prompt/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/danielkremen818/claude-prompt/releases/tag/v0.2.0
[0.1.0]: https://github.com/danielkremen818/claude-prompt/releases/tag/v0.1.0
