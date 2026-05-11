# Anti-Contamination and Evidence

Read this before using subagents to validate a skill, especially when you already suspect the failure mode or desired fix.

## Validation integrity rule

A subagent test is only useful when the subagent succeeds from the skill and task-local artifacts, not from leaked conclusions.

Do not reveal:

- suspected bug,
- intended fix,
- expected answer,
- hidden rubric,
- your diagnosis,
- which output should win.

When the user has already stated a leaked answer, avoid repeating it verbatim in the response. Refer to it generically as "the suspected bug", "the intended fix", or "the expected answer" so the final response does not become a contaminated prompt someone might copy.

Pass instead:

- the skill path,
- the user-like task,
- raw input files or fixtures,
- output location,
- neutral success criteria if the user would naturally provide them.

## Prompt pattern

Always prefer a saved `skill_test_subagent` scenario when validating a skill. If required artifacts are missing, do not call the skill ready; report exact labels `Verdict: not ready`, `Evidence paths: none yet`, `Reviewer rationale: ...`, and `Next action: ...`. Include the phrases `raw task/artifact prompt` and `do not reveal` when explaining the uncontaminated scenario.

Good:

```text
Use the skill at /path/to/skill to validate ./sample.csv and write a validation report to ./outputs/report.md. Treat this as a user task. If data is invalid, identify invalid rows and explain why.
```

Bad:

```text
Use the skill at /path/to/skill. The bug is that missing emails should be rejected; check whether it rejects row 4.
```

## When expected behavior must be specified

Some tasks require explicit requirements. It is fine to state requirements that a real user would provide:

```text
The CSV schema requires id, email, and created_at. Validate ./sample.csv against that schema.
```

It is not fine to reveal your hidden evaluation target:

```text
The correct answer is that row 4 is invalid because email is missing.
```

## Evidence to preserve

Every readiness report should include:

- scenario file path,
- output directory,
- baseline verdict,
- skill-present verdict,
- reviewer rationale,
- important quotes or artifact paths,
- validator result,
- remaining risks,
- recommended next action.

## Readiness report template

```markdown
## Skill readiness evidence

Verdict: ready / not ready / needs another iteration

### Scenarios

| Scenario | Baseline | Skill-present | Evidence |
| --- | --- | --- | --- |
| `<path>` | failed-as-expected | passed | `<output-dir>` |

### Reviewer rationale

- Baseline failed because ...
- Skill-present passed because ...
- Remaining concern: ...

### Validator

- Command: `python .pi/skills/writing-skills/scripts/validate_skill.py <skill-path>`
- Result: pass/fail/warnings

### Next action

Recommended next action: ...
```

## Cleaning and isolation

Use `workingDirectory: "temp-git-worktree"` in scenarios that might write files. Keep test outputs outside the skill package, for example:

```text
skill-tests/my-skill/red-results/
skill-tests/my-skill/green-results/
```

Do not place eval outputs, transcripts, or workspaces inside `.pi/skills/<skill-name>/`; they can be accidentally loaded or packaged.

## Interpreting results

- Baseline fails + skill-present passes: useful GREEN evidence.
- Baseline passes: scenario does not prove the skill is needed; strengthen or replace it.
- Both fail: skill instructions or resources are insufficient, or scenario is unrealistic.
- Skill-present passes only with leaked hints: not a valid pass.
- Skill-present improves but remains incomplete: refactor and retest.

Treat every failure as one of:

1. instruction improvement,
2. scenario improvement,
3. validation rule,
4. bundled helper/script/reference.
