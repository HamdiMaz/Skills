# Skill Architecture and Descriptions

Read this when drafting or reviewing a skill's structure, frontmatter, and supporting resources.

## Pi skill requirements

A Pi skill is a directory containing `SKILL.md`.

Required frontmatter:

```yaml
---
name: my-skill
description: What the skill is for and when to use it.
---
```

Pi follows the Agent Skills standard leniently, but write strict skills:

- `name`: lowercase letters, numbers, hyphens; max 64 chars.
- `name` should match the parent directory.
- `description`: max 1024 chars; missing descriptions prevent loading.
- Use forward slashes in paths.
- Unknown fields may be ignored; do not rely on them for trigger behavior.

## Description pattern

Use this shape:

```yaml
description: <short capability>. Use when <trigger conditions, user intents, file types, symptoms, or contexts>.
```

Include:

- what the skill is for,
- when Pi should load it,
- specific trigger terms or situations,
- file types or tools if relevant.

Do not include:

- the internal workflow,
- step lists,
- implementation sequence,
- evaluation methodology,
- claims that cause Pi to follow the description instead of reading `SKILL.md`.

Good:

```yaml
description: Creates Kubernetes incident runbooks. Use when creating, reviewing, or updating Kubernetes runbook documentation, triage steps, rollback guidance, or kubectl-based operator procedures.
```

Bad:

```yaml
description: Creates runbooks by asking questions, writing RED tests, running subagents, drafting SKILL.md, validating, and refactoring.
```

## Progressive disclosure

Keep `SKILL.md` as the operating guide. Move detailed material out when it would bloat context or is only conditionally needed.

Use:

```text
my-skill/
  SKILL.md
  references/
    api-reference.md
    troubleshooting.md
  scripts/
    validate_plan.py
  assets/
    template.docx
```

Rules:

- Keep reference files one level from `SKILL.md`; avoid nested chains like `references/a.md` → `details/b.md`.
- In `SKILL.md`, explicitly say when to read each reference.
- For reference files over ~100 lines, include a short contents list.
- Use `scripts/` for deterministic, fragile, or frequently repeated operations.
- Use `assets/` only for files used in final outputs.
- Do not create README, changelog, installation guide, or process-summary files inside a skill package unless they are actual task assets.

## Choosing instruction strictness

Match specificity to fragility:

| Situation | Degree of freedom | Best form |
| --- | --- | --- |
| Many valid approaches | High | Heuristics and principles |
| Preferred pattern with variation | Medium | Checklist, template, pseudocode |
| Fragile, repeated, or security-sensitive operation | Low | Script or exact command |

If the agent repeatedly writes the same helper during tests, bundle that helper as a script.

## Script ergonomics

Scripts should be easy for Pi to execute and interpret:

- Print concise success/failure messages.
- Avoid long tracebacks when a friendly error is possible.
- Truncate or summarize large outputs.
- Use non-zero exit codes for real failures.
- Validate inputs and explain how to fix problems.
- Prefer no network dependency unless the skill explicitly requires it.

## Resource placement checklist

Put content in `SKILL.md` when:

- It is core to every invocation.
- It is a short workflow or decision rule.
- Missing it would cause frequent failure.

Put content in `references/` when:

- It is long, domain-specific, or only sometimes needed.
- It is an API, schema, policy, style guide, or advanced workflow.

Put content in `scripts/` when:

- It is deterministic validation or transformation.
- It is repeated across scenarios.
- It is hard for the model to reproduce reliably.

Put content in `assets/` when:

- It is copied, transformed, or included in final user output.

Remove generated placeholders before readiness.
