# Flow Matching Series Handoff

State date: 2026-05-19

## Current State

- Worktree: `/Users/quan238/personal/code_space/research-harness-cookiecutter-blog-visual-pipeline`
- Branch: `main` after FM-03 merge; create a fresh
  `codex/flow-matching-series-*` branch for the next harness task.
- Previous PR: `https://github.com/quanth238/quanth238.github.io/pull/1` (merged before FM-03).
- Main CV checkout at `/Users/quan238/personal/cv` is the clean publication
  target, not the working tree for this pipeline.
- Harness internals must stay in this checkout. Export only approved `_posts`
  files, final `assets/img/blog/flow-matching-guide/` assets, and minimal
  required bibliography/config changes after explicit user approval.
- Part 1 is published on the branch as `_posts/2026-05-19-flow-matching-guide-part-1.md`.
- The cold-start contract is `_blog_work/flow-matching-guide/SESSION_BOOTSTRAP.md`.
- The task source of truth is `_blog_work/flow-matching-guide/series_tasks.yml`; keep `wip_limit: 1`.
- `FM-02` is passing. The Part 1 overview figure is now a local SVG schematic:
  `assets/img/blog/flow-matching-guide/flow-matching-overview.svg`.
- `FM-03` is passing. The full-series plan is stored in
  `_blog_work/flow-matching-guide/series_plan.yml`, with planned visual briefs
  for Parts 2-6 in `_blog_work/flow-matching-guide/visual_sources.yml`.

## Harness Files To Read First

- `AGENTS.md`
- `codex/skills/cv-research-blogger/SKILL.md`
- `codex/skills/cv-research-blogger/visual_quality.md`
- `_blog_work/flow-matching-guide/SESSION_BOOTSTRAP.md`
- `_blog_work/flow-matching-guide/manifest.yml`
- `_blog_work/flow-matching-guide/visual_sources.yml`
- `_blog_work/flow-matching-guide/series_tasks.yml`
- `_blog_work/flow-matching-guide/series_plan.yml`
- `_blog_work/flow-matching-guide/series_prompt.md`
- `_blog_work/flow-matching-guide/EXPORT_POLICY.md`

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

2026-05-19 FM-04 Part 2 draft check:

- Active branch: `codex/flow-matching-series-complete-drafts`.
- FM-04 is passing and no task is currently active.
- Planner verified the current official continuous solver API from
  `facebookresearch/flow_matching` commit
  `11568d37f8d5a080e12aa7b5305d9c35ae07d136`; retained evidence is in
  `_blog_work/flow-matching-guide/remote_runs/20260519T150932Z_fm04_official_api/api_verification.md`.
- Generator created `_drafts/flow-matching-guide-part-2.md`, the deterministic
  example `scripts/blog_pipeline/examples/flow_matching_solver_steps.py`, run
  metadata under
  `_blog_work/flow-matching-guide/remote_runs/20260519T151120Z_fm04_solver_steps/`,
  and the local figure
  `assets/img/blog/flow-matching-guide/flow-matching-solver-steps.svg`.
- Evaluator decision: passed. The draft keeps claims toy-scoped, registers the
  local figure and alt text in `visual_sources.yml`, uses verified solver names
  only, keeps equations narrow, and avoids reader-facing pipeline prose.
- `python3 scripts/blog_pipeline/check_harness.py flow-matching-guide`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-2.md`: passed.
- `python3 -m py_compile scripts/blog_pipeline/*.py scripts/blog_pipeline/examples/*.py`: passed.
- `BUNDLE_GEMFILE=/Users/quan238/personal/cv/Gemfile bundle exec jekyll build --drafts`: passed.

2026-05-19 harness/website separation correction:

- The harness checkout remains the workshop for `_blog_work/`,
  `scripts/blog_pipeline/`, `codex/skills/`, draft files, run logs, and evidence.
- `/Users/quan238/personal/cv` is treated only as the publication target.
- Future export must list exact source-to-target files and receive user approval
  before any personal-site write.
- `python3 scripts/blog_pipeline/check_harness.py flow-matching-guide`: passed.
- YAML parse of `manifest.yml`, `series_plan.yml`, `visual_sources.yml`, and
  `series_tasks.yml`: passed.
- `python3 -m py_compile scripts/blog_pipeline/*.py scripts/blog_pipeline/examples/*.py`: passed.
- `git diff --check`: passed.

2026-05-19 FM-03 series-planning artifact check:

- `python3 scripts/blog_pipeline/check_harness.py flow-matching-guide`: passed after artifact edits.
- YAML parse of `_blog_work/flow-matching-guide/manifest.yml`,
  `_blog_work/flow-matching-guide/series_plan.yml`,
  `_blog_work/flow-matching-guide/visual_sources.yml`, and
  `_blog_work/flow-matching-guide/series_tasks.yml`: passed.
- `git diff --name-only`: showed only tracked allowed planning artifacts:
  `_blog_work/flow-matching-guide/HANDOFF.md`,
  `_blog_work/flow-matching-guide/series_tasks.yml`, and
  `_blog_work/flow-matching-guide/visual_sources.yml`.
- `git status --short`: showed only allowed planning artifacts, including new
  untracked `_blog_work/flow-matching-guide/series_plan.yml`.
- Generator artifacts created or updated:
  `_blog_work/flow-matching-guide/series_plan.yml`,
  `_blog_work/flow-matching-guide/visual_sources.yml`,
  `_blog_work/flow-matching-guide/series_tasks.yml`, and
  `_blog_work/flow-matching-guide/HANDOFF.md`.
- Reader-facing `_drafts` and `_posts` files were not created or edited.
- Evaluator decision: `PASS_WITH_NOTES`. Each planned part has one clear reader
  question, the sequence teaches naturally, planned sections are tied to
  diagnostics or code results, citations support the planned claims, visual
  briefs match the content, code targets are feasible, and no Part 2 prose was
  drafted.

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

Use `$cv-research-blogger` and start with `FM-04` only if the user asks to draft
Part 2. Keep WIP to one task. Before drafting, verify official solver API names
and generate the Part 2 step-count result planned in `series_plan.yml` and
`visual_sources.yml`.

Do not move directly into drafting Part 2 until the visual plan for Part 2 has
figure briefs and cited visual references.

Do not edit `/Users/quan238/personal/cv` while finishing drafts. When all parts
are passing and the user asks to publish, prepare an export manifest first and
wait for approval.

## FM-03 Gaps To Preserve

- Part 2: exact solver APIs and naming in `facebookresearch/flow_matching` are
  not verified.
- Part 3: exact theorem statement and notation from the Flow Matching Guide are
  not verified.
- Part 5: conical Gaussian or diffusion schedule equations need primary-source
  verification before drafting.
- Part 6: official package install/run feasibility in this worktree is
  unverified; keep Part 6 blocked if that check fails.

## Clean Exit Requirements

- Update `series_tasks.yml` with the active task state and evidence.
- Update this handoff with checks run, unresolved blockers, and next action.
- Keep all generated assets local and registered in `visual_sources.yml`.
- Record failed checks explicitly instead of marking a task complete.
