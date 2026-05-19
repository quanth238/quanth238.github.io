# FM-06 Source Verification

Verification date: `2026-05-19`

Primary sources checked:

- `https://arxiv.org/abs/2302.00482`
- `https://arxiv.org/abs/2209.03003`
- `https://arxiv.org/abs/2412.06264`

Allowed claims for Part 4:

- Conditional Flow Matching permits different conditional constructions and endpoint couplings.
- OT-CFM is reported as creating simpler flows and faster inference in the authors' experiments.
- When the true OT plan is available, OT-CFM approximates dynamic OT; a minibatch assignment is only a finite-batch approximation used as a training heuristic.
- Rectified Flow learns ODE models that follow straight paths between empirically observed distributions as much as possible.
- Rectification is reported to produce increasingly straight paths that can be simulated accurately with coarse time discretization.

Draft guardrails:

- Do not claim minibatch OT is the global OT plan for the full data distribution.
- Keep code-result metrics as toy diagnostics: batch transport cost, segment crossings, and endpoint geometry.
- Cite Rectified Flow for straight-path and coarse-discretization motivation, not as the same algorithm as minibatch OT-CFM.
