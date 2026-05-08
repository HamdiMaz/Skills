---
name: guiding-product-specs
description: Use when a user asks to create or refine a product spec, MVP spec, PRD, requirements document, user flows, dashboard states, auth/upload/answering flows, scoring behavior, or in/out-of-scope boundaries from an idea.
---

# Guiding Product Specs

## Overview

Turn rough product ideas into approved product specs through structured discovery, explicit trade-offs, and section-by-section review.

**Core principle:** Do not draft the spec from assumptions. First learn what the user wants, using `AskUserQuestion` when available.

## Required Behavior

1. **Load context first**
   - Read relevant docs/specs, project files, and recent commits.
   - Note existing constraints so questions build on known decisions.

2. **Use structured discovery**
   - If `AskUserQuestion` exists, use it for discovery and approvals.
   - Ask one focused question per call unless questions are tightly related.
   - Prefer 2-4 concrete options.
   - Put the recommended option first and suffix its label with ` (Recommended)`.
   - Do not include `Other`; the tool adds it.
   - Keep headers short.
   - If the tool is unavailable, say so and ask one concise multiple-choice question per message.

3. **Question sequence**
   Cover these before drafting unless already answered:
   - audience and access model
   - auth/signup/profile fields
   - first-time user journey
   - language/locale behavior
   - upload/source-material model
   - configuration vs zero-config flow
   - generated content types/counts
   - dashboard states and card actions
   - quiz/task answering flow
   - feedback timing
   - scoring, attempts, and results
   - quotas/limits
   - deletion, retention, privacy, and consent
   - in-scope and out-of-scope items
   - success criteria

4. **Explore alternatives before locking direction**
   Present 2-3 product approaches with trade-offs and a recommendation. Ask the user to choose before writing sections.

5. **Present sections for approval**
   Draft sections incrementally. After each section, ask whether it looks right before continuing.

   Typical sections:
   - purpose, audience, and MVP boundary
   - auth flow
   - upload flow
   - dashboard states
   - quiz/answering flow
   - score/result behavior
   - final in/out-of-MVP scope
   - risks and trade-offs

6. **Write, self-review, and commit**
   - Save the approved spec to the user-requested path, or `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`.
   - Self-review for placeholders, contradictions, ambiguity, and scope creep.
   - Run `grep` for placeholders and `git diff --check`.
   - Commit only the spec file; do not stage unrelated user changes.
   - Before claiming success, use verification-before-completion if available.
   - Ask the user to review the written spec before implementation planning.

## Quick Reference

| Situation | Do |
|---|---|
| User says “create an MVP spec” | Read context, then start structured discovery |
| User says “ask me questions” | Use `AskUserQuestion`; do not dump inline lists |
| User asks to move fast | Ask only high-impact questions, but do not invent core flows |
| Answers reveal scope conflict | Clarify or decompose before drafting |
| User approves a section | Continue to the next section |
| User corrects an answer | Update the emerging spec and continue |

## Good Opening Pattern

```text
I’ll first read the existing context so the questions line up with prior decisions.
```

Then use `AskUserQuestion`, for example:

```text
Who should the MVP primarily serve in the first pilot?
- Self-serve students (Recommended)
- Invite-only students
- Teacher-led classes
- Admin-created quizzes
```

## Red Flags

Stop and correct course if you are about to:

- draft the whole spec before discovery
- invent roles, payments, admin features, or workflows
- ask 10+ inline questions when `AskUserQuestion` is available
- skip the 2-3 approach comparison
- write the file before section approval
- claim the spec is complete without verification evidence
- commit unrelated files
- move to implementation planning before the user reviews the written spec

## Common Mistakes

| Mistake | Fix |
|---|---|
| “I’ll assume…” for major product behavior | Ask a structured question |
| Generic dashboard states | Ask what states matter for this product |
| Treating uploaded files as manageable by default | Ask the source-material/product model |
| Asking every possible question | Ask sequentially and stop when decisions are sufficient |
| Approvals only at the end | Review after each major section |
| Tool unavailable means no structure | Use one concise multiple-choice question per message |
