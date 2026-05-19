---
layout: distill
title: "Flow Matching Guide and Code, part 3"
description: "Connect endpoint-conditioned velocity targets to the marginal field used at sampling time."
date: 2026-05-19
author: "Quan Tran Hong"
thumbnail: /assets/img/blog/flow-matching-guide/flow-matching-conditional-marginal-arrows.svg
tags: ["tutorial", "reading-notes", "generative-modeling"]
categories: ["tutorial"]
series: "flow-matching-guide"
part: 3
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
  - "https://arxiv.org/abs/2302.00482"
  - "https://www.weideng.org/posts/flow_matching/"
  - "https://dl.heeere.com/conditional-flow-matching/blog/conditional-flow-matching/"
  - "_blog_work/flow-matching-guide/remote_runs/20260519T152000Z_fm05_source_check/"
  - "_blog_work/flow-matching-guide/remote_runs/20260519T152215Z_fm05_conditional_marginal/"
---

## Introduction

The sampler in Part 2 never chooses a target endpoint. It starts from noise and follows $v_\theta(x,t)$. Training, however, used endpoint pairs. The Flow Matching Guide states the bridge directly: under the marginalization trick, conditional velocity fields can be averaged into a marginal velocity field that generates the marginal probability path [Flow Matching Guide and Code](https://arxiv.org/abs/2412.06264). The original paper gives the same construction for conditional probability paths and states that the Flow Matching and Conditional Flow Matching objectives have identical gradients [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747).

The useful way to read the result is local. Around one position and one time, many endpoint pairs may pass nearby. Each pair proposes a conditional velocity. The marginal field is the average direction that the sampler should use at that location.

```mermaid
flowchart LR
    accTitle: Conditional To Marginal Flow Matching Argument
    accDescr: The diagram separates the unavailable marginal flow matching loss from the tractable conditional flow matching loss and shows that population averaging recovers the marginal velocity used by sampling.

    endpoints["Sample endpoint pair"]
    path["Build conditional point Xt"]
    cond["Conditional velocity Ut"]
    cfm["Conditional FM loss"]
    avg["Average over pairs near (x,t)"]
    marginal["Marginal velocity ut(x)"]
    sampler["ODE sampler uses vtheta(x,t)"]
    ideal["Ideal FM loss"]

    endpoints --> path
    endpoints --> cond
    path --> cfm
    cond --> cfm
    cond --> avg
    avg --> marginal
    marginal --> ideal
    cfm --> sampler
    ideal --> sampler
```

## Problem setup

Let $Z$ denote the conditioning information used to create a training target. In the straight endpoint-pair version, $Z=(X_0,X_1)$. At a sampled time $t$, the conditional point is

$$
X_t=(1-t)X_0+tX_1.
$$

The endpoint-conditioned velocity is

$$
U_t=X_1-X_0.
$$

During training, the model sees $(X_t,t)$ and regresses toward $U_t$. During sampling, $Z$ is absent. A generated point has only its current state and time.

## Path and velocity target

The marginal field is the conditional average of the endpoint-conditioned velocity at the current location:

$$
u_t(x)=\mathbb{E}[U_t\mid X_t=x].
$$

For a more general conditioning variable $Z$, the guide writes the same idea as an average of conditional velocities:

$$
u_t(x)=\mathbb{E}[u_t(X_t|Z)\mid X_t=x].
$$

This is the field the sampler wants. It is not a single endpoint arrow. It is the average of all conditional arrows compatible with the same local state.

The guide's quick tour also gives a target-conditioned linear path. If the path is conditioned only on a data point $x_1$, the conditional velocity is

$$
u_t(x|x_1)=\frac{x_1-x}{1-t}.
$$

The paired-endpoint implementation uses the same averaging principle with $Z=(X_0,X_1)$ and the simple velocity $X_1-X_0$.

## Training objective

The ideal marginal Flow Matching loss would regress directly to $u_t(X_t)$:

$$
\mathcal{L}_{\mathrm{FM}}(\theta)=
\mathbb{E}\left[\|v_\theta(X_t,t)-u_t(X_t)\|_2^2\right].
$$

That target is usually unavailable because it already requires the local average over endpoint pairs. Conditional Flow Matching uses the tractable target:

$$
\mathcal{L}_{\mathrm{CFM}}(\theta)=
\mathbb{E}\left[\|v_\theta(X_t,t)-U_t\|_2^2\right].
$$

The theorem statement used here is the gradient equivalence:

$$
\nabla_\theta \mathcal{L}_{\mathrm{FM}}(\theta)=
\nabla_\theta \mathcal{L}_{\mathrm{CFM}}(\theta).
$$

Under the theorem assumptions, the population minimizer of the conditional objective is the marginal velocity. This is why endpoint-conditioned targets can train a field that later samples without a chosen endpoint.

## Minimal implementation

The code target is still the same regression loop. The only extra diagnostic is to inspect the average of conditional arrows near a location.

```python
import torch


def endpoint_batch(data: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    x1 = data
    x0 = torch.randn_like(x1)
    t = torch.rand(x1.shape[0], device=x1.device)
    xt = (1.0 - t[:, None]) * x0 + t[:, None] * x1
    target_velocity = x1 - x0
    return xt, t, target_velocity


def local_average_velocity(
    xt: torch.Tensor,
    target_velocity: torch.Tensor,
    query: torch.Tensor,
    radius: float,
) -> torch.Tensor:
    keep = torch.linalg.norm(xt - query[None, :], dim=1) <= radius
    return target_velocity[keep].mean(dim=0)
```

The first function is the training target. The second function is a diagnostic version of the marginalization idea: keep endpoint pairs whose interpolated point lies near the query and average their velocities.

## Code result

The local plot fixes $t=0.55$ and marks one query location. Gray arrows are endpoint-conditioned velocities from sampled pairs whose interpolated points land near the query. The teal arrow is their empirical average.

{% include figure.liquid path="/assets/img/blog/flow-matching-guide/flow-matching-conditional-marginal-arrows.svg" class="img-fluid rounded z-depth-1" width="920" height="640" zoomable=true alt="Conditional endpoint velocity arrows near one query point averaged into a local marginal direction." %}

The run sampled 5,000 endpoint pairs and kept the 26 nearest interpolated points around the query. The local average velocity was approximately $(-0.126, 0.131)$. The exact number is not the point; the useful object is the distinction between many conditional arrows and one marginal direction.

## Sampling procedure

Sampling uses the learned approximation to the marginal field:

$$
\frac{dX_t}{dt}=v_\theta(X_t,t).
$$

No target endpoint is sampled during generation. The endpoint construction lives in the training objective, where it supplies cheap supervised velocity targets. At population scale, the conditional objective pushes the model toward the same marginal velocity field that the ODE sampler needs.

This also explains why Part 2 could integrate a field without carrying endpoint labels. The solver does not know which data point a generated sample will approach. It only evaluates a learned average direction at the current location and time.

## Next part

Part 4 changes the endpoint coupling and measures how pairing alters path geometry.

## References and visual resources

- Primary guide and codebase paper: [Flow Matching Guide and Code](https://arxiv.org/abs/2412.06264).
- Core paper: [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747).
- Conditional flow matching and minibatch OT: [Improving and Generalizing Flow-Based Generative Models with Minibatch Optimal Transport](https://arxiv.org/abs/2302.00482).
- Visual reference: [A Visual Dive into Conditional Flow Matching](https://dl.heeere.com/conditional-flow-matching/blog/conditional-flow-matching/) uses path and velocity diagrams that help separate conditional and marginal objects.
- Compact technical reference: [Flow Matching: A Minimal Guide](https://www.weideng.org/posts/flow_matching/) gives a concise conditional-expectation view of the training target.
