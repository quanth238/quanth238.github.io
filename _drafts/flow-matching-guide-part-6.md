---
layout: distill
title: "Flow Matching Guide and Code, part 6"
description: "Map the toy flow-matching pieces to the verified official package components."
date: 2026-05-19
author: "Quan Tran Hong"
thumbnail: /assets/img/blog/flow-matching-guide/flow-matching-official-package-bridge.svg
tags: ["tutorial", "reading-notes", "generative-modeling"]
categories: ["tutorial"]
series: "flow-matching-guide"
part: 6
draft_stage: "draft"
publish_ready: false
mermaid:
  enabled: true
  zoomable: true
chart:
  plotly: false
  vega_lite: false
visual_plan: "_blog_work/flow-matching-guide/visual_sources.yml"
source_materials:
  - "https://arxiv.org/abs/2412.06264"
  - "https://github.com/facebookresearch/flow_matching"
  - "https://arxiv.org/abs/2210.02747"
  - "_blog_work/flow-matching-guide/remote_runs/20260519T155000Z_fm08_official_package/"
---

## Introduction

The toy code has four moving parts: a probability path, a velocity target, a velocity model, and an ODE sampler. The official [`flow_matching`](https://github.com/facebookresearch/flow_matching) package keeps the same separation. The repository describes a PyTorch library for continuous and discrete flow matching implementations, with path, scheduler, solver, loss, and example modules tied to the Flow Matching Guide and Code paper [Flow Matching Guide and Code](https://arxiv.org/abs/2412.06264).

I verified the package install and component names with `flow_matching==1.0.10`. The installed package exports `CondOTProbPath`, `AffineProbPath`, scheduler classes such as `CondOTScheduler` and `LinearVPScheduler`, and `ODESolver` for continuous sampling.

```mermaid
flowchart LR
    accTitle: Toy Flow Matching To Official Package Components
    accDescr: The diagram maps the tutorial's toy path, scheduler, velocity target, model, and solver concepts to verified components in the official flow_matching package.

    toy_path["Toy path xt"]
    toy_velocity["Toy target Ut"]
    toy_model["Velocity model vtheta"]
    toy_loss["MSE velocity loss"]
    toy_solver["Euler or midpoint loop"]

    pkg_path["CondOTProbPath or AffineProbPath"]
    pkg_scheduler["CondOTScheduler or LinearVPScheduler"]
    pkg_sample["PathSample: x_t and dx_t"]
    pkg_model["Callable or ModelWrapper"]
    pkg_solver["ODESolver.sample"]

    toy_path --> pkg_path
    pkg_scheduler --> pkg_path
    pkg_path --> pkg_sample
    toy_velocity --> pkg_sample
    toy_model --> pkg_model
    toy_loss --> pkg_sample
    toy_solver --> pkg_solver
    pkg_model --> pkg_solver
```

## Problem setup

The package does not remove the conceptual work. It gives names and tested APIs for the same objects:

| Tutorial object | Verified package object |
| --- | --- |
| Conditional OT path | `CondOTProbPath` |
| General affine path | `AffineProbPath` |
| Conditional OT scheduler | `CondOTScheduler` |
| Linear VP scheduler | `LinearVPScheduler` |
| Continuous ODE sampler | `ODESolver` |
| Model wrapper option | `ModelWrapper` |
| Discrete generalized KL loss | `MixturePathGeneralizedKL` |

For the continuous path used in this series, the path object returns a `PathSample` with `x_t` and `dx_t`. The training loop can then use a standard PyTorch regression loss between the model output and `dx_t`.

## Path and velocity target

The package path object owns the schedule and target construction. For Conditional OT:

```python
import torch
from flow_matching.path import CondOTProbPath


path = CondOTProbPath()
x0 = torch.randn(batch_size, 2)
x1 = data_batch
t = torch.rand(batch_size)

sample = path.sample(x0, x1, t)
xt = sample.x_t
velocity_target = sample.dx_t
```

For a custom affine schedule, use `AffineProbPath` with a scheduler:

```python
from flow_matching.path import AffineProbPath
from flow_matching.path.scheduler import LinearVPScheduler


path = AffineProbPath(scheduler=LinearVPScheduler())
sample = path.sample(x0, x1, t)
```

That mapping is the package version of the equations from Part 5.

## Training objective

The continuous training objective remains velocity regression:

$$
\mathcal{L}(\theta)=
\mathbb{E}\left[\|v_\theta(X_t,t)-\dot{X}_t\|_2^2\right].
$$

In code, `sample.dx_t` is the target:

```python
pred = velocity_model(sample.x_t, sample.t)
loss = torch.mean((pred - sample.dx_t) ** 2)
```

The package also has discrete-flow components. In the installed version, `MixtureDiscreteProbPath`, `MixtureDiscreteEulerSolver`, and `MixturePathGeneralizedKL` are exported for discrete settings. That belongs to a different branch of the library than the continuous 2D examples used here.

## Minimal implementation

The verified continuous solver API is `ODESolver.sample`. It accepts `x_init`, `step_size`, `method`, `time_grid`, and `return_intermediates`.

```python
import torch
from flow_matching.solver import ODESolver


solver = ODESolver(velocity_model=velocity_model)
time_grid = torch.linspace(0.0, 1.0, 32)

samples = solver.sample(
    x_init=x0,
    step_size=1.0 / 32,
    method="midpoint",
    time_grid=time_grid,
    return_intermediates=False,
)
```

The velocity model can be a callable or a `ModelWrapper`. Extra keyword arguments passed to `sample` are forwarded to the velocity model, which is useful for conditional checks and guided settings.

## Code result

The verified package run uses `CondOTProbPath` to sample exact conditional path points, then uses `ODESolver` with the matching conditional velocity to integrate the same endpoints up to $t=0.98$. Dotted gray curves are path-object samples. Solid blue curves are solver trajectories.

{% include figure.liquid path="/assets/img/blog/flow-matching-guide/flow-matching-official-package-bridge.svg" class="img-fluid rounded z-depth-1" width="980" height="620" zoomable=true alt="Official flow_matching package smoke test using CondOTProbPath and ODESolver on conditional endpoint trajectories." %}

The mean endpoint error at $t=0.98$ was 0.0524 in the 2D check. The point of the run is API wiring: the path object, velocity callable, and solver agree on tensor shapes and time arguments.

## Sampling procedure

For a trained continuous model, the package sampling pattern is direct:

1. choose the source batch `x_init`;
2. wrap or pass the velocity model;
3. choose `time_grid`, `method`, and `step_size`;
4. call `ODESolver.sample`.

The conceptual checks from the earlier parts still apply. The solver method should match the field's time behavior, the path scheduler should match training, and diagnostics should separate numerical integration error from model quality.

## Next part

The series ends with an export checklist after all draft checks pass.

## References and visual resources

- Primary guide and codebase paper: [Flow Matching Guide and Code](https://arxiv.org/abs/2412.06264).
- Official package repository: [`facebookresearch/flow_matching`](https://github.com/facebookresearch/flow_matching).
- Core paper: [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747).
- Package verification metadata: `_blog_work/flow-matching-guide/remote_runs/20260519T155000Z_fm08_official_package/package_verification.md`.
