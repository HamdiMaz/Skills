# Skills

A catalog of reusable AI agent skills for use with the [`sv`](https://github.com/HamdiMaz/sv) CLI.

This repository is meant to be used as a Git-backed skill source. `sv` can list the skills here, copy selected skills into a project, and keep those project-local copies in sync.

## Available skills

| Skill | When to use |
| --- | --- |
| [`brainstorming`](skills/brainstorming/) | Exploring intent, requirements, approaches, and design before creative work or behavior changes. |
| [`find-docs`](skills/find-docs/) | Retrieving current documentation, API references, and examples for developer technologies. |
| [`github-release`](skills/github-release/) | Creating or publishing a GitHub release from repository version metadata, changelog entries, git tags, and the GitHub CLI. |
| [`guiding-product-specs`](skills/guiding-product-specs/) | Creating or refining product specs, MVP specs, PRDs, user flows, dashboard states, and scope boundaries. |
| [`systematic-debugging`](skills/systematic-debugging/) | Investigating bugs, test failures, or unexpected behavior before proposing fixes. |
| [`writing-skills`](skills/writing-skills/) | Creating new skills, editing existing skills, or verifying skills before deployment. |

## Use with sv

Configure this repository as the global skill source:

```bash
sv config repo HamdiMaz/Skills
```

List available skills:

```bash
sv list
```

Add a skill to the current project:

```bash
sv add github-release
```

Sync project-local skills with matching skills from this catalog:

```bash
sv sync
```

Run Pi with only the current project's local skills enabled:

```bash
sv run -- <pi args>
```

## Repository layout

`sv` expects skills to live as immediate folders under `skills/`:

```text
skills/
  skill-name/
    SKILL.md
    optional-supporting-file.md
```

Each skill folder should include a `SKILL.md` file with skill frontmatter:

```markdown
---
name: skill-name
description: Use when ...
---
```

Supporting files are copied with the skill folder, so templates, scripts, diagrams, and reference docs can live next to `SKILL.md` when needed.

## Maintaining the catalog

To add a skill:

1. Create `skills/<skill-name>/`.
2. Add `SKILL.md` with `name` and `description` frontmatter.
3. Keep the skill focused, reusable, and project-agnostic.
4. Add any supporting files inside the same skill folder.
5. Update the **Available skills** table in this README.

To update a skill, edit its folder in this repository. Users can pull the latest version into their projects with `sv sync`.

## License

MIT
