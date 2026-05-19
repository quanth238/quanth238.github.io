---
name: cv-research-blogger
description: Create checkpointed tutorial blog series for Quan Tran Hong's CV site from books, papers, tutorials, and research notes. Use when asked to plan, outline, draft, review, humanize, cite-check, create visual plans, run examples, or publish-check personal research blog posts for the CV site.
metadata:
  short-description: Build checkpointed research blog tutorials for the CV site
---

# CV Research Blogger

Use this skill for tutorial-style research blog posts in the active CV worktree.
The target voice is clear, technical, concise, and useful to students. Go directly
to the concept; do not write meta commentary about the draft, the author's mental
model, or what the post "should help" someone do.

## Harness vs Publication Target

The blog harness is the drafting and verification workspace. Keep `_blog_work/`,
`scripts/blog_pipeline/`, `codex/skills/`, remote-run logs, evidence screenshots,
and working drafts in the harness checkout.

The personal al-folio site is the publication target. Do not edit
`/Users/quan238/personal/cv` during drafting or review. After the series passes
and the user approves publication, prepare an explicit export manifest that lists
only reader-facing `_posts/` files, final local assets under `assets/img/blog/`,
and any minimal bibliography or config changes. Do not export harness internals.

## Agent Roles

- Planner: source intake, literature/blog search, visual-source planning, and citation targets.
- Generator: draft prose, Mermaid diagrams, original AI image prompts, and runnable examples.
- Evaluator: citation support, visual metadata, local asset checks, human voice, remote code-result presence, and Jekyll render checks.

## Three-Role Execution

Use the roles as an explicit handoff, even when one Codex session performs all
of them:

1. Planner decides the practical reader question, core sources, external visual
   references, original-figure plan, and code-result target.
2. Generator writes the outline, prose, Mermaid, image prompts, and runnable
   example around that plan. The generator must not add uncited claims or
   reader-facing process notes.
3. Evaluator checks citations, visual metadata, local assets, equation width,
   human voice, code-result presence, and Jekyll/browser rendering before any
   post is considered publishable.

Do not skip the Planner role for later posts in a series. The next part still
needs its own practical question, visual plan, and code result.

## Harness Contract

Treat the repository as the source of truth. Before continuing a series, read:

- `AGENTS.md`
- this `SKILL.md`
- `codex/skills/cv-research-blogger/visual_quality.md`
- `_blog_work/<series-slug>/manifest.yml`
- `_blog_work/<series-slug>/SESSION_BOOTSTRAP.md` when it exists
- `_blog_work/<series-slug>/visual_sources.yml`
- `_blog_work/<series-slug>/series_tasks.yml` when it exists
- `_blog_work/<series-slug>/HANDOFF.md` when it exists
- `_blog_work/<series-slug>/series_prompt.md` when it exists
- `_blog_work/<series-slug>/EXPORT_POLICY.md` when it exists

Work in one active blog part at a time. Every completed step needs durable
evidence in `_blog_work/<series-slug>/`: source decisions, visual decisions,
code-run metadata, checker output, render status, and the next task. If a new
session cannot recover the current state from those files, the harness is not
complete yet.

## Session Bootstrap

Before writing or drawing, run the cold-start routine:

1. Read the series bootstrap, manifest, visual plan, task list, and handoff.
2. Confirm the task list has `wip_limit: 1` and at most one `active` task.
3. Run `python3 scripts/blog_pipeline/check_harness.py <series-slug>` when the
   series already has bootstrap files.
4. Pick exactly one task from `series_tasks.yml`; if a task needs to start, mark
   it `active` before implementation and write the verification target.
5. Do not mark a task `passing` until its verification command has run and the
   output/evidence path is recorded.

Before ending a session, update `series_tasks.yml` and `HANDOFF.md` with what
changed, what passed, what is blocked, and the next recommended task. A clean
exit requires passing blog checks, current progress, no stale generated assets,
and an explicit startup path for the next session.

## Professional Visual Standard

Read `visual_quality.md` before `visual-plan`, `draft`, `review`, or
`publish-check` work. Every reader-facing figure needs a figure brief before it
is generated or drawn. The brief states the question the figure answers, the
exact objects to show, the visual form, the cited inspiration sources, and what
to avoid.

Use this visual chain for each major concept:

1. Planner collects external diagrams/blogs and cites only the ideas to learn
   from them.
2. Planner writes a figure brief in `_blog_work/<series-slug>/visual_sources.yml`.
3. Generator creates an original Mermaid diagram, data plot, or AI bitmap from
   the brief.
4. Evaluator scores conceptual correctness, visual hierarchy, label quality,
   originality, accessibility, and browser rendering.
5. Weak visuals are marked for redesign instead of being described as
   professional.

Prefer clean local plots, SVGs, and Mermaid for precise technical objects. Use
ChatGPT image generation for intuition-building overview figures only when it
adds clarity. Do not embed equations in AI bitmap figures unless the text is
short and verified after rendering.

## Routing

Expected prompt:

```text
Use $cv-research-blogger with source: <paper/book/tutorial>, audience: CS/ML students, mode: intake|visual-plan|outline|draft|code-run|review|publish-check.
```

Route the work by mode:

- `intake`: collect source metadata, user notes, intended audience, prerequisite level, primary/core papers, supporting tutorials, and what the post should help the reader do.
- `visual-plan`: collect external diagrams/blogs, decide which ideas to cite, and create `_blog_work/<series-slug>/visual_sources.yml`; do not copy or hotlink external figures.
- `outline`: produce a topic-driven outline with required diagrams, minimal theory, code, and missing evidence.
- `draft`: write or revise `_drafts/<series-slug>-part-N.md`; keep the post unpublished.
- `code-run`: run a small reproducible example, preferably through `scripts/blog_pipeline/run_remote_example.py`, and store figures under `assets/img/blog/<series-slug>/`.
- `review`: check explanation quality, citation support, visual clarity, and voice.
- `publish-check`: run `python3 scripts/blog_pipeline/check_post.py <path>` and require explicit user approval before moving anything into `_posts/`.

## Required Workflow

1. Work on a dedicated branch for CV content changes.
2. Use `_blog_work/<series-slug>/manifest.yml` as the source of truth for checkpoints.
3. Use `_blog_work/<series-slug>/visual_sources.yml` for external visual references, figure briefs, original figure prompts, generated asset paths, quality-gate notes, and alt text.
4. Keep posts in `_drafts/` until the outline and final draft are approved.
5. Prefer Mermaid for structural diagrams because the site already renders it and it is easy to edit in git.
6. Use ChatGPT image generation only for original scientific-educational bitmap figures; never copy, trace, or hotlink external diagrams.
7. Treat humanizer-style edits as prose quality checks, not evidence checks.
8. Cite or link every external claim that is not common background knowledge.
9. Keep the harness separate from the publication target; export only approved reader-facing files and assets after explicit user approval.

## Series Continuation

For a new part in an existing series, run:

```bash
python3 scripts/blog_pipeline/new_series.py --slug <series-slug> --part <N>
```

When `_blog_work/<series-slug>/manifest.yml` already exists, `new_series.py`
reuses the saved title, audience, source materials, and visual plan. Do not use
`--force` for normal continuation because it overwrites the manifest and visual
source plan.

## Default Post Shape

Every tutorial draft should include these sections:

- Introduction
- Problem setup
- Path and velocity target
- Training objective
- Minimal implementation
- Code result
- Sampling procedure
- Next part
- References and visual resources

For math-heavy tutorials, use `layout: distill` with:

```yaml
mermaid:
  enabled: true
  zoomable: true
```

## Quality Bar

- Explain from scratch but avoid shallow summaries.
- Write front matter descriptions as a concrete reader promise, not article metadata. Say what the reader will build, understand, or inspect; avoid phrases like "a concise tutorial note that connects...".
- Keep theory to the amount needed for a working mental model.
- Order the tutorial as path, velocity target, loss, minimal code, code result, then theory/sampling.
- Use concrete section titles. Prefer `Path and velocity target` over vague labels such as `Core construction`.
- Use named topic sections instead of generic sections such as "My mental model", "Minimum math", or "Common confusions".
- Show at least one diagram before long derivations, and cite useful external visual explanations.
- Cite the main paper for every core idea and add related papers when they explain design choices, not only external blogs.
- Keep the reference list anchored in core sources. For technical posts, include the primary paper/tutorial, at least two scholarly core sources, and external explanation/visual references when useful.
- Keep display equations narrow. Split side conditions into prose, avoid `\quad` and `\qquad`, and break long objectives into short named equations so mobile and desktop renders do not show formula scrollbars.
- Keep visual-source planning explicit: at least two cited visual/blog references before publication.
- Write a figure brief before creating a bitmap figure, Mermaid diagram, or code-result plot. A figure brief must include purpose, must-show objects, avoided failure modes, status, and cited inspirations.
- Do not accept a generated figure only because it exists. If labels are blurry, composition is generic, colors are confusing, arrows do not match the explanation, or the figure feels like stock art, mark it for redesign.
- Every Mermaid diagram must include `accTitle` and `accDescr` and must render without label overlap at desktop and mobile widths.
- Save original bitmap figures in `assets/img/blog/<series-slug>/` with alt text and prompt provenance.
- In `distill` posts, render local images with `{% include figure.liquid ... class="img-fluid rounded z-depth-1" width="..." height="..." zoomable=true alt="..." %}` so large figures stay responsive and SVGs keep nonzero height.
- Do not use raw HTML image hotlinks. Every image must be a local asset with non-empty alt text.
- Include toy code when the topic is algorithmic.
- Prefer remote runnable examples when the post claims code results.
- Keep provenance and process details out of the article body. Store visual inspiration, image prompts, remote execution details, and run metadata in `_blog_work/<series-slug>/`, not in reader-facing prose.
- Code-result prose should describe what the result shows, not how the pipeline produced it. Do not write sentences such as "I ran a small dependency-light example..." or mention `scripts/blog_pipeline` in the post body.
- State scope positively. Avoid caveats such as "This code does not implement..." unless the missing piece is necessary for correct use; explain what the shown code does and where the next part continues.
- End every series part with a short `Next part` section that says only what the next part will cover, preferably one sentence under 25 words.
- Preserve uncertainty: mark unverified claims instead of inventing support.
- Remove AI-sounding filler, inflated claims, chatbot phrases, generic conclusions, and draft-process notes.
- Do not publish without `publish_ready: true`, `draft_stage: "published"`, and user approval.
