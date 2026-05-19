# FM-08 Official Package Verification

Verification date: `2026-05-19`

Install/run environment:

- Temporary venv: `/tmp/fm08-flow-matching-venv`
- Install command: `python -m pip install flow_matching`
- Installed package: `flow_matching==1.0.10`
- Torch: `2.8.0`

Verified imports:

- `flow_matching.path.AffineProbPath`
- `flow_matching.path.CondOTProbPath`
- `flow_matching.path.scheduler.CondOTScheduler`
- `flow_matching.path.scheduler.LinearVPScheduler`
- `flow_matching.path.scheduler.VPScheduler`
- `flow_matching.path.scheduler.ScheduleTransformedModel`
- `flow_matching.solver.ODESolver`
- `flow_matching.loss.MixturePathGeneralizedKL`

API note:

- The installed PyPI package exports `CondOTProbPath`, not `CondOTPath`.
- Part 6 must use `CondOTProbPath` or `AffineProbPath(scheduler=CondOTScheduler())`.

Smoke test:

- Script: `scripts/blog_pipeline/examples/flow_matching_official_package_bridge.py`
- Run metadata: `_blog_work/flow-matching-guide/remote_runs/20260519T155000Z_fm08_official_package/official_package_smoke_test.json`
- Local output: `assets/img/blog/flow-matching-guide/flow-matching-official-package-bridge.svg`

Draft guardrail:

- Treat the output as an official-package component smoke test. It verifies path and solver APIs; it is not a trained generative model.

FM-15 review correction:

- Rerun environment: `/tmp/fm15-flow-matching-venv`
- Additional package needed by the solver import: `tqdm`
- Rerun command: `/tmp/fm15-flow-matching-venv/bin/python scripts/blog_pipeline/examples/flow_matching_official_package_bridge.py --run-dir _blog_work/flow-matching-guide/remote_runs/20260519T155000Z_fm08_official_package`
- The corrected metric compares the final solver state with the exact `CondOTProbPath` sample at the same final time, `t=0.98`.
- Remaining distance from the `t=0.98` path point to `x_1` is recorded separately and is not treated as solver error.
