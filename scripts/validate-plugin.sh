#!/usr/bin/env bash
#
# validate-plugin.sh — the green-bar invariant for claude-prompt.
#
# This is a command-only Claude Code plugin, so there is no compiled code to test.
# "Valid" instead means: the manifests parse, their versions agree, the command file
# is well-formed, and no private data has leaked into a tracked file. CI runs exactly
# this script, so a green local run means a green CI run.
#
# Usage:  scripts/validate-plugin.sh        (run from the repo root)
set -euo pipefail

cd "$(dirname "$0")/.."

fail() { echo "FAIL: $*" >&2; exit 1; }
ok()   { echo "ok: $*"; }

command -v jq >/dev/null || fail "jq is required"

PLUGIN=.claude-plugin/plugin.json
MARKET=.claude-plugin/marketplace.json
CMD=commands/p.md

# 1) Manifests are valid JSON.
jq -e . "$PLUGIN" >/dev/null  || fail "$PLUGIN is not valid JSON"
jq -e . "$MARKET" >/dev/null  || fail "$MARKET is not valid JSON"
ok "manifests are valid JSON"

# 2) Required fields exist and the two version strings agree (Claude Code skips
#    re-install when the version is unchanged, so a mismatch ships stale installs).
pv=$(jq -r '.version // empty' "$PLUGIN")
pn=$(jq -r '.name // empty'    "$PLUGIN")
mv=$(jq -r '.plugins[0].version // empty' "$MARKET")
[ -n "$pn" ] || fail "plugin.json is missing .name"
[ -n "$pv" ] || fail "plugin.json is missing .version"
[ "$pv" = "$mv" ] || fail "version mismatch: plugin.json=$pv marketplace.json=$mv"
ok "plugin '$pn' version $pv (manifests agree)"

# 3) The command file exists and carries YAML frontmatter with a description.
[ -f "$CMD" ] || fail "$CMD is missing"
head -1 "$CMD" | grep -qx -- '---' || fail "$CMD is missing the opening '---' frontmatter fence"
grep -q '^description:' "$CMD"     || fail "$CMD frontmatter has no 'description:'"
grep -q '\$ARGUMENTS' "$CMD"       || fail "$CMD does not reference \$ARGUMENTS"
ok "command file $CMD is well-formed"

# 4) Private-data leak scan over tracked files (this script excludes itself so its
#    own pattern strings don't trigger a false positive).
LEAK='jeen\.ai|/Users/[a-z]|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-ant-[A-Za-z0-9-]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----'
if git grep -nIE "$LEAK" -- . ':!scripts/validate-plugin.sh' ':!*.svg' >/tmp/leak.$$ 2>/dev/null; then
  echo "FAIL: possible private data in tracked files:" >&2
  cat /tmp/leak.$$ >&2
  rm -f /tmp/leak.$$
  exit 1
fi
rm -f /tmp/leak.$$
ok "no private data found in tracked files"

echo "PASS: claude-prompt plugin is valid."
