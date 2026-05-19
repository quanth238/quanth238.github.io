# Flow Matching Series Prompt

Use this prompt to continue the Flow Matching Guide and Code tutorial series.

```text
Use $cv-research-blogger for the Flow Matching Guide and Code series.

Workspace:
- Work only in /Users/quan238/personal/code_space/research-harness-cookiecutter-blog-visual-pipeline.
- Use branch codex/cv-research-blog-visual-pipeline, or create a new codex/flow-matching-series-* branch if this PR has already merged.
- Do not edit /Users/quan238/personal/cv directly.
- Before writing, read AGENTS.md, codex/skills/cv-research-blogger/SKILL.md,
  codex/skills/cv-research-blogger/visual_quality.md, SESSION_BOOTSTRAP.md,
  manifest.yml, visual_sources.yml, series_tasks.yml, HANDOFF.md, and this
  prompt.
- Run python3 scripts/blog_pipeline/check_harness.py flow-matching-guide before
  changing a post, visual, or pipeline file.

Source:
- Primary: https://arxiv.org/abs/2412.06264
- Core references: https://arxiv.org/abs/2210.02747, https://arxiv.org/abs/2302.00482, https://arxiv.org/abs/2209.03003, https://arxiv.org/abs/2303.08797
- Official code: https://github.com/facebookresearch/flow_matching

Goal:
Write the full Flow Matching tutorial series for CS/ML students in my voice:
clear, technical, concise, personal, and useful. Each part should answer one
practical question first, then add only the theory needed to understand it.

Three-role workflow:
1. Planner: choose the practical question for the part, map the core sources,
   collect visual/blog references, plan original figures, and define the code
   result the reader should inspect. Write figure briefs before any figure is
   generated or drawn.
2. Generator: write the topic outline, draft the prose, create Mermaid diagrams
   and original image prompts, and build the runnable example around the
   Planner's target.
3. Evaluator: check citations, visual metadata, local assets, equation width,
   human voice, code-result presence, professional visual quality, Jekyll build,
   and browser rendering.

Required modes for each part:
- mode:intake
- mode:visual-plan
- mode:outline
- mode:draft
- mode:code-run
- mode:review
- mode:publish-check

Harness rules:
- Treat series_tasks.yml as the only source of truth for active work.
- Keep WIP to one task. Valid states are not_started, active, blocked, and
  passing.
- Do not mark a task passing until its verification commands pass and evidence
  is recorded.
- Store visual decisions in visual_sources.yml, code-run logs under
  _blog_work/flow-matching-guide/remote_runs/, and final assets under
  assets/img/blog/flow-matching-guide/.
- End every session by updating HANDOFF.md and the relevant task evidence.

Writing constraints:
- No meta sentences like "this tutorial explains" or "the reader should see".
- No pipeline/process prose in the article body.
- Use direct topic sections, not generic labels.
- Put the practical target before large derivations.
- Keep equations narrow; avoid display math that scrolls.
- Cite core papers for core claims and related papers for design choices.
- Use original local figures or Mermaid diagrams; do not copy or hotlink images.
- Every major visual needs a figure brief in visual_sources.yml before creation.
- Figures should look like professional technical diagrams: clear hierarchy,
  readable labels, colorblind-safe palette, no generic stock-art style, no dense
  text, no copied layout, and no equations embedded in AI bitmaps.
- Prefer local SVG/matplotlib plots for precise flow paths, vector fields,
  losses, samples, and solver comparisons.
- Code-result prose should explain what the result shows, not how the pipeline ran.
- End each part with one short sentence saying what the next part covers.

First, inspect the handoff and visual task list. Then plan the whole Flow
Matching series. Implement only one active part or visual redesign at a time.
```
