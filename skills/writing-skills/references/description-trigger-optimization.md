# Description Trigger Optimization

Read this when a user asks to optimize, improve, tune, repair, or benchmark a skill's frontmatter `description`, skill triggering, under-triggering, or over-triggering.

## Core rule

Description optimization is a skill edit. Do not replace the live frontmatter from intuition alone.

Before editing the live skill, create evidence that the current description misses real trigger cases or over-triggers on near misses, then test candidate descriptions against the same suite.

## Trigger suite requirements

Use a saved suite under `skill-tests/<skill-name>/trigger-evals/` or `skill-tests/<skill-name>/scenarios/`. Keep outputs outside the skill package.

A useful trigger suite includes:

- **should-trigger prompts**: realistic user requests where Pi should load and apply the skill.
- **should-not-trigger prompts**: realistic near misses that share words with the skill but should be handled without that skill.
- **Concrete context**: file names, symptoms, tools, user phrasing, typos, urgency, or partial information.
- **No leaked conclusion**: do not tell the subagent which phrase should make the skill trigger.
- **Observable checks**: require behavior or artifacts that are hard to produce without the skill; forbid skill-specific behavior in near misses.

Start with 8-12 prompts unless the skill is tiny:

| Prompt type | Count | Purpose |
| --- | ---: | --- |
| Clear should-trigger | 3-4 | Common intended use |
| Edge should-trigger | 2-3 | Casual, indirect, abbreviated, or file/symptom-driven requests |
| Near-miss should-not-trigger | 3-4 | Shared vocabulary but wrong capability |
| Competing-skill case | 1-2 | Another skill or generic tools should win |

## Workflow

1. **Extract trigger intent**
   - Identify what the skill does, who uses it, file types, tools, symptoms, and non-goals.
   - Ask `AskUserQuestion` only when missing choices materially change the suite.

2. **Snapshot the current description**
   - For an existing skill, copy it outside the live package, for example `skill-tests/<skill-name>/snapshots/current-description/`.
   - The snapshot is the current-description baseline.

3. **Create saved trigger scenarios**
   - Write one scenario per prompt or a suite file pointing to scenario files when tools are available.
   - If tools are not available, provide a concrete proposed path such as `skill-tests/<skill-name>/trigger-evals/description-trigger-suite.json` and include representative prompt text in the response.
   - Do not defer suite design by saying no scenario exists yet.
   - Use raw user-like prompts. Do not say "this should trigger" inside the prompt.
   - Mark each case in scenario metadata or title as `should-trigger` or `should-not-trigger` for the reviewer.

4. **Run the baseline/current-description measurement**
   - Run `skill_test_subagent` against the snapshot or current skill before editing the live skill.
   - Record false negatives, false positives, reviewer rationale, and evidence paths.
   - If `skill_test_subagent` is unavailable, stop before changing frontmatter and report the missing baseline evidence.

5. **Draft candidate descriptions**
   - Keep candidates as concise what+when trigger descriptions.
   - Include capability, trigger conditions, file types/symptoms, and important near-miss boundaries.
   - Do not summarize the internal workflow.
   - Keep within Pi's 1024-character limit.

6. **Forward-test candidates in temp copies**
   - Create one temp copy per candidate outside the skill package.
   - Edit only that copy's description.
   - Run the same trigger suite for each candidate.
   - Prefer the candidate with better should-trigger coverage and fewer should-not-trigger false positives. Do not choose a candidate based only on sounding good.

7. **Apply and report**
   - Apply the winning description to the live skill only after evidence.
   - Run this skill's validator.
   - Report scenario paths, baseline/current-description verdicts, candidate verdicts, evidence paths, reviewer rationale, remaining risks, and next action.

## Scenario template: should-trigger

```json
{
  "id": "log-triage-desc-01-should-trigger-nginx-500s",
  "title": "Description trigger: should-trigger for nginx 500 spike",
  "targetSkill": "/absolute/path/to/skill-copy-under-test",
  "mode": "skill-present",
  "tools": ["full"],
  "workingDirectory": "temp-git-worktree",
  "prompt": "Production nginx access logs in ./logs/access.log show a sudden burst of 500s after the 14:05 deploy. Find the likely pattern and write a short triage note to ./outputs/triage.md.",
  "expectedSkillBehavior": "The agent loads and applies the log-triage skill's method to inspect logs and produce a triage note.",
  "checks": {
    "requiredArtifacts": ["outputs/triage.md"],
    "requiredText": ["500", "triage"]
  }
}
```

## Scenario template: should-not-trigger

```json
{
  "id": "log-triage-desc-09-should-not-trigger-login-copy",
  "title": "Description trigger: should-not-trigger for login button copy",
  "targetSkill": "/absolute/path/to/skill-copy-under-test",
  "mode": "skill-present",
  "tools": ["full"],
  "workingDirectory": "temp-git-worktree",
  "prompt": "The login page copy says 'Log in' in three places. Update the button text to 'Sign in' and summarize the code change.",
  "expectedSkillBehavior": "The agent should handle this as a UI text edit, not as log triage.",
  "checks": {
    "forbiddenText": ["log triage", "triage logs", "access.log"]
  }
}
```

## Candidate comparison table

Use this table in the readiness report:

| Candidate | Should-trigger pass | Should-not-trigger pass | False negatives | False positives | Evidence |
| --- | ---: | ---: | --- | --- | --- |
| current | 0/0 | 0/0 | none measured | none measured | `<path>` |
| candidate-a | 0/0 | 0/0 | none measured | none measured | `<path>` |

## Red flags

- The agent says a description is "ready to paste" without a trigger suite.
- The suite has only obvious positives and no near-miss negatives.
- Prompts explicitly name the skill instead of using natural user phrasing.
- The candidate wins by including workflow steps in the description.
- The live skill is edited before baseline/current-description evidence exists.
