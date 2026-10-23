# Physical-model verification

| Capability | Evidence |
| --- | --- |
| Battery terminal power | Stable quadratic root and chemical/terminal/copper power identity |
| Chemical capacity | Exact piecewise-linear OCV integral |
| Polarization | RC storage plus resistor dissipation equals polarization power |
| Bidirectional DC/DC | Battery input minus bus output equals L energy rate plus copper loss |
| DC bus hold-up | Analytical capacitor brownout time |
| Coupled DC plant | Instantaneous electrical storage identity in closed/open-contactor modes |
| Regeneration | Negative chemical draw, increasing SOC, positive losses |
| Full battery-to-AC path | Independent saved-state electrical energy audit |
| LC dq plant | Three-phase instantaneous power balance |
| LC integration | Exact state-space exponential against RK4 trajectory |
| LC passivity | Physical storage matrix gives the expected resistor/load dissipation |
| LQR | Riccati residual and stable feedback poles |
| Sampled PI cascade | Exact ZOH plant plus implemented digital PI integrators |
| Transport delay | Explicit command queue states in sampled stability map |
| Kalman observer | Seeded noisy voltage-only experiment and PSD covariance |
| LCL active damping | Oscillatory eigenvalues move left under capacitor-current feedback |
| ADC | Half-LSB reconstruction error and endpoint clipping |
| SVPWM | Reconstruction across all six vector sectors |
| Carrier switching | Duty average and floating-neutral phase-voltage sum |
| Dead time | Polarity reversal and compensation identity |
| BMS/gating | Hysteresis, latching, continuous healthy dwell and explicit rearm |
| Case storage | Physical initial-state, nested model and event round trips |
| Reports | File checksums and original typed trace data |

Run all checks with `uv run python -m pytest -q`. The physical tests complement,
rather than replace, the original network/phasor validation in validation.md.

The full hybrid audit includes the observed DC cap voltage in the AC modulation
ceiling. Solar injection is included as external input. Copper and empirical
inverter losses are accounted for separately. VSM virtual inertia is not counted
as stored electrical energy.

Numerical integration convergence, analytical consistency and agreement with
measured hardware are different forms of evidence. This project currently
provides the first two. No physical inverter or commercial EMT cross-validation
has been performed.

Default sample intervals, empirical resistance/thermal parameters, protection
thresholds and illustrative pack capacity must be reported with results.
Changing them can change both stability and recoverability.
