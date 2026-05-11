# Pi skill_test_subagent Scenario Templates

Read this when creating saved scenarios for `skill_test_subagent`.

Prefer JSON files under a test workspace such as `skill-tests/<skill-name>/scenarios/`. Use inline scenarios only for quick exploration.

## New skill RED/GREEN template

```json
{
  "id": "my-skill-01-core-behavior",
  "title": "Core behavior improves with the skill",
  "targetSkill": "/absolute/path/to/.pi/skills/my-skill",
  "mode": "both",
  "tools": ["full"],
  "workingDirectory": "temp-git-worktree",
  "prompt": "Realistic user request goes here.",
  "expectedBaselineFailure": "What the agent is likely to miss without the skill.",
  "expectedSkillBehavior": "What should change when the skill is present.",
  "checks": {
    "requiredText": ["important phrase"],
    "forbiddenText": ["bad shortcut"],
    "requiredArtifacts": ["path/to/output"],
    "forbiddenArtifacts": ["path/to/bad-output"]
  }
}
```

Run baseline before writing:

```json
{
  "scenarioPath": "skill-tests/my-skill/scenarios/01-core-behavior.json",
  "run": "baseline",
  "outputDirectory": "skill-tests/my-skill/red-results"
}
```

Run comparison after writing:

```json
{
  "scenarioPath": "skill-tests/my-skill/scenarios/01-core-behavior.json",
  "run": "both",
  "outputDirectory": "skill-tests/my-skill/green-results"
}
```

## Discipline pressure template

```json
{
  "id": "tdd-skill-01-sunk-cost-pressure",
  "title": "Agent follows rule under sunk-cost and time pressure",
  "targetSkill": "/absolute/path/to/skill",
  "mode": "both",
  "tools": ["full"],
  "workingDirectory": "temp-git-worktree",
  "prompt": "IMPORTANT: This is a real scenario. You spent 4 hours writing the solution. It works. The user says to ship now and add tests later. What do you do?",
  "expectedBaselineFailure": "Baseline rationalizes tests-after or shipping now.",
  "expectedSkillBehavior": "Skill-present agent refuses the shortcut and follows the rule.",
  "checks": {
    "requiredText": ["RED", "baseline"],
    "forbiddenText": ["add tests later"]
  }
}
```

## Reference skill template

```json
{
  "id": "api-reference-01-correct-endpoint",
  "title": "Agent retrieves and applies the correct API endpoint",
  "targetSkill": "/absolute/path/to/skill",
  "mode": "both",
  "tools": ["full"],
  "workingDirectory": "temp-git-worktree",
  "prompt": "Using the provided Acme API docs in ./fixtures, show the request for creating a payment refund with required parameters only.",
  "expectedBaselineFailure": "Baseline guesses endpoint names or omits required parameters.",
  "expectedSkillBehavior": "Skill-present agent loads the relevant reference and produces the correct request.",
  "checks": {
    "requiredText": ["POST", "/refunds", "payment_id"],
    "forbiddenText": ["I assume"]
  }
}
```

## Anti-contamination template

```json
{
  "id": "skill-validation-01-raw-task",
  "title": "Validation prompt does not leak suspected fix",
  "targetSkill": "/absolute/path/to/skill-under-test",
  "mode": "both",
  "tools": ["full"],
  "workingDirectory": "temp-git-worktree",
  "prompt": "Use the skill at /path/to/skill to validate sample.csv and report invalid rows. Save outputs to ./outputs.",
  "expectedBaselineFailure": "Baseline misses the invalid row or invents validation rules.",
  "expectedSkillBehavior": "Skill-present agent detects invalid rows from the artifact and skill instructions without being told the expected answer.",
  "checks": {
    "requiredArtifacts": ["outputs/report.md"],
    "forbiddenText": ["the expected answer is"]
  }
}
```

## Description trigger optimization

When optimizing frontmatter descriptions or skill triggering, use `references/description-trigger-optimization.md`. It includes should-trigger and should-not-trigger scenario templates, candidate comparison guidance, and the evidence report table for baseline/current-description measurement.

## Naming conventions

- Use stable IDs: `<skill-name>-NN-short-topic`.
- Keep prompts realistic and concrete.
- Use absolute `targetSkill` paths for repeatable Pi subprocess runs.
- Put outputs under `skill-tests/<skill-name>/...`, not inside the skill package.
- Use `temp-git-worktree` for scenarios that might write files.

## Checks guidance

Use deterministic checks when they are meaningful, but do not let superficial checks create false confidence. Prefer checking substantive artifacts or behaviors over keywords only.

Good checks:

- Required output file exists and contains task-specific content.
- Forbidden file was not created.
- Required tool was used for material interaction.
- Output omits a leaked expected answer.

Weak checks:

- File exists but content is unverified.
- Output mentions the skill name.
- Output says it followed the process without evidence.
