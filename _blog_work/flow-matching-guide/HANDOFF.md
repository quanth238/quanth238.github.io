# Flow Matching Series Handoff

State date: 2026-05-19

## Current State

- Worktree: `/Users/quan238/personal/code_space/research-harness-cookiecutter-blog-visual-pipeline`
- Branch: `codex/cv-research-blog-visual-pipeline`
- PR: `https://github.com/quanth238/quanth238.github.io/pull/1`
- Main CV checkout at `/Users/quan238/personal/cv` is not the working tree for this pipeline.
- Part 1 is published on the branch as `_posts/2026-05-19-flow-matching-guide-part-1.md`.

## Harness Files To Read First

- `AGENTS.md`
- `codex/skills/cv-research-blogger/SKILL.md`
- `codex/skills/cv-research-blogger/visual_quality.md`
- `_blog_work/flow-matching-guide/manifest.yml`
- `_blog_work/flow-matching-guide/visual_sources.yml`
- `_blog_work/flow-matching-guide/series_tasks.yml`
- `_blog_work/flow-matching-guide/series_prompt.md`

## Visual Quality Note

The Part 1 Mermaid diagram and code-result plots are acceptable because they are
editable or generated from local run data. The overview bitmap is useful as a
draft intuition figure, but it should be redesigned before it becomes the visual
style for the full series. The redesign should show exact flow-matching objects:
source samples, target samples, interpolation times, velocity arrows, learned
field, and ODE sampling trajectory.

## Next Recommended Session

Use `$cv-research-blogger` and start with the Planner role. Keep WIP to one
task. If the user asks to continue the Flow Matching series, first either:

1. Redesign the Part 1 overview figure, or
2. Plan the full series and explicitly carry the Part 1 figure redesign as a
   separate planned task.

Do not move directly into drafting Part 2 until the visual plan for Part 2 has
figure briefs and cited visual references.
