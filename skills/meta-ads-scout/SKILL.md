---
name: meta-ads-scout
description: Search the current Meta Ads Intelligence repository and relevant external sources before creating, duplicating, or extending a skill or module; identify the closest existing workflow, gaps, and safe extension path.
metadata:
  origin: Meta-Ads-Intelligence
---

# Meta Ads Scout

Use this skill before creating a new Meta Ads Intelligence skill, script, workflow, or integration when a search is reasonable.

## When to Use

- The user asks to create or add a new Meta Ads capability.
- The user asks whether the project already supports something.
- The user wants to extend an existing module.
- The user provides another skill repository and wants ideas or compatibility review.

If the user explicitly says to skip discovery and build from scratch, follow that request.

## Step 1 — Capture Intent

Extract:

- requested task
- expected trigger/invocation
- analysis vs action requirement
- browser/API/data source requirement
- affected Meta Ads object: account, campaign, ad set, ad, creative, report, or competitor
- likely keywords and synonyms

## Step 2 — Search Local Repository

Inspect the current project before adding files.

Useful searches:

```bash
find . -maxdepth 3 -name SKILL.md | sort
rg -n "<keyword>|<synonym>" skills scripts references examples tests
```

Prefer extending the closest existing module rather than creating duplicate logic.

## Step 3 — Inspect Related Files

Read only the relevant:

- `SKILL.md`
- module script
- reference methodology
- examples
- tests

Check interfaces and naming conventions before modifying anything.

## Step 4 — External Research

When the user provides or requests external skill references, inspect them before borrowing ideas.

Evaluate:

- skill frontmatter and triggers
- workflow structure
- tool assumptions
- browser requirements
- file writes/network calls
- credential handling
- action safety
- testing strategy
- maintenance quality

Use external work for architectural ideas, not blind copying.

## Step 5 — Decide

Return one of:

### Extend Existing

Use when a close module already covers most of the requested behavior.

### Add Companion Skill

Use when the capability is a distinct user-facing workflow that should have its own trigger and documentation.

### Create Fresh

Use only when no suitable existing surface exists.

## Decision Table

| Situation | Decision |
| --- | --- |
| Same task, missing edge case | Extend existing |
| Same data, different user workflow | Companion skill |
| Duplicate functionality | Do not create; improve existing |
| No relevant module | Create fresh |
| External skill has useful architecture | Adapt ideas after review |

## Action Safety

Discovery never authorizes Meta account changes. A module that recommends an action must remain separate from the module that executes the action.

## Output

Keep the scouting result concise:

```text
Request: <task>
Closest existing module: <path or none>
Overlap: <what already exists>
Gap: <what is missing>
Recommendation: <extend / companion / fresh>
Files to touch: <paths>
Tests needed: <tests>
Action impact: <analysis-only / write-capable>
```

## Anti-Patterns

- Do not create duplicate modules because a filename is different.
- Do not overwrite an existing module without inspecting its current content.
- Do not copy external skill code blindly.
- Do not treat public competitor data as private performance data.
- Do not add API credentials or browser session secrets to the repository.
