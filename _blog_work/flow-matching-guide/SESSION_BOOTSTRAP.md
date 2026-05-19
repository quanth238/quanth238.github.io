# Flow Matching Session Bootstrap

Use this file as the cold-start contract for a fresh agent session. The goal is
that the session can recover the current blog state from repository files alone,
choose one task, and verify it without relying on chat history.

## Read Order

1. `AGENTS.md`
2. `codex/skills/cv-research-blogger/SKILL.md`
3. `codex/skills/cv-research-blogger/visual_quality.md`
4. `_blog_work/flow-matching-guide/manifest.yml`
5. `_blog_work/flow-matching-guide/visual_sources.yml`
6. `_blog_work/flow-matching-guide/series_tasks.yml`
7. `_blog_work/flow-matching-guide/HANDOFF.md`
8. `_blog_work/flow-matching-guide/series_prompt.md`

## Cold-Start Questions

A new session is ready only if it can answer these from repo files:

- What is the active series and current publication state?
- Which file is the source of truth for tasks?
- Which visual assets are approved, created, or marked for redesign?
- What verification commands prove a post or visual change is acceptable?
- What is the next single task under the WIP limit?

## Harness Subsystems

- Instructions: `AGENTS.md`, the CV blogger skill, and `visual_quality.md`.
- Environment: Docker/Jekyll for site rendering, Python scripts under
  `scripts/blog_pipeline/`, and local assets under `assets/img/blog/`.
- State: `manifest.yml`, `series_tasks.yml`, `HANDOFF.md`, remote-run logs, and
  git history.
- Tools: `new_series.py`, `plan_visuals.py`, `run_remote_example.py`,
  `check_post.py`, and `check_harness.py`.
- Feedback: blog checker, Python compile check, Jekyll build, browser/screenshot
  visual review, and evaluator notes in `visual_sources.yml`.

## Start Commands

```bash
python3 scripts/blog_pipeline/check_harness.py flow-matching-guide
python3 scripts/blog_pipeline/check_post.py _posts/2026-05-19-flow-matching-guide-part-1.md
python3 -m py_compile scripts/blog_pipeline/*.py scripts/blog_pipeline/examples/*.py
```

Use the Docker/Jekyll build from `AGENTS.md` when reader-facing pages or visual
rendering change. Use browser or screenshot verification for changed figures.

## Task Rules

- Keep `wip_limit: 1`.
- Treat `_blog_work/flow-matching-guide/series_tasks.yml` as the only task
  source of truth.
- Valid task states are `not_started`, `active`, `blocked`, and `passing`.
- A task moves to `passing` only after the listed verification commands pass.
- Write evidence paths, command output summaries, or build status into
  `series_tasks.yml` or `HANDOFF.md`.

## Current Best Next Task

`FM-02` is the next preferred task: redesign the Part 1 overview figure before
using it as the style reference for later Flow Matching posts. If the user asks
to plan the full series first, keep `FM-02` as a separate tracked task and do
not draft Part 2 until its visual plan has figure briefs and cited references.

## Clean Exit

Before ending a session:

- Update `series_tasks.yml` with state and evidence.
- Update `HANDOFF.md` with current branch, changed files, checks run, blockers,
  and next task.
- Leave generated assets either referenced in `visual_sources.yml` or removed.
- Run the relevant checker commands and record failures explicitly if any remain.
