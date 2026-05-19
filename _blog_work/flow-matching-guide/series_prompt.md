# Flow Matching Series Prompt

Use this prompt to continue the Flow Matching Guide and Code tutorial series.

```text
Use $cv-research-blogger for the Flow Matching Guide and Code series.

Workspace:
- Work only in /Users/quan238/personal/code_space/research-harness-cookiecutter-blog-visual-pipeline.
- Use branch codex/cv-research-blog-visual-pipeline, or create a new codex/flow-matching-series-* branch if this PR has already merged.
- Do not edit /Users/quan238/personal/cv directly.

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
   result the reader should inspect.
2. Generator: write the topic outline, draft the prose, create Mermaid diagrams
   and original image prompts, and build the runnable example around the
   Planner's target.
3. Evaluator: check citations, visual metadata, local assets, equation width,
   human voice, code-result presence, Jekyll build, and browser rendering.

Required modes for each part:
- mode:intake
- mode:visual-plan
- mode:outline
- mode:draft
- mode:code-run
- mode:review
- mode:publish-check

Writing constraints:
- No meta sentences like "this tutorial explains" or "the reader should see".
- No pipeline/process prose in the article body.
- Use direct topic sections, not generic labels.
- Put the practical target before large derivations.
- Keep equations narrow; avoid display math that scrolls.
- Cite core papers for core claims and related papers for design choices.
- Use original local figures or Mermaid diagrams; do not copy or hotlink images.
- Code-result prose should explain what the result shows, not how the pipeline ran.
- End each part with one short sentence saying what the next part covers.

First, plan the whole Flow Matching series. Then implement the next unpublished part.
```
