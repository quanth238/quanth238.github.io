# FM-07 Source Verification

Verification date: `2026-05-19`

Primary sources checked:

- `https://arxiv.org/abs/2412.06264` source archive, `paper.tex`
- `https://arxiv.org/abs/2303.08797`
- `https://arxiv.org/abs/2210.02747`

Allowed path equations for Part 5:

- Affine conditional flow:
  `psi_t(x|x_1) = alpha_t x_1 + sigma_t x`.
- Scheduler boundary conditions:
  `alpha_0 = 0`, `alpha_1 = 1`, `sigma_0 = 1`, `sigma_1 = 0`, with monotone alpha and sigma on `(0,1)`.
- Conditional OT schedule listed by the guide:
  `alpha_t = t`, `sigma_t = 1-t`.
- Linear VP schedule listed by the guide:
  `alpha_t = t`, `sigma_t = sqrt(1-t^2)`.
- Gaussian conditional path:
  `p_{t|1}(x|x_1) = N(x | alpha_t x_1, sigma_t^2 I)`.
- Diffusion processes with affine drift coefficients can be written as Gaussian probability paths with `alpha_t` and `sigma_t` after time reparameterization.
- Under a Gaussian source, independent coupling, and score parameterization, the guide states probability-flow ODE sampling from a diffusion model is the same as sampling from a Flow Matching model with the corresponding Gaussian path.
- Stochastic interpolants provide a broader framework that connects deterministic probability-flow equations and stochastic differential equations.

Draft guardrails:

- The code-result figure compares the guide-listed Conditional OT and Linear VP schedules only.
- Do not claim the toy Linear VP schedule is a full diffusion sampler.
- Keep diffusion discussion to the verified connection through Gaussian paths, scores, and probability-flow ODEs.
