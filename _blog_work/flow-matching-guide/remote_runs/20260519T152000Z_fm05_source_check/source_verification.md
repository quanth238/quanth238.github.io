# FM-05 Source Verification

Verification date: `2026-05-19`

Primary sources checked:

- `https://arxiv.org/abs/2412.06264` source archive, `paper.tex`
- `https://arxiv.org/abs/2210.02747` source archive, `fm_arxiv_v2.tex`

Allowed theorem wording for Part 3:

- Flow Matching Guide and Code defines the marginal path as an aggregation of conditional paths, with the quick-tour linear path `X_t = t X_1 + (1-t) X_0`.
- For the conditional OT/linear path conditioned on `x_1`, the guide gives the conditional velocity `u_t(x|x_1) = (x_1 - x)/(1-t)`.
- The guide states the Conditional Flow Matching loss and the marginal Flow Matching loss have identical gradients:
  `nabla_theta L_FM(theta) = nabla_theta L_CFM(theta)`.
- In the general section, the guide states the marginalization trick:
  `u_t(x) = E[u_t(X_t|Z) | X_t=x]` generates the marginal path under the listed assumptions.
- The original Flow Matching paper states the same construction as a marginal vector field
  `u_t(x) = int u_t(x|x_1) p_t(x|x_1) q(x_1) / p_t(x) dx_1`
  and states that the FM and CFM objectives have identical gradients.

Draft guardrails:

- Use theorem language as an explanation, not as a full proof.
- State assumptions qualitatively: conditional velocity must generate the conditional path, the marginal density is positive where the formula is used, and required integrability/regularity conditions are assumed by the theorem.
- Do not claim a single sampled conditional arrow is the sampling-time velocity. The marginal field is an average conditioned on `(X_t=x, t)`.
