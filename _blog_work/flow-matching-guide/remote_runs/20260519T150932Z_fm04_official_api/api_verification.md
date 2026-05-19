# FM-04 Official Solver API Verification

- Source: `https://github.com/facebookresearch/flow_matching`
- Checked commit: `11568d37f8d5a080e12aa7b5305d9c35ae07d136`
- Verification date: `2026-05-19`

Relevant source files inspected:

- `flow_matching/solver/ode_solver.py`
- `flow_matching/solver/__init__.py`
- `tests/solver/test_ode_solver.py`
- `examples/2d_flow_matching.ipynb`

Verified names used in Part 2:

- Continuous solver class: `flow_matching.solver.ODESolver`
- Constructor argument: `velocity_model`
- Sampling method: `ODESolver.sample(...)`
- Sampling arguments used in the draft: `x_init`, `step_size`, `method`, `time_grid`, `return_intermediates`
- Fixed/adaptive method names observed in source/tests: `"euler"`, `"midpoint"`, `"heun3"`, `"dopri5"`

Draft guardrail:

- Part 2 only uses these names as a current package vocabulary check and keeps the solver-step result toy-scoped.
