---
layout: distill
title: "Flow Matching Guide and Code, part 2"
description: "Build the ODE sampling loop and inspect how Euler step count changes a toy flow."
date: 2026-05-19
author: "Quan Tran Hong"
thumbnail: /assets/img/blog/flow-matching-guide/flow-matching-solver-steps.svg
tags: ["flow-matching", "tutorial", "reading-notes", "generative-modeling"]
categories: ["tutorial"]
series: "flow-matching-guide"
part: 2
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
  - "https://github.com/facebookresearch/flow_matching"
  - "_blog_work/flow-matching-guide/remote_runs/20260519T151120Z_fm04_solver_steps/"
---

## Introduction

Sampling is the moment where the trained velocity field becomes a generator. Start from fresh source noise, evaluate $v_\theta(x,t)$ at the current state, and take numerical ODE steps until $t=1$. The Flow Matching Guide and Code paper presents this as integrating the learned vector field after training [Flow Matching Guide and Code](https://arxiv.org/abs/2412.06264), and the original flow matching paper frames the same object as a continuous normalizing flow velocity field [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747).

The practical question is small but important: if the field is fixed, what does the solver actually do, and what changes when the step count changes?

## Problem setup

Assume the model already learned a time-dependent velocity field $v_\theta(x,t)$. Generation starts with a batch of source samples:

$$
x_0 \sim p_0.
$$

The sampler follows the ODE

$$
\frac{d x_t}{dt}=v_\theta(x_t,t).
$$

The exact endpoint would be

$$
x_1=x_0+\int_0^1 v_\theta(x_t,t)\,dt.
$$

That integral is not evaluated in closed form for a neural field. A solver approximates it by querying the model at a finite number of times.

## Path and velocity target

The straight conditional path from the first part gives the training target

$$
u_t=x_1-x_0.
$$

Sampling no longer has access to a paired data endpoint. The sampler only sees the current state $x_t$, the current time $t$, and the learned field $v_\theta(x_t,t)$. This distinction is useful: training constructs supervised velocity targets from endpoint pairs; sampling integrates the marginal field learned from those targets.

## Training objective

There is no new loss in the sampling loop. The same velocity regression objective trains the field:

$$
\mathcal{L}(\theta)=\mathbb{E}\left[\|v_\theta(x_t,t)-u_t\|_2^2\right].
$$

Once training is done, solver behavior is a numerical question. A coarse solver may follow the field with visible discretization error. A finer solver spends more evaluations to track the same field more closely. For this toy example, I use a 128-step Euler run as a reference and compare coarser Euler runs against it.

## Minimal implementation

The simplest sampler is explicit Euler. Divide $[0,1]$ into `steps` equal intervals, query the velocity field, and update the state:

$$
x_{t+\Delta t}=x_t+\Delta t\,v_\theta(x_t,t).
$$

```python
import torch


@torch.no_grad()
def euler_sample(model, x0: torch.Tensor, steps: int) -> torch.Tensor:
    x = x0
    dt = 1.0 / steps
    for i in range(steps):
        t = torch.full((x.shape[0],), i / steps, device=x.device)
        velocity = model(x, t)
        x = x + dt * velocity
    return x
```

The hand-written loop is the sampler used below. For orientation, [`flow_matching==1.0.10`](https://github.com/facebookresearch/flow_matching) exposes the same continuous-sampling idea through `flow_matching.solver.ODESolver`; Part 6 maps the toy pieces to the package API in detail. A minimal Euler call has the same ingredients: an initial batch, a velocity model, a method, and a time grid.

```python
import torch
from flow_matching.solver import ODESolver


solver = ODESolver(velocity_model=velocity_model)
samples = solver.sample(
    x_init=x0,
    step_size=1.0 / 32,
    method="euler",
    time_grid=torch.tensor([0.0, 1.0], device=x0.device),
)
```

For the step-count diagnostic here, the hand-written Euler loop is enough because it exposes each model evaluation and update directly.

## Code result

The figure uses one trained 2D toy field and the same initial noise samples for every panel. Only the number of Euler steps changes. Black dots are starts, blue curves are solver trajectories, teal dots are final samples, and the vermillion cloud is the target distribution.

{% include figure.liquid path="/assets/img/blog/flow-matching-guide/flow-matching-solver-steps.svg" class="img-fluid rounded z-depth-1" width="1180" height="760" zoomable=true alt="Euler solver step sweep showing 4, 8, 16, and 32 step trajectories for the same toy flow matching field." %}

The endpoint drift compares each coarse Euler endpoint to a 128-step Euler reference on the same initial samples.

| Euler steps | Mean reference drift | Mean nearest-mode distance |
| ----------: | -------------------: | -------------------------: |
|           4 |                0.239 |                      1.423 |
|           8 |                0.126 |                      1.476 |
|          16 |                0.062 |                      1.509 |
|          32 |                0.027 |                      1.527 |

The drift decreases as the step count increases because the coarse integrator is getting closer to the fine Euler reference for this fixed field. The nearest-mode distance does not monotonically improve here, which is a useful warning: a solver metric and a data-quality metric are not the same object.

## Sampling procedure

A practical sampling loop has four moving parts.

First, choose the initial distribution. In the toy code this is standard Gaussian noise in two dimensions. In larger models it is still usually an easy source distribution.

Second, choose the time grid. A uniform grid is the easiest first choice:

$$
t_i=\frac{i}{N}.
$$

Third, choose the numerical method. Euler is readable and cheap. Midpoint or higher-order solvers add extra velocity evaluations per step, which can reduce numerical error for the same grid length. Adaptive solvers such as `dopri5` choose internal steps based on error tolerances, so their `step_size` handling differs from fixed-step Euler-style loops.

Fourth, decide what diagnostic you trust. In a toy plot, reference drift checks numerical integration against a finer solver. It does not prove that the learned field matches the data distribution. Sample plots, target-distance summaries, and trajectory shape all answer different questions.

## Next part

Part 3 derives why endpoint-conditioned targets recover the marginal velocity used by the sampler.

## References and visual resources

- Primary guide and codebase paper: [Flow Matching Guide and Code](https://arxiv.org/abs/2412.06264).
- Core paper: [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747).
- Official package: [`facebookresearch/flow_matching`](https://github.com/facebookresearch/flow_matching).
- Visual reference: [A Visual Dive into Conditional Flow Matching](https://dl.heeere.com/conditional-flow-matching/blog/conditional-flow-matching/) uses probability-path diagrams that are helpful context for reading solver trajectories.
- Implementation-oriented walkthrough: [Flow Matching from Scratch](https://daddaops.com/blog/flow-matching-from-scratch/) gives a compact straight-line training loop before moving to sampling.
