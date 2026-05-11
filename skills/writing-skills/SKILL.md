---
name: writing-skills
description: Creates and improves Pi agent skills using test-driven skill development. Use when creating, editing, validating, or pressure-testing SKILL.md files, especially before deploying skills.
---

# Writing Skills

## Pi-native contract

Use this skill to create or improve Pi agent skills under `.pi/skills/`, `~/.pi/agent/skills/`, `.agents/skills/`, or another user-approved skill directory.

Collaborate with the user to understand the desired capability. Once authoring begins, do not let user pressure bypass the methodology: skill creation follows RED-first testing, progressive disclosure, validation, and evidence reporting.

## Operating stance

- The user controls the goal, scope, domain facts, and preferences.
- The protocol controls the method: no new or edited skill is ready without RED evidence first.
- Use `AskUserQuestion` when choices materially affect the skill: scope, skill type, trigger conditions, output format, resource needs, risk tolerance, or install location.
- If `AskUserQuestion` is unavailable in an isolated test harness, ask plain-text questions but keep the same labeled intake fields: Skill type, Trigger conditions, Expected outputs, Success criteria, Edge cases, Resources.
- Do not use `AskUserQuestion` for plan approval or for decisions already clear from context.

## RED-first iron law

No final skill draft or skill edit without a failing baseline scenario first.

For a new skill, baseline means running the task without the proposed skill. For improving an existing skill, baseline means running the task against the old skill or current draft. For a pure reference skill, failure can be retrieval failure, incorrect application, missing context, or hallucinated use of the reference.

If a user asks to skip tests because the skill is simple, quick, obvious, or only documentation, stop and create the RED scenario first. Creating scenario files is not enough: do not create the final skill artifact until a baseline run has failed for the right reason. If `skill_test_subagent` is unavailable, report the blocker and stop before writing the final skill.

## Workflow

1. **Intake before authoring**
   - Extract any requirements already present in the conversation.
   - Ask only material unresolved questions with `AskUserQuestion`; if the tool is unavailable, ask plain-text questions with explicit labels.
   - Cover these fields before drafting: Skill type, Trigger conditions, Expected outputs, Success criteria, Edge cases, Resources, and install location when relevant.
   - Identify the skill type: discipline, technique, pattern, reference, or hybrid.
   - Define triggering conditions, expected behavior, outputs, non-goals, edge cases, and success criteria.
   - Do not proceed to final `SKILL.md` authoring until the intake is resolved.

2. **Design RED scenarios**
   - Prefer saved JSON scenario files for `skill_test_subagent` over ad-hoc inline scenarios.
   - Choose scenario shape by skill type:
     - Discipline: pressure/rationalization tests.
     - Technique: application and edge-case tests.
     - Pattern: recognition plus application tests.
     - Reference: retrieval plus application/correct-use tests.
   - For reference-skill requests, explicitly state: "This is a reference skill; RED must test retrieval and application before authoring."
   - See `references/intake-and-test-design.md` for the full matrix.
   - See `references/scenario-templates.md` for Pi scenario templates.

3. **Run baseline**
   - Use `skill_test_subagent` with `run="baseline"` before writing or editing the skill.
   - Preserve the output directory and evidence paths.
   - If `skill_test_subagent` is unavailable, do not draft the final skill; report `Verdict: blocked before authoring` and the missing baseline evidence.
   - If baseline unexpectedly succeeds, strengthen the scenario or choose a more meaningful gap before authoring.

4. **Write the minimal skill**
   - Create only enough instruction and supporting resources to address observed RED failures.
   - Keep `SKILL.md` lean. Move details to one-level `references/`; put deterministic or repeated logic in `scripts/`; use `assets/` only for files used in outputs.
   - Do not add README, changelog, installation guides, or process notes inside the skill package unless the user explicitly needs them as task assets.

5. **Validate**
   - Run `python scripts/validate_skill.py <skill-path>` from this skill when available.
   - Fix errors before testing skill-present behavior.
   - For scripts in the authored skill, run or syntax-check representative scripts.

6. **Verify GREEN**
   - Use `skill_test_subagent` with `run="both"` or `run="skill-present"` after the skill exists.
   - Prefer `run="both"` for final evidence so baseline and skill-present results are comparable.
   - Require reviewer verdicts, rationale, and durable evidence paths.

7. **Refactor from evidence**
   - If a valid test cannot run because the user has not provided the draft skill path or artifacts, return a mini evidence report anyway: `Verdict: not ready`, `Evidence paths: none yet`, `Reviewer rationale: proposed test is contaminated or underspecified`, `Next action: provide artifacts or approve a saved skill_test_subagent scenario`.
   - If skill-present fails, classify the failure as one of:
     - instruction improvement,
     - scenario improvement,
     - validation rule,
     - bundled helper/script/reference.
   - Change only what the evidence justifies, then re-run the affected scenarios.

8. **Report readiness**
   - Do not call the skill ready without evidence.
   - Report scenario paths, baseline verdicts, skill-present verdicts, reviewer rationale, evidence paths, validator results, remaining risks, and recommended next action.

## Description rule for Pi skills

Write frontmatter descriptions as a concise capability plus trigger conditions. Include what the skill is for and when to use it, but never summarize the internal workflow.

Description optimization is a skill edit, not a copywriting shortcut. When a user asks to optimize, improve, tune, repair, or benchmark triggering, do not produce a final replacement description from judgment alone. Create saved Pi `skill_test_subagent` **scenario** files or a suite with realistic **should-trigger** and **should-not-trigger** prompts, run a baseline/current-description measurement, test candidate descriptions in temporary copies, and report evidence before editing the live frontmatter or saying the description is ready. If the user asks for a paste-ready answer before evidence exists, do not repeat that phrase; report `Verdict: not ready` and the concrete scenario/evidence next action instead.

Do not defer trigger-suite design. In the same response or tool turn, either write the scenario/suite file or provide a concrete proposed path plus sample prompts. Do not say the scenario path is absent.

Minimum response before changing a description:

```markdown
Verdict: not ready
Scenario path: `skill-tests/<skill-name>/trigger-evals/description-trigger-suite.json` saved/proposed
Trigger suite: includes should-trigger prompts and should-not-trigger near misses.
Trigger prompts:
- should-trigger: `<realistic prompt 1>`
- should-trigger: `<realistic prompt 2>`
- should-not-trigger: `<near-miss prompt 1>`
- should-not-trigger: `<near-miss prompt 2>`
Baseline/current-description: not run yet / failed-as-expected / measured at `<evidence-path>`.
Evidence paths: none yet / `<output-directory>`
Next action: run the saved scenario or suite, compare candidate descriptions, then edit the live frontmatter only if evidence improves.
```

See `references/description-trigger-optimization.md` for the full Pi workflow and templates.

Good:

```yaml
description: Creates and improves Pi agent skills using test-driven skill development. Use when creating, editing, validating, or pressure-testing SKILL.md files, especially before deploying skills.
```

Bad:

```yaml
description: Creates skills by asking questions, writing failing tests, running baselines, drafting SKILL.md, validating with subagents, and refactoring until green.
```

See `references/architecture-and-descriptions.md` for naming, descriptions, progressive disclosure, and file organization.

## Anti-contamination rules

Validation subagents must test transferable behavior, not leaked conclusions.

- Use a **raw task/artifact prompt**: pass the raw task, raw artifacts, and relevant skill path.
- State the guardrail explicitly: **do not reveal** the suspected bug, intended fix, desired answer, prior diagnosis, or hidden rubric.
- When refusing a contaminated test, avoid repeating the user's leaked answer verbatim; refer to it generically as "the suspected bug", "the intended fix", or "the expected answer".
- Prefer a saved `skill_test_subagent` scenario for validation, then run it when enough artifacts are available.
- Use isolated workspaces or clean temp worktrees.
- Avoid leaving artifacts from previous iterations where a later subagent can discover them.
- Treat a pass as trustworthy only when the task-local prompt would also be fair for a real user request.

When refusing a contaminated validation request, use this exact mini-report shape so the user gets durable next steps:

```markdown
Verdict: not ready
Evidence paths: none yet
Reviewer rationale: proposed test is contaminated; do not reveal the suspected bug, intended fix, or expected answer.
Next action: create a saved skill_test_subagent scenario using a raw task/artifact prompt, then run baseline vs skill-present when the draft skill path and artifacts are available.
```

See `references/anti-contamination-and-evidence.md` for prompt patterns and the readiness report template.

## Validator

Use the bundled validator for Pi-compatible skill checks:

```bash
python .pi/skills/writing-skills/scripts/validate_skill.py .pi/skills/example-skill
```

The validator checks frontmatter, name/directory consistency, missing or long descriptions, TODO placeholders, broken relative links, oversized `SKILL.md`, and script executability/syntax where possible.

## Common failure patterns to prevent

| Failure | Required response |
| --- | --- |
| User says "just write it" | Ask material intake questions or create RED scenario first. |
| User says "no tests" | Explain RED-first is not optional for skill readiness. |
| "It's only reference docs" | Use retrieval/application RED tests. |
| Description summarizes workflow | Rewrite as what+when trigger only. |
| User asks to optimize triggering quickly | Require should-trigger/should-not-trigger suite, baseline/current-description evidence, candidate comparison, and evidence paths before editing. |
| Giant SKILL.md requested | Split detailed material into one-level references. |
| Subagent prompt includes expected answer | Rewrite prompt to use raw task/artifacts only. |
| Agent wants to call ready from vibes | Require validator + skill_test_subagent evidence. |

## Minimal readiness checklist

- [ ] User goal and material preferences understood.
- [ ] Skill type identified.
- [ ] RED scenario files saved.
- [ ] Baseline run failed for the right reason.
- [ ] Skill written with lean progressive disclosure.
- [ ] Description uses what+when without workflow summary.
- [ ] If optimizing a description, should-trigger/should-not-trigger scenarios and baseline/current-description evidence exist.
- [ ] Validator passes or documented warnings are accepted.
- [ ] `skill_test_subagent` evidence shows skill-present improvement.
- [ ] Readiness report includes evidence paths, verdicts, rationale, risks, and next action.
