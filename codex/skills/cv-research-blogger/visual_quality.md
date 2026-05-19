# Visual Quality Contract

This skill treats figures as part of the explanation, not decoration. A visual is
publishable only when it helps a student reconstruct the idea without reading a
long derivation first.

## Figure Brief Template

Add one entry under `figure_briefs` in
`_blog_work/<series-slug>/visual_sources.yml` before creating the figure:

```yaml
figure_briefs:
  - id: "short-stable-id"
    kind: "mermaid|data-plot|ai-bitmap|svg-schematic"
    reader_question: "What should the reader understand after this figure?"
    purpose: "One sentence on the concept this figure carries."
    must_show:
      - "Concrete object, axis, arrow, state, or transformation."
    avoid:
      - "Known failure mode: vague labels, copied layout, dense text, bad contrast."
    cited_inspirations:
      - "https://example.com/source-used-for-idea-not-pixels"
    status: "planned|created|redesign|approved"
```

## Visual Evaluation Rubric

The Evaluator checks every reader-facing visual against these dimensions:

- Conceptual correctness: arrows, axes, samples, equations, and labels match the
  post and cited sources.
- Reader flow: the eye can follow the concept in the same order as the section.
- Visual hierarchy: the main object is dominant; secondary objects are quieter.
- Label quality: labels are short, readable, and do not overlap marks.
- Technical style: colors are restrained and colorblind-safe; no generic stock
  look, decorative clutter, blurry text, logos, watermarks, or accidental UI.
- Originality: external diagrams are cited as conceptual references only; local
  figures do not copy layout or pixels.
- Web rendering: the figure has local paths, alt text, stable dimensions, and
  renders without overflow in the Jekyll page.

If any dimension fails, mark the relevant brief or figure as `redesign` in the
visual plan. Do not call the figure professional in prose or handoff notes until
the issue is fixed.

## Format Preferences

- Use Mermaid for pipelines, dependency graphs, and state transitions.
- Use matplotlib/SVG for quantitative results, probability paths, samples,
  vector fields, loss curves, and solver comparisons.
- Use AI bitmap generation for high-level intuition only: for example, a
  readable overview of source samples, paths, velocities, vector fields, and
  sampling. The final prompt must be stored in `visual_sources.yml`.
- Keep equations in Markdown/MathJax, not inside generated bitmap figures.
- Prefer a small number of precise labels over dense annotation.

## Flow Matching Visual Direction

For Flow Matching, professional visuals should make the following objects easy
to inspect:

- endpoint samples from source and target distributions;
- the interpolation path at several time values;
- the target velocity as arrows along that path;
- the learned vector field as a function of position and time;
- the ODE sampling trajectory and solver step count when sampling is the topic.

Part 1 can use an overview figure, but later parts should rely more on local
data plots and clean schematic diagrams so the reader sees exact outputs from
the code being discussed.
