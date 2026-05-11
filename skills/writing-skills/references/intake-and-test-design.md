# Intake and Test Design

Read this when a user asks to create or improve a skill and the requirements, skill type, or RED scenarios are not yet clear.

## Intake questions

Extract answers from conversation first. Ask only unresolved material questions, preferably with `AskUserQuestion` when the answer changes the resulting skill.

Core intake:

1. What should the skill enable Pi to do?
2. What user phrases or contexts should trigger it?
3. What should the skill produce or change?
4. What should it avoid doing?
5. What examples represent success and failure?
6. What files, APIs, tools, or domain facts are needed?
7. Does the skill need scripts, references, assets, or only SKILL.md?
8. Where should the skill live: `.pi/skills/`, `~/.pi/agent/skills/`, or another path?

Use `AskUserQuestion` for branching choices such as scope, output format, install location, and resource design. If the tool is unavailable in an isolated test harness, ask plain-text questions but preserve explicit labels: Skill type, Trigger conditions, Expected outputs, Success criteria, Edge cases, Resources. Do not ask the user whether to skip RED-first testing; that is part of the method.

## Skill type matrix

| Skill type | What it teaches | RED failure to seek | Scenario style | Success evidence |
| --- | --- | --- | --- | --- |
| Discipline | A rule the agent is tempted to violate | Rationalization, shortcut, user pressure, authority pressure | Pressure scenario with concrete choice | Agent follows the rule under pressure and cites/uses the skill |
| Technique | A procedure or method | Wrong approach, missed step, edge-case failure | Realistic task requiring technique application | Output uses the technique correctly on a new case |
| Pattern | A mental model or recognition heuristic | Fails to recognize when pattern applies or misapplies it | Recognition plus application/counterexample | Agent chooses the pattern only when appropriate |
| Reference | Domain/API/file-format knowledge | Cannot find fact, hallucinates fact, applies reference incorrectly | Retrieval plus application/correct-use task | Agent locates and applies the right reference content |
| Hybrid | Multiple of the above | Any relevant gap | Combine scenario types, but keep each scenario focused | Evidence isolates which part improved |

## Pressure patterns for discipline skills

Good pressure scenarios combine at least three pressures:

- Time: urgent deadline, production incident, deploy window.
- Sunk cost: already wrote the skill or code.
- Authority: user or senior person says skip the method.
- Simplicity: “this is obvious / only documentation.”
- Exhaustion: end of day, want to finish.
- Social pressure: “don’t be dogmatic.”
- Economic pressure: cost or business consequence.

Force a concrete decision. Avoid academic prompts like “what does the skill say?” Use “what do you do now?” or ask the agent to act.

## RED scenario quality gates

A RED scenario is good when:

- It is something a real user might ask.
- The baseline has a realistic reason to fail.
- The expected failure is observable from final output, tool use, or artifacts.
- The skill-present behavior can be checked without knowing hidden intentions.
- It does not leak the desired solution to the subagent.
- It is saved as a scenario file for repeatability.

If baseline passes, do not write the skill yet. Strengthen or replace the scenario until it reveals a real gap, or conclude the skill may not be needed. If `skill_test_subagent` is unavailable, stop before creating final skill artifacts and report the missing baseline evidence.

## Scenario coverage planning

For a new skill, start with 3-5 scenarios:

1. The common happy path.
2. A realistic edge case.
3. A near-miss where the skill should not overreach.
4. A pressure/rationalization case if compliance is costly.
5. A resource/navigation case if references or scripts are involved.

For this writing-skills meta-skill, keep at least five scenarios before calling it ready.
