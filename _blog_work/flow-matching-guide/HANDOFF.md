# Flow Matching Series Handoff

State date: 2026-05-19

## Current State

- Worktree: `/Users/quan238/personal/code_space/research-harness-cookiecutter-blog-visual-pipeline`
- Branch: `codex/flow-matching-series-review-revisions`.
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
- `FM-04` through `FM-08` are passing. Drafts for Parts 2-6 are in `_drafts/`.
- `FM-09` is passing. The clean export manifest is
  `_blog_work/flow-matching-guide/export_manifest.yml`; no export has been
  performed and `/Users/quan238/personal/cv` was not modified.
- `FM-10` is passing. The Revision Agent changed only the
  Problem setup transition in
  `_posts/2026-05-19-flow-matching-guide-part-1.md` to distinguish the missing
  direct marginal velocity target from the endpoint-conditioned target used in
  the next section. Part 1 visual metadata in `visual_sources.yml` was tightened
  to explicitly approve/register the final reader-facing Part 1 visuals. No
  visual assets, Parts 2-6 drafts, export files, or personal CV files were changed.
- `FM-11` is passing. The Revision Agent tightened the Part 2 official-package
  paragraph to be version-scoped to `flow_matching==1.0.10` and kept the
  solver-step diagnostic centered on the hand-written Euler loop. Part 2 visual
  metadata now records local ownership and no paper-figure extraction for the
  solver-step SVG.
- `FM-12` is passing. The Revision Agent added the Part 3 bridge around
  target-conditioned notation, scoped the population-objective theorem wording,
  and registered/approved Part 3 visual ownership metadata.
- `FM-13` is passing. The Revision Agent narrowed Part 4 scope to endpoint/path
  geometry and toy diagnostics, and kept sampling-cost language as a hypothesis
  rather than a demonstrated result.
- `FM-14` is passing. The Revision Agent added the Linear VP late-time endpoint
  caveat and tied the toy implementation to the epsilon clamp.
- `FM-15` is passing. The Revision Agent corrected the official-package bridge
  metric semantics in code and draft prose. The coordinator regenerated the
  package bridge JSON/SVG in a temporary `flow_matching==1.0.10` environment.
- No review/revision task is currently active.

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
- `_blog_work/flow-matching-guide/export_manifest.yml` when reviewing export readiness

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

2026-05-19 FM-10 Part 1 revision update:

- Active branch: `codex/flow-matching-series-review-revisions`.
- Accepted Planner/Critic decision: revise only the Part 1 Problem setup
  transition; keep all existing visuals; do not add diagrams; do not edit Parts
  2-6; do not export.
- Revision changed `_posts/2026-05-19-flow-matching-guide-part-1.md` so the
  unavailable direct target is the direct marginal velocity target, while the
  endpoint-conditioned path velocity remains the tractable target introduced in
  the next section.
- `visual_sources.yml` was tightened for Part 1 visual approvals: the Mermaid
  pipeline is explicitly approved and registered with source post, accTitle /
  accDescr note, local-original/editable ownership, and no paper-figure
  extraction; the overview, loss, and path SVGs now record local ownership and
  no paper-figure extraction, with loss and path marked approved.
- `python3 scripts/blog_pipeline/check_harness.py flow-matching-guide`: passed.
- `python3 scripts/blog_pipeline/check_post.py _posts/2026-05-19-flow-matching-guide-part-1.md`: passed.
- `python3 -m py_compile scripts/blog_pipeline/*.py scripts/blog_pipeline/examples/*.py`: passed.
- `BUNDLE_GEMFILE=/Users/quan238/personal/cv/Gemfile bundle exec jekyll build --drafts`: passed.
- Rendered HTML check after build: `/blog/` contains the expected
  `flow-matching`, `tutorial`, and `generative-modeling` tag links; Flow
  Matching Parts 1-6 contain Contents; footer/copyright/powered-by strings are
  absent from `/blog/` and Flow Matching Parts 1-6.
- `FM-10` is passing; `FM-11` is active.

2026-05-19 FM-11 Part 2 revision update:

- Active branch: `codex/flow-matching-series-review-revisions`.
- Accepted Planner/Critic decision: revise only the Part 2 official-package
  paragraph around Minimal implementation; scope it to `flow_matching==1.0.10`;
  present it as a bridge to Part 6; avoid process phrasing; keep the solver-step
  result toy-scoped; do not add diagrams.
- Revision changed `_drafts/flow-matching-guide-part-2.md` so the ODESolver
  paragraph is version-scoped and points forward to Part 6 while the Part 2
  diagnostic remains centered on the hand-written Euler loop.
- `visual_sources.yml` was tightened for the Part 2 final solver-step SVG:
  `flow-matching-solver-steps.svg` now records local-original/reproducible code
  ownership and no paper-figure extraction.
- `python3 scripts/blog_pipeline/check_harness.py flow-matching-guide`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-2.md`: passed.
- `python3 -m py_compile scripts/blog_pipeline/*.py scripts/blog_pipeline/examples/*.py`: passed.
- `BUNDLE_GEMFILE=/Users/quan238/personal/cv/Gemfile bundle exec jekyll build --drafts`: passed.
- Rendered HTML check after build: `/blog/` contains the expected
  `flow-matching`, `tutorial`, and `generative-modeling` tag links; Flow
  Matching Parts 1-6 contain Contents; footer/copyright/powered-by strings are
  absent from `/blog/` and Flow Matching Parts 1-6.
- `FM-11` is passing; `FM-12` is active.

2026-05-19 FM-12 Part 3 revision update:

- Active branch: `codex/flow-matching-series-review-revisions`.
- Accepted Planner/Critic decision: revise only Part 3; add a short bridge
  before the target-conditioned formula so it is not confused with paired
  endpoint paths; scope theorem wording to the population objective, same
  conditional path, and regularity assumptions; do not expand the math; do not
  add diagrams.
- Revision changed `_drafts/flow-matching-guide-part-3.md` to distinguish the
  target-conditioned path from the paired-endpoint implementation and to name
  the theorem scope before the gradient-equivalence equation.
- `visual_sources.yml` was tightened for Part 3: the Mermaid argument map is
  explicitly approved and registered with source post, accTitle / accDescr note,
  local-original/editable ownership, and no paper-figure extraction; the
  conditional-to-marginal arrows SVG records local reproducible-code ownership
  and no paper-figure extraction.
- `python3 scripts/blog_pipeline/check_harness.py flow-matching-guide`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-3.md`: passed.
- `python3 -m py_compile scripts/blog_pipeline/*.py scripts/blog_pipeline/examples/*.py`: passed.
- `BUNDLE_GEMFILE=/Users/quan238/personal/cv/Gemfile bundle exec jekyll build --drafts`: passed.
- Rendered HTML check after build: `/blog/` contains the expected
  `flow-matching`, `tutorial`, and `generative-modeling` tag links; Flow
  Matching Parts 1-6 contain Contents; footer/copyright/powered-by strings are
  absent from `/blog/` and Flow Matching Parts 1-6.
- `FM-12` is passing; `FM-13` is active.

2026-05-19 FM-13 Part 4 revision update:

- Active branch: `codex/flow-matching-series-review-revisions`.
- Accepted Planner/Critic decision: do not add a new sampling-cost diagnostic or
  diagram; narrow Part 4 reader-facing and planning scope from path quality and
  sampling cost to endpoint/path geometry and toy diagnostics; keep the guarded
  OT-CFM and Rectified Flow wording; avoid implying minibatch OT is globally
  optimal or directly proven to reduce sampling cost in this toy result.
- Revision changed `_blog_work/flow-matching-guide/series_plan.yml` so the Part
  4 reader question and objective focus on endpoint/path geometry and toy
  diagnostics.
- Revision changed `_drafts/flow-matching-guide-part-4.md` so solver-cost
  language is a hypothesis for later inspection, not a result demonstrated by
  the current coupling diagnostic.
- `visual_sources.yml` was tightened for Part 4: the coupling diagnostic SVG now
  records local-original/reproducible-code-result ownership and no paper-figure
  extraction.
- `python3 scripts/blog_pipeline/check_harness.py flow-matching-guide`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-4.md`: passed.
- `python3 -m py_compile scripts/blog_pipeline/*.py scripts/blog_pipeline/examples/*.py`: passed.
- `BUNDLE_GEMFILE=/Users/quan238/personal/cv/Gemfile bundle exec jekyll build --drafts`: passed.
- Rendered HTML check after build: `/blog/` contains the expected
  `flow-matching`, `tutorial`, and `generative-modeling` tag links; Flow
  Matching Parts 1-6 contain Contents; footer/copyright/powered-by strings are
  absent from `/blog/` and Flow Matching Parts 1-6.
- `FM-13` is passing; `FM-14` is active.

2026-05-19 FM-14 Part 5 revision update:

- Active branch: `codex/flow-matching-series-review-revisions`.
- Accepted Planner/Critic decision: add a short note near the Linear VP
  schedule/velocity target that `sigma_t = sqrt(1-t^2)` has singular or
  large-velocity behavior as `t` approaches 1; state that the toy comparison
  evaluates `t < 1` or uses an epsilon guard; connect this to the clamp in the
  minimal implementation; keep diffusion/probability-flow wording modest and
  source-tied; do not add diagrams.
- Revision changed `_drafts/flow-matching-guide-part-5.md` near the Linear VP
  velocity target and minimal implementation to explain the endpoint behavior
  and the `torch.clamp(..., min=1e-6)` guard.
- `visual_sources.yml` was tightened for Part 5: the path-family snapshots SVG
  now records local-original/reproducible-code-result ownership and no
  paper-figure extraction.
- `python3 scripts/blog_pipeline/check_harness.py flow-matching-guide`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-5.md`: passed.
- `python3 -m py_compile scripts/blog_pipeline/*.py scripts/blog_pipeline/examples/*.py`: passed.
- `BUNDLE_GEMFILE=/Users/quan238/personal/cv/Gemfile bundle exec jekyll build --drafts`: passed.
- Rendered HTML check after build: `/blog/` contains the expected
  `flow-matching`, `tutorial`, and `generative-modeling` tag links; Flow
  Matching Parts 1-6 contain Contents; footer/copyright/powered-by strings are
  absent from `/blog/` and Flow Matching Parts 1-6.
- `FM-14` is passing; `FM-15` is active.

2026-05-19 FM-15 Part 6 revision update:

- Active branch: `codex/flow-matching-series-review-revisions`.
- Accepted Planner/Critic decision: fix the official package bridge metric so
  solver/path agreement compares `solved[-1]` with the exact `CondOTProbPath`
  sample at the same final time, `t=0.98`; keep endpoint distance as a separately
  named remaining-distance metric; fix the 32-interval time-grid snippet; remove
  process phrasing and the reader-facing `_blog_work` reference; reduce the
  discrete side branch; do not add diagrams.
- Revision changed `scripts/blog_pipeline/examples/flow_matching_official_package_bridge.py`
  so future runs write `mean_solver_path_gap_at_final_time` /
  `max_solver_path_gap_at_final_time` and separately named remaining-distance
  metrics.
- Revision updated the existing
  `_blog_work/flow-matching-guide/remote_runs/20260519T155000Z_fm08_official_package/official_package_smoke_test.json`
  metric names and the existing
  `assets/img/blog/flow-matching-guide/flow-matching-official-package-bridge.svg`
  label so the intentional `t=0.98` to `t=1.0` gap is no longer described as
  solver error.
- Coordinator reran the package bridge in `/tmp/fm15-flow-matching-venv` after
  installing `flow_matching==1.0.10` and `tqdm`. The regenerated metadata records
  `mean_solver_path_gap_at_final_time=1.433954537333193e-07` and
  `mean_remaining_distance_to_endpoint_at_final_time=0.05236712470650673`.
- Revision changed `_drafts/flow-matching-guide-part-6.md` with
  version-scoped `flow_matching==1.0.10` wording, a 33-point time grid for 32
  intervals, corrected code-result prose, a short discrete-components pointer,
  and no reader-facing `_blog_work` reference.
- `visual_sources.yml` was tightened for Part 6: the Mermaid component map is
  explicitly approved and registered with source post, accTitle / accDescr note,
  local-original/editable ownership, and no paper-figure extraction; the official
  package bridge SVG records local reproducible-code ownership and no
  paper-figure extraction.
- `python3 scripts/blog_pipeline/check_harness.py flow-matching-guide`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-6.md`: passed.
- `python3 -m py_compile scripts/blog_pipeline/*.py scripts/blog_pipeline/examples/*.py`: passed.
- `BUNDLE_GEMFILE=/Users/quan238/personal/cv/Gemfile bundle exec jekyll build --drafts`: passed.
- Rendered HTML check after build: `/blog/` contains the expected
  `flow-matching`, `tutorial`, and `generative-modeling` tag links; Flow
  Matching Parts 1-6 contain Contents; footer/copyright/powered-by strings are
  absent from `/blog/` and Flow Matching Parts 1-6.
- `FM-15` is passing; no review/revision task is currently active.

2026-05-19 final review/revision suite:

- Active branch: `codex/flow-matching-series-review-revisions`.
- `python3 scripts/blog_pipeline/check_harness.py flow-matching-guide`: passed.
- `python3 scripts/blog_pipeline/check_post.py _posts/2026-05-19-flow-matching-guide-part-1.md`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-2.md`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-3.md`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-4.md`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-5.md`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-6.md`: passed.
- `python3 -m py_compile scripts/blog_pipeline/*.py scripts/blog_pipeline/examples/*.py`: passed.
- `BUNDLE_GEMFILE=/Users/quan238/personal/cv/Gemfile bundle exec jekyll build --drafts`: passed.
- Rendered HTML check after final build: `/blog/` contains the expected
  `flow-matching`, `tutorial`, and `generative-modeling` tag links; Flow
  Matching Parts 1-6 contain Contents; footer/copyright/powered-by strings are
  absent from `/blog/` and Flow Matching Parts 1-6.
- Export manifest updated but export not performed. `/Users/quan238/personal/cv`
  was not modified.

2026-05-19 blog index footer and tag follow-up:

- Active branch: `codex/flow-matching-series-complete-drafts`.
- The blog index `_pages/blog.md` now sets `hide_footer: true`.
- The default and Distill layouts now respect `page.hide_footer` before including
  the al-folio footer.
- `_config.yml` now displays the `flow-matching`, `tutorial`, and
  `generative-modeling` tags on the blog index.
- Flow Matching Parts 1-6 now include the `flow-matching` tag.
- `_blog_work/flow-matching-guide/export_manifest.yml` now records the required
  layout, page, and config changes for a future approved export. Those target
  files already exist in `/Users/quan238/personal/cv`, so they are marked as
  overwrites in the manifest. No personal CV files were modified.
- `python3 scripts/blog_pipeline/check_harness.py flow-matching-guide`: passed.
- `python3 scripts/blog_pipeline/check_post.py _posts/2026-05-19-flow-matching-guide-part-1.md`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-2.md`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-3.md`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-4.md`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-5.md`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-6.md`: passed.
- `BUNDLE_GEMFILE=/Users/quan238/personal/cv/Gemfile bundle exec jekyll build --drafts`: passed.
- Live `http://127.0.0.1:8080/blog/` check: `flow-matching` tag present and
  copyright/powered-by footer absent.

2026-05-19 FM-09 export manifest check:

- Active branch: `codex/flow-matching-series-complete-drafts`.
- FM-09 is passing and no task is currently active.
- Generator created `_blog_work/flow-matching-guide/export_manifest.yml`.
- The manifest lists Part 1 as an existing harness `_posts` source and Parts 2-6
  as draft-to-post promotions that require explicit approval before export.
- The manifest lists final assets under `assets/img/blog/flow-matching-guide/`
  and excludes `_blog_work/`, `scripts/blog_pipeline/`, `codex/skills/`,
  `_drafts/`, remote-run logs, evidence screenshots, helper scripts, and the
  unused AI overview PNG.
- Read-only target checks found no existing personal CV target files for the
  proposed posts or final assets at manifest time; `overwrites_existing_target`
  is false for every listed item.
- No files were copied, created, or modified under `/Users/quan238/personal/cv`.
- `python3 scripts/blog_pipeline/check_harness.py flow-matching-guide`: passed.
- YAML parse of `manifest.yml`, `series_plan.yml`, `visual_sources.yml`,
  `series_tasks.yml`, and `export_manifest.yml`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-2.md`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-3.md`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-4.md`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-5.md`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-6.md`: passed.
- `python3 -m py_compile scripts/blog_pipeline/*.py scripts/blog_pipeline/examples/*.py`: passed.
- `BUNDLE_GEMFILE=/Users/quan238/personal/cv/Gemfile bundle exec jekyll build --drafts`: passed.

2026-05-19 FM-08 Part 6 draft check:

- Active branch: `codex/flow-matching-series-complete-drafts`.
- FM-08 is passing and no task is currently active.
- Planner verified package install/run feasibility with `flow_matching==1.0.10`
  in a temporary venv; retained evidence is in
  `_blog_work/flow-matching-guide/remote_runs/20260519T155000Z_fm08_official_package/package_verification.md`.
- The installed package exports `CondOTProbPath`, not `CondOTPath`; Part 6 uses
  the verified installed name.
- Generator created `_drafts/flow-matching-guide-part-6.md`, the deterministic
  example `scripts/blog_pipeline/examples/flow_matching_official_package_bridge.py`,
  run metadata under
  `_blog_work/flow-matching-guide/remote_runs/20260519T155000Z_fm08_official_package/`,
  and the local figure
  `assets/img/blog/flow-matching-guide/flow-matching-official-package-bridge.svg`.
- Evaluator decision: passed. The draft maps toy concepts to verified package
  components, includes Mermaid accessibility metadata, records the package API
  naming difference, and keeps the output claim to a component run check.
- `python3 scripts/blog_pipeline/check_harness.py flow-matching-guide`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-6.md`: passed.
- `python3 -m py_compile scripts/blog_pipeline/*.py scripts/blog_pipeline/examples/*.py`: passed.
- `BUNDLE_GEMFILE=/Users/quan238/personal/cv/Gemfile bundle exec jekyll build --drafts`: passed.
- Post-FM-08 full draft suite passed for Parts 2-6: `check_harness`, all
  draft `check_post.py` commands, `py_compile`, and the Jekyll drafts build.

2026-05-19 FM-07 Part 5 draft check:

- Active branch: `codex/flow-matching-series-complete-drafts`.
- FM-07 is passing and no task is currently active.
- Planner verified Conditional OT, Linear VP, Gaussian path, and
  probability-flow ODE claim scope; retained evidence is in
  `_blog_work/flow-matching-guide/remote_runs/20260519T154000Z_fm07_source_check/source_verification.md`.
- Generator created `_drafts/flow-matching-guide-part-5.md`, the deterministic
  example `scripts/blog_pipeline/examples/flow_matching_path_families.py`, run
  metadata under
  `_blog_work/flow-matching-guide/remote_runs/20260519T154210Z_fm07_path_families/`,
  and the local figure
  `assets/img/blog/flow-matching-guide/flow-matching-path-family-snapshots.svg`.
- Evaluator decision: passed. The draft uses only source-verified schedules,
  keeps schedule equations in Markdown, scopes the diffusion discussion to
  Gaussian paths and probability-flow ODEs, and registers the local figure with
  alt text.
- `python3 scripts/blog_pipeline/check_harness.py flow-matching-guide`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-5.md`: passed.
- `python3 -m py_compile scripts/blog_pipeline/*.py scripts/blog_pipeline/examples/*.py`: passed.
- `BUNDLE_GEMFILE=/Users/quan238/personal/cv/Gemfile bundle exec jekyll build --drafts`: passed.

2026-05-19 FM-06 Part 4 draft check:

- Active branch: `codex/flow-matching-series-complete-drafts`.
- FM-06 is passing and no task is currently active.
- Planner verified OT-CFM and Rectified Flow claim scope; retained evidence is
  in
  `_blog_work/flow-matching-guide/remote_runs/20260519T153000Z_fm06_source_check/source_verification.md`.
- Generator created `_drafts/flow-matching-guide-part-4.md`, the deterministic
  example `scripts/blog_pipeline/examples/flow_matching_coupling_diagnostics.py`,
  run metadata under
  `_blog_work/flow-matching-guide/remote_runs/20260519T153215Z_fm06_coupling_diagnostics/`,
  and the local figure
  `assets/img/blog/flow-matching-guide/flow-matching-coupling-diagnostics.svg`.
- Evaluator decision: passed. The draft explicitly scopes minibatch OT as a
  batch-local assignment, avoids global OT claims, keeps Rectified Flow as
  straight-path motivation, and registers the local figure with alt text.
- `python3 scripts/blog_pipeline/check_harness.py flow-matching-guide`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-4.md`: passed after splitting a display equation side condition.
- `python3 -m py_compile scripts/blog_pipeline/*.py scripts/blog_pipeline/examples/*.py`: passed.
- `BUNDLE_GEMFILE=/Users/quan238/personal/cv/Gemfile bundle exec jekyll build --drafts`: passed.

2026-05-19 FM-05 Part 3 draft check:

- Active branch: `codex/flow-matching-series-complete-drafts`.
- FM-05 is passing and no task is currently active.
- Planner verified theorem wording against `Flow Matching Guide and Code` and
  `Flow Matching for Generative Modeling`; retained evidence is in
  `_blog_work/flow-matching-guide/remote_runs/20260519T152000Z_fm05_source_check/source_verification.md`.
- Generator created `_drafts/flow-matching-guide-part-3.md`, the deterministic
  example `scripts/blog_pipeline/examples/flow_matching_conditional_marginal.py`,
  run metadata under
  `_blog_work/flow-matching-guide/remote_runs/20260519T152215Z_fm05_conditional_marginal/`,
  and the local figure
  `assets/img/blog/flow-matching-guide/flow-matching-conditional-marginal-arrows.svg`.
- Evaluator decision: passed. The draft distinguishes conditional endpoint
  velocities from the marginal sampling field, uses source-verified theorem
  language, includes Mermaid accessibility metadata, and keeps all assets local.
- `python3 scripts/blog_pipeline/check_harness.py flow-matching-guide`: passed.
- `python3 scripts/blog_pipeline/check_post.py _drafts/flow-matching-guide-part-3.md`: passed.
- `python3 -m py_compile scripts/blog_pipeline/*.py scripts/blog_pipeline/examples/*.py`: passed.
- `BUNDLE_GEMFILE=/Users/quan238/personal/cv/Gemfile bundle exec jekyll build --drafts`: passed.

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

FM-10 through FM-15 are passing and no review/revision task is active. The next
step is not an export by default. If the user asks to publish, first present the
updated `_blog_work/flow-matching-guide/export_manifest.yml` for explicit
approval, including the source-to-target post list, final assets, required site
changes, overwrites, and verification evidence.

Do not edit `/Users/quan238/personal/cv` until the user approves that export
manifest. No old FM-03 verification gaps remain open; the solver API, theorem
wording, path schedules, and package install/run feasibility were verified in
FM-04 through FM-08 and rechecked during this review pass where needed.

## Clean Exit Requirements

- `series_tasks.yml` records `current_state: "fm-15-passing"` and
  `active_task: null`.
- This handoff records the final review/revision suite and rendered HTML checks.
- Generated assets remain local and registered in `visual_sources.yml`.
- Export is still approval-gated and has not been performed.
