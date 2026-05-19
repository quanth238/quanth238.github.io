---
layout: distill
title: "Flow Matching Guide and Code, part 4"
description: "Compare endpoint couplings and inspect how pairing changes path geometry."
date: 2026-05-19
author: "Quan Tran Hong"
thumbnail: /assets/img/blog/flow-matching-guide/flow-matching-coupling-diagnostics.svg
tags: ["tutorial", "reading-notes", "generative-modeling"]
categories: ["tutorial"]
series: "flow-matching-guide"
part: 4
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
  - "https://arxiv.org/abs/2302.00482"
  - "https://arxiv.org/abs/2209.03003"
  - "https://arxiv.org/abs/2412.06264"
  - "https://dl.heeere.com/conditional-flow-matching/blog/conditional-flow-matching/"
  - "_blog_work/flow-matching-guide/remote_runs/20260519T153000Z_fm06_source_check/"
  - "_blog_work/flow-matching-guide/remote_runs/20260519T153215Z_fm06_coupling_diagnostics/"
---

## Introduction

Endpoint pairing is a modeling choice. The path formula can stay simple, while the coupling that chooses which source sample pairs with which data sample changes the training targets. Conditional Flow Matching makes this choice explicit: different couplings define different conditional paths, and the marginal field is learned by averaging those conditional velocities [Flow Matching Guide and Code](https://arxiv.org/abs/2412.06264).

OT-CFM studies this choice through optimal-transport-inspired couplings. The paper reports simpler flows and faster inference in its experiments, and it states the true-OT case as an approximation to dynamic OT [Improving and generalizing flow-based generative models with minibatch optimal transport](https://arxiv.org/abs/2302.00482). In code, the common lightweight version is a minibatch assignment. That assignment is useful, but it is only an optimization inside the current batch.

## Problem setup

Let $\pi(x_0,x_1)$ be the coupling between source and data endpoints. The independent coupling samples the two endpoints separately:

$$
X_0\sim p_0,
$$

$$
X_1\sim p_1.
$$

A transport-aware coupling tries to pair nearby or compatible endpoints more deliberately. Inside one minibatch, that often means solving an assignment problem over the batch cost matrix:

$$
C_{ij}=\|x_0^{(i)}-x_1^{(j)}\|_2^2.
$$

The result is a permutation of target samples for this batch. It is not the full-data OT plan; it is a finite-batch pairing rule.

## Path and velocity target

Once a pair is chosen, the straight conditional path is unchanged:

$$
X_t=(1-t)X_0+tX_1.
$$

The velocity target is also unchanged:

$$
U_t=X_1-X_0.
$$

The coupling changes which $X_1$ appears next to each $X_0$. That changes the segment lengths, the line crossings, and the distribution of velocity targets seen by the model.

## Training objective

With a coupling $\pi$, the conditional objective is

$$
\mathcal{L}_{\mathrm{CFM}}(\theta)=
\mathbb{E}_{t,(X_0,X_1)\sim\pi}
\left[\|v_\theta(X_t,t)-(X_1-X_0)\|_2^2\right].
$$

The loss shape is the same for independent pairing and minibatch assignment. The data distribution over endpoint pairs is different.

Rectified Flow gives a second reason to care about path geometry. It learns ODE models that follow straight paths between the two observed distributions as much as possible, and reports that increasingly straight paths can be simulated accurately with coarse time discretization [Flow Straight and Fast](https://arxiv.org/abs/2209.03003). That does not make minibatch OT and Rectified Flow the same algorithm. It gives a shared diagnostic: straighter, shorter, less tangled paths are easier for a coarse solver to follow.

## Minimal implementation

A batch-local assignment needs a cost matrix and an assignment solver. The important restriction is the scope: the optimizer sees only the current minibatch.

```python
import torch
from scipy.optimize import linear_sum_assignment


def minibatch_ot_pairs(x0: torch.Tensor, x1: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    cost = torch.cdist(x0, x1).pow(2)
    row, col = linear_sum_assignment(cost.detach().cpu().numpy())
    row = torch.as_tensor(row, device=x0.device)
    col = torch.as_tensor(col, device=x1.device)
    return x0[row], x1[col]


def straight_targets(x0: torch.Tensor, x1: torch.Tensor, t: torch.Tensor):
    xt = (1.0 - t[:, None]) * x0 + t[:, None] * x1
    velocity = x1 - x0
    return xt, velocity
```

This changes the pairing, not the regression formula. The same model still learns $v_\theta(x,t)$ from interpolated points and velocity targets.

## Code result

The diagnostic below uses the same source and target minibatch for both panels. The left panel shuffles endpoints independently. The right panel uses the minimum squared-distance assignment inside the displayed minibatch.

{% include figure.liquid path="/assets/img/blog/flow-matching-guide/flow-matching-coupling-diagnostics.svg" class="img-fluid rounded z-depth-1" width="1100" height="620" zoomable=true alt="Endpoint coupling comparison showing independent random pairing and minibatch optimal transport assignment on the same toy batch." %}

| Pairing rule | Mean squared endpoint cost | Segment crossings |
| --- | ---: | ---: |
| Independent random pairing | 7.430 | 16 |
| Minibatch OT assignment | 3.917 | 3 |

The batch assignment reduces this toy transport cost and removes many line crossings. That is a path-geometry result for the displayed batch. It does not say the learned model has solved the global OT problem.

## Sampling procedure

The sampler still integrates the learned marginal field. Coupling affects sampling indirectly by changing the conditional velocities used during training.

A tangled independent pairing can ask the model to explain many long crossing segments. A batch assignment often gives shorter targets, so the learned field may be easier to integrate with fewer solver steps. Rectified-flow work pushes this idea further by training toward straighter transports and studying coarse discretization.

The practical diagnostic is simple: after changing the coupling, inspect segment cost, path crossings, trajectory curvature, and solver-step sensitivity. If those improve together, the sampler has a cleaner field to follow. If only the batch cost improves, the change may be an optimization artifact.

## Next part

Part 5 changes the probability path itself and connects flow matching to diffusion-style paths.

## References and visual resources

- Conditional flow matching and minibatch OT: [Improving and generalizing flow-based generative models with minibatch optimal transport](https://arxiv.org/abs/2302.00482).
- Rectified paths and coarse solvers: [Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow](https://arxiv.org/abs/2209.03003).
- Primary guide and codebase paper: [Flow Matching Guide and Code](https://arxiv.org/abs/2412.06264).
- Visual reference: [A Visual Dive into Conditional Flow Matching](https://dl.heeere.com/conditional-flow-matching/blog/conditional-flow-matching/) uses pairing and path pictures that are useful for thinking about endpoint geometry.
