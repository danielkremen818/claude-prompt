# Maintaining claude-prompt

Maintainer-only runbook: how to cut a release and how to lock down the repository with
branch/tag rulesets and the security toggles.

> **Audience:** the maintainer (**@danielkremen818**). Contributors don't need any of
> this — see [CONTRIBUTING.md](CONTRIBUTING.md).

## 1. Release process

Releases are tag-driven. Pushing a `vX.Y.Z` tag triggers
[`.github/workflows/release.yml`](.github/workflows/release.yml), which validates the
plugin, checks the tag matches the manifest version, and creates a GitHub Release.
There is no npm publish — users get the new version on their next `/plugin` update.

1. Bump the version in **both** manifests (they must match — CI enforces it):
   - `.claude-plugin/plugin.json` → `"version"`
   - `.claude-plugin/marketplace.json` → `plugins[0].version`
2. Update `CHANGELOG.md`: move `## [Unreleased]` entries under a new
   `## [X.Y.Z] - YYYY-MM-DD` heading and refresh the compare links.
3. Verify locally:
   ```bash
   bash scripts/validate-plugin.sh
   ```
4. Commit, then tag and push:
   ```bash
   git commit -am "chore: release vX.Y.Z"
   git tag vX.Y.Z
   git push origin main
   git push origin vX.Y.Z   # this triggers release.yml
   ```
5. Watch the run: `gh run watch` (or the Actions tab).

> Bump `version` on **every** change to the plugin. Claude Code skips re-install when
> the resolved version is unchanged, so users won't get updates otherwise.

## 2. Branch & tag protection (GitHub Rulesets)

These use **repository Rulesets** (not the legacy "branch protection" UI) for layered,
named, auditable rules.

> **Prerequisite — the remote must exist first.** Every `gh` command below targets
> `danielkremen818/claude-prompt`, so create and push the repo before running any
> of them:
>
> ```bash
> gh repo create danielkremen818/claude-prompt --source=. --public --remote=origin --push
> ```

### 2a. `main` branch ruleset (strict solo)

Requires a PR (0 approvals — you're solo, but a PR gives you CI + a diff before merge),
the `validate` check must pass and be up to date, conversations resolved, and
force-push + deletion blocked. **No bypass actors** — applies to everyone, including
the owner.

```bash
gh api --method POST repos/danielkremen818/claude-prompt/rulesets --input - <<'JSON'
{
  "name": "main protection",
  "target": "branch",
  "enforcement": "active",
  "bypass_actors": [],
  "conditions": {
    "ref_name": { "include": ["refs/heads/main"], "exclude": [] }
  },
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": true,
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_review_thread_resolution": true
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": true,
        "required_status_checks": [
          { "context": "validate" }
        ]
      }
    }
  ]
}
JSON
```

> The status-check context `validate` is the job name from `ci.yml`. It only becomes
> selectable after CI has run at least once on the repo.

### 2b. `v*` tag ruleset (restrict release tags to the owner)

Releases are tag-driven, so tags are privileged. This restricts who can create or
delete `v*` tags to the **Admin** role (the owner).

```bash
gh api --method POST repos/danielkremen818/claude-prompt/rulesets --input - <<'JSON'
{
  "name": "version tags",
  "target": "tag",
  "enforcement": "active",
  "bypass_actors": [
    { "actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always" }
  ],
  "conditions": {
    "ref_name": { "include": ["refs/tags/v*"], "exclude": [] }
  },
  "rules": [
    { "type": "creation" },
    { "type": "deletion" },
    { "type": "non_fast_forward" }
  ]
}
JSON
```

> `actor_id: 5` + `actor_type: RepositoryRole` is the built-in **Admin** role. On a
> personal repo the owner always holds Admin, so this effectively means "only me."

## 3. Repository settings hardening

Run these once after the remote exists (each is idempotent):

```bash
# Dependabot alerts (prerequisite) + automated security updates
gh api --method PUT repos/danielkremen818/claude-prompt/vulnerability-alerts
gh api --method PUT repos/danielkremen818/claude-prompt/automated-security-fixes

# Secret scanning + push protection
gh api --method PATCH repos/danielkremen818/claude-prompt --input - <<'JSON'
{
  "security_and_analysis": {
    "secret_scanning": { "status": "enabled" },
    "secret_scanning_push_protection": { "status": "enabled" }
  }
}
JSON

# GitHub Actions: require approval to run workflows for ALL outside collaborators
gh api --method PUT repos/danielkremen818/claude-prompt/actions/permissions/fork-pr-contributor-approval --input - <<'JSON'
{ "approval_policy": "all_external_contributors" }
JSON
```

> If a `gh api` endpoint name has drifted, the equivalent toggles live under
> **Settings → Code security** (Dependabot, secret scanning, push protection) and
> **Settings → Actions → General → Fork pull request workflows** in the web UI.
> Verify against the current GitHub REST docs before relying on the exact path.
