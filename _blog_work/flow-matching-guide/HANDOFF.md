# Flow Matching Series Handoff

State date: 2026-05-19

## Current State

- Worktree: `/Users/quan238/personal/code_space/research-harness-cookiecutter-blog-visual-pipeline`
- Branch: `codex/cv-research-blog-visual-pipeline`
- PR: `https://github.com/quanth238/quanth238.github.io/pull/1`
- Main CV checkout at `/Users/quan238/personal/cv` is not the working tree for this pipeline.
- Part 1 is published on the branch as `_posts/2026-05-19-flow-matching-guide-part-1.md`.
- The cold-start contract is `_blog_work/flow-matching-guide/SESSION_BOOTSTRAP.md`.
- The task source of truth is `_blog_work/flow-matching-guide/series_tasks.yml`; keep `wip_limit: 1`.
- `FM-02` is passing. The Part 1 overview figure is now a local SVG schematic:
  `assets/img/blog/flow-matching-guide/flow-matching-overview.svg`.

## Harness Files To Read First

- `AGENTS.md`
- `codex/skills/cv-research-blogger/SKILL.md`
- `codex/skills/cv-research-blogger/visual_quality.md`
- `_blog_work/flow-matching-guide/SESSION_BOOTSTRAP.md`
- `_blog_work/flow-matching-guide/manifest.yml`
- `_blog_work/flow-matching-guide/visual_sources.yml`
- `_blog_work/flow-matching-guide/series_tasks.yml`
- `_blog_work/flow-matching-guide/series_prompt.md`

## Bootstrap Check

Start a fresh session with:

```bash
python3 scripts/blog_pipeline/check_harness.py flow-matching-guide
python3 scripts/blog_pipeline/check_post.py _posts/2026-05-19-flow-matching-guide-part-1.md
python3 -m py_compile scripts/blog_pipeline/*.py scripts/blog_pipeline/examples/*.py
```

For visual changes, also run the Jekyll build and inspect the rendered page or a
screenshot. A task should not be marked `passing` in `series_tasks.yml` until its
verification command succeeds and the evidence is recorded.

## Latest Verification

2026-05-19 FM-02 overview redesign check:

- `python3 scripts/blog_pipeline/check_harness.py flow-matching-guide`: passed.
- `python3 scripts/blog_pipeline/check_post.py _posts/2026-05-19-flow-matching-guide-part-1.md`: passed.
- `python3 -m py_compile scripts/blog_pipeline/*.py scripts/blog_pipeline/examples/*.py _blog_work/flow-matching-guide/make_overview_schematic.py`: passed.
- `BUNDLE_GEMFILE=/Users/quan238/personal/cv/Gemfile bundle exec jekyll build`: passed.
- Browser verification at `http://127.0.0.1:8765/blog/2026/flow-matching-guide-part-1/`: passed at 1280x720 and 390x844. The SVG loaded with natural size 1600x900, scaled responsively, and did not overflow the viewport.
- Evidence screenshots:
  `_blog_work/flow-matching-guide/evidence/2026-05-19-overview-desktop-fullpage.jpg`
  and `_blog_work/flow-matching-guide/evidence/2026-05-19-overview-mobile.jpg`.

## Visual Quality Note

The Part 1 Mermaid diagram, code-result plots, and overview schematic are now
acceptable because they are editable or generated from local source. The overview
SVG shows exact flow-matching objects: source samples, target samples,
interpolation times, velocity target arrows, learned field arrows, and an ODE
sampling trajectory. The replaced AI bitmap remains registered in
`visual_sources.yml` as archived provenance but is no longer reader-facing.

## Next Recommended Session

Use `$cv-research-blogger` and start with the Planner role. Keep WIP to one
task. The next recommended task is `FM-03`: plan the full Flow Matching series.

Do not move directly into drafting Part 2 until the visual plan for Part 2 has
figure briefs and cited visual references.

## Clean Exit Requirements

- Update `series_tasks.yml` with the active task state and evidence.
- Update this handoff with checks run, unresolved blockers, and next action.
- Keep all generated assets local and registered in `visual_sources.yml`.
- Record failed checks explicitly instead of marking a task complete.
