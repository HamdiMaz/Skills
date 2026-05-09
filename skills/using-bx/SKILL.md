---
name: using-bx
description: Use when needing general web search, current public web facts, news, factual research, source grounding, non-documentation lookups, fact-checking, or public web content via the Brave Search CLI; not for library, framework, SDK, CLI, cloud-service, API, setup, configuration, or migration documentation, where find-docs applies.
---

# Using bx

## Overview

`bx` is the Brave Search CLI for general web search and grounding. Default to `bx "query"` for RAG-ready extracted web content.

**Core rule:** Do not use `bx` for developer documentation lookups. For libraries, frameworks, SDKs, CLIs, cloud services, API syntax, setup, configuration, migrations, or version-specific docs, use `find-docs` first.

## Command Choice

| Need | Command |
|---|---|
| Grounded web content | `bx "query"` |
| Synthesized answer | `bx answers "query" --no-stream` |
| Deep research | `bx answers "query" --enable-research --no-stream` |
| Traditional results | `bx web "query"` |
| Forums/discussions | `bx web "query" --result-filter discussions` |
| Recent news | `bx news "query" --freshness pd` |
| Images/videos/places | `bx images`, `bx videos`, `bx places "query" --location "city"` |

For large results, constrain context:

```bash
bx "topic" --max-tokens 4096 --max-tokens-per-url 1024 --max-urls 5 --threshold strict
```

## Routing Rules

| User asks for | Use |
|---|---|
| Current facts, public claims, companies, people, events, policies, statistics | `bx "query"` |
| Breaking or recent events | `bx news "query" --freshness pd` |
| Broad multi-source research | `bx answers "query" --enable-research --no-stream` |
| Official library/framework/API/CLI/cloud docs, code examples, setup, config, migrations | `find-docs` |
| Library-specific error behavior | `find-docs` first; use `bx web ... --result-filter discussions` only for non-official community reports |

Use `bx` for documentation only when the user explicitly overrides the normal `find-docs` route. State that `find-docs` is the preferred documentation tool before doing so.

## Workflow

1. Sanitize the query: remove secrets, private code, credentials, personal data, and proprietary details.
2. Pick the narrowest command from the table.
3. Run `command -v bx` if availability is unknown. If missing, tell the user; install only with permission:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/brave/brave-search-cli/main/scripts/install.sh | sh
   ```
4. Run the search. All output is JSON on stdout; errors are on stderr.
5. Synthesize results with citations/URLs. Distinguish verified facts from uncertain or conflicting claims.

## Error Handling

| Exit | Meaning | Action |
|---|---|---|
| 1-2 | Bad request or flags | Fix query/arguments |
| 3 | Auth/permission | Check `bx config show-key` or `BRAVE_SEARCH_API_KEY` |
| 4 | Rate limited | Retry later/back off |
| 5 | Server/network | Retry with backoff |

## Red Flags

- Using `bx` because upstream docs mention documentation lookup in general.
- Searching official developer docs with `bx` instead of `find-docs`.
- Adding documentation-search examples such as `--include-site docs.*` to this skill.
- Including API keys, credentials, private URLs, or proprietary code in a query.
- Answering current factual questions from training data when `bx` is available.
- Returning raw JSON instead of a concise synthesis with source URLs.
