---
name: github-release
description: Use when creating or publishing a GitHub release from repository version metadata, changelog entries, git tags, and the GitHub CLI.
---

# GitHub Release

## Overview

Create releases from explicit user intent only. Core rule: if the user did not provide an exact version number or tag, ask for it and stop; never infer `next patch`, `latest + 1`, or a SemVer bump.

**REQUIRED SUB-SKILL:** Use superpowers:verification-before-completion before reporting that a release is published.

## Version Gate

Before touching files, extract an exact version:

| User input | Action |
|---|---|
| `v1.2.3` or `1.2.3` | Continue with tag `v1.2.3` and package version `1.2.3` |
| `next patch`, `new release`, `bump version`, no number | Ask: `What version should I release?` and stop |
| Existing remote tag | Stop and ask how to proceed |

## Workflow

1. Preflight:
   ```bash
   git fetch --tags origin
   git status --short --branch
   git tag --list 'v[0-9]*.[0-9]*.[0-9]*' --sort=v:refname
   git ls-remote --tags origin refs/tags/vX.Y.Z
   gh auth status
   ```
   If unrelated uncommitted files exist, ask before staging anything.

2. Update release metadata:
   - Move all `## Unreleased` changelog bullets under `## vX.Y.Z`; leave `## Unreleased` empty.
   - Update package metadata such as `pyproject.toml` from the current version to `X.Y.Z`.
   - Update lockfile project-version mirrors such as the root package entry in `uv.lock`; do not change dependencies.

3. Verify local diff:
   ```bash
   git diff --check
   git diff -- CHANGELOG.md pyproject.toml uv.lock
   ```
   Run project-required tests only if code changed; release metadata only usually needs diff verification.

4. Commit, tag, and push:
   ```bash
   git add CHANGELOG.md pyproject.toml uv.lock
   git commit -m "chore: release vX.Y.Z" -m "Move unreleased changelog entries under vX.Y.Z and synchronize project version metadata."
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   git push origin HEAD
   git push origin vX.Y.Z
   ```

5. Create release notes from the exact changelog section:
   ```bash
   notes_file=$(mktemp)
   python - "vX.Y.Z" "$notes_file" <<'PY'
   import sys
   from pathlib import Path

   tag = sys.argv[1]
   output = Path(sys.argv[2])
   text = Path("CHANGELOG.md").read_text(encoding="utf-8")
   section = text.split(f"## {tag}", 1)[1].split("\n## ", 1)[0].strip()
   output.write_text(section + "\n", encoding="utf-8")
   PY
   gh release create vX.Y.Z --title "vX.Y.Z" --notes-file "$notes_file" --verify-tag
   rm -f "$notes_file"
   ```

6. Verify publication:
   ```bash
   git status --short --branch
   git ls-remote origin refs/heads/$(git branch --show-current) refs/tags/vX.Y.Z 'refs/tags/vX.Y.Z^{}'
   gh release view vX.Y.Z --json tagName,name,url,body
   ```

## Red Flags

- Inferring a version because the next SemVer bump is obvious.
- Running `gh release create` before pushing the git tag.
- Omitting `--verify-tag`, which can let GitHub CLI auto-create a tag.
- Using the whole changelog or generated notes instead of the `vX.Y.Z` section.
- Staging unrelated user changes with the release commit.
- Claiming publication before checking remote branch, tag, and `gh release view` output.
