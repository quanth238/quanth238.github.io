# FM-08 Official Package Smoke Test

This run targets `flow_matching==1.0.10` in a temporary venv with system Torch. It imports `CondOTProbPath` and `ODESolver`, samples conditional OT path points, integrates the matching conditional velocity with `ODESolver.sample`, and writes a local SVG output.
