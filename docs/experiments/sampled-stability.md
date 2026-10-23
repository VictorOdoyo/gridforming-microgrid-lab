# Sampled-loop stability and transport delay

The converter analysis includes four LC plant states and the real and imaginary
integrators of both PI loops. Additional command-delay states shift one complete
voltage command per tick. Physical plant propagation uses an exact zero-order-hold
matrix exponential; controller updates match the implemented sampled PI laws.

Local differentiation produces the full discrete transition matrix. Its spectral
radius must be below one for local sampled stability. The default 50 microsecond
control period is stable in this model; a 500 microsecond period is unstable.

Stability is not necessarily monotonic in sample period. Aliasing can create
apparent sampled stability bands; examine intersample behavior and physical
bandwidth, not just a single pole-radius result. Saturation and large disturbances
require separate nonlinear tests. The delay map is a local unsaturated analysis.

An independent regression compares RK4 physical LC trajectories against an exact
linear state-space solution at identical inputs and times.
