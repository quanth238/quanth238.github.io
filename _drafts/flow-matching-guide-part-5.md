---
layout: distill
title: "Flow Matching: Path Design"
description: "Compare two path schedules."
date: 2026-05-19
author: "Quan Tran Hong"
thumbnail: /assets/img/blog/flow-matching-guide/flow-matching-card-part-5.svg
tags: ["flow-matching", "tutorial", "reading-notes", "generative-modeling"]
categories: ["tutorial"]
series: "flow-matching-guide"
part: 5
draft_stage: "draft"
publish_ready: false
hide_footer: true
toc:
  - name: "Introduction"
  - name: "Problem setup"
  - name: "Path and velocity target"
  - name: "Training objective"
  - name: "Minimal implementation"
  - name: "Code result"
  - name: "Sampling procedure"
  - name: "Next part"
  - name: "References and visual resources"
mermaid:
  enabled: true
  zoomable: true
chart:
  plotly: false
  vega_lite: false
visual_plan: "_blog_work/flow-matching-guide/visual_sources.yml"
source_materials:
  - "https://arxiv.org/abs/2412.06264"
  - "https://arxiv.org/abs/2210.02747"
  - "https://arxiv.org/abs/2303.08797"
  - "https://dl.heeere.com/conditional-flow-matching/blog/conditional-flow-matching/"
  - "_blog_work/flow-matching-guide/remote_runs/20260519T154000Z_fm07_source_check/"
  - "_blog_work/flow-matching-guide/remote_runs/20260519T154210Z_fm07_path_families/"
---

## Introduction

The endpoint coupling chooses which samples are paired. The probability path chooses how each pair moves through time. Flow Matching Guide and Code frames this as a scheduler choice inside affine conditional flows: choose $\alpha_t$ and $\sigma_t$, then form a path between source and data [Flow Matching Guide and Code](https://arxiv.org/abs/2412.06264).

This is also where the diffusion connection becomes concrete. Gaussian paths with schedules $\alpha_t$ and $\sigma_t$ include flow-matching paths and diffusion-style probability paths. With a Gaussian source, independent coupling, and score parameterization, the guide connects diffusion probability-flow ODE sampling to flow matching with the corresponding Gaussian path. Stochastic interpolants give an even broader view that includes deterministic probability-flow equations and stochastic differential equations [Stochastic Interpolants](https://arxiv.org/abs/2303.08797).

## Problem setup

Keep the same endpoint pair $(X_0,X_1)$. Instead of always using the straight interpolation, define an affine path:

$$
X_t=\alpha_t X_1+\sigma_t X_0.
$$

The scheduler satisfies the endpoint conditions

$$
\alpha_0=0,
$$

$$
\alpha_1=1,
$$

$$
\sigma_0=1,
$$

$$
\sigma_1=0.
$$

The guide lists several schedulers. I will compare two:

| Schedule       | $\alpha_t$ | $\sigma_t$     |
| -------------- | ---------- | -------------- |
| Conditional OT | $t$        | $1-t$          |
| Linear VP      | $t$        | $\sqrt{1-t^2}$ |

The second schedule keeps more source noise at middle times. That changes both what the model sees and the scale of the target velocity.

## Path and velocity target

Different schedulers imply different conditional velocity targets. Differentiate the affine path:

$$
U_t=\dot{\alpha}_t X_1+\dot{\sigma}_t X_0.
$$

For Conditional OT,

$$
\alpha_t=t,
$$

$$
\sigma_t=1-t.
$$

The target is

$$
U_t=X_1-X_0.
$$

For Linear VP,

$$
\alpha_t=t,
$$

$$
\sigma_t=\sqrt{1-t^2}.
$$

The derivative gives

$$
U_t=X_1-\frac{t}{\sqrt{1-t^2}}X_0.
$$

The late-time velocity can become large because $\sigma_t=\sqrt{1-t^2}$ goes to zero as $t$ approaches 1, so the factor $t/\sigma_t$ is singular at the endpoint. That is a schedule effect, not a model architecture effect. In the toy comparison below, the reported times stay below 1, and the code uses a small epsilon guard when evaluating the schedule near the endpoint.

## Training objective

The loss still regresses the model toward the path velocity:

$$
\mathcal{L}(\theta)=
\mathbb{E}\left[\|v_\theta(X_t,t)-U_t\|_2^2\right].
$$

Changing the path changes the distribution of $X_t$ and the target $U_t$. The same network and optimizer can face a different regression problem.

Gaussian paths also explain the diffusion connection. The guide writes Gaussian conditional paths as

$$
p_{t|1}(x|x_1)=
\mathcal{N}(x\mid \alpha_t x_1,\sigma_t^2 I).
$$

Diffusion forward processes with affine drift coefficients can be expressed as Gaussian probability paths after time reparameterization. With the right score parameterization, the probability-flow ODE is another way to sample the same marginal path.

## Minimal implementation

The path family fits into one small scheduler object.

```python
import torch


def cond_ot_schedule(t: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    return t, 1.0 - t


def linear_vp_schedule(t: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    return t, torch.sqrt(torch.clamp(1.0 - t**2, min=1e-6))


def affine_path(x0: torch.Tensor, x1: torch.Tensor, t: torch.Tensor, schedule):
    alpha, sigma = schedule(t)
    xt = alpha[:, None] * x1 + sigma[:, None] * x0
    return xt
```

For training, the schedule also needs $\dot{\alpha}_t$ and $\dot{\sigma}_t$ so the velocity target matches the sampled path.

```python
def linear_vp_velocity(x0: torch.Tensor, x1: torch.Tensor, t: torch.Tensor):
    sigma = torch.sqrt(torch.clamp(1.0 - t**2, min=1e-6))
    return x1 - (t / sigma)[:, None] * x0
```

The clamp is the epsilon guard for the Linear VP endpoint. It keeps the toy computation finite if a sampled or plotted time gets too close to $t=1$; the comparison table evaluates times below the endpoint.

## Code result

The figure uses the same endpoint pairs and the same x-y axes for both rows. The top row uses Conditional OT. The bottom row uses the guide-listed Linear VP schedule.

{% include figure.liquid path="/assets/img/blog/flow-matching-guide/flow-matching-path-family-snapshots.svg" class="img-fluid rounded z-depth-1" width="1180" height="760" zoomable=true alt="Probability path snapshots comparing Conditional OT and Linear VP schedules on the same toy endpoint pairs and shared x-y axes." %}

The middle-time snapshots differ because the schedules mix source and data with different weights. Conditional OT moves mass linearly toward the target. Linear VP keeps a wider source-noise component for longer, then pays for that with larger late-time velocity magnitudes.

| Schedule                     | $t=0.00$ | $t=0.33$ | $t=0.66$ | $t=0.90$ |
| ---------------------------- | -------: | -------: | -------: | -------: |
| Conditional OT mean velocity |     2.50 |     2.50 |     2.50 |     2.50 |
| Linear VP mean velocity      |     2.29 |     2.31 |     2.45 |     3.35 |

The numbers are conditional target magnitudes for the toy draw. They are useful because they show what the loss is asking the model to fit at each time.

## Sampling procedure

The sampler must use a field trained for the chosen path. If the model was trained with Conditional OT targets, its velocity scale and time behavior match that path. If it was trained with a Gaussian or diffusion-like schedule, the solver queries a field with a different time profile.

This is why path choice is not just a notation change. It changes intermediate distributions, loss weighting over time, target magnitude, and sometimes the best solver schedule. The diffusion link is the same idea in a broader form: choose a Gaussian probability path, train a score or velocity parameterization for that path, then sample with an ODE or SDE that follows the same marginals.

## Next part

Part 6 maps the toy pieces to the official `flow_matching` package.

## References and visual resources

- Primary guide and codebase paper: [Flow Matching Guide and Code](https://arxiv.org/abs/2412.06264).
- Core paper: [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747).
- Related interpolant view: [Stochastic Interpolants: A Unifying Framework for Flows and Diffusions](https://arxiv.org/abs/2303.08797).
- Visual reference: [A Visual Dive into Conditional Flow Matching](https://dl.heeere.com/conditional-flow-matching/blog/conditional-flow-matching/) uses probability-path pictures that are helpful for reading scheduler changes.
