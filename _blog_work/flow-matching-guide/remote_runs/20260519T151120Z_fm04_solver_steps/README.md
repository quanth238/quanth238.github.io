# FM-04 Solver Step Sweep

Deterministic pure-Python run for Flow Matching Part 2. The script trains a small linear velocity field on the two-cluster toy distribution, then integrates the same initial samples with 4, 8, 16, and 32 explicit Euler steps. Metrics compare each endpoint to a 128-step Euler reference on the same starts. The SVG marks the reference endpoints with purple rings and the coarse-to-reference endpoint residuals with orange segments so the solver-step effect is visible at page scale.
