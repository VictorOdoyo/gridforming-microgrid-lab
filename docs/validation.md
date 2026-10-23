# Verification and evidence

The tests verify mathematical implementations and selected reduced-model behavior.
They do not establish hardware compliance or experimental model accuracy.

| Layer | Independent reference or invariant |
| --- | --- |
| Per-unit bases | Three-phase VA and line-current identity |
| Clarke/Park transforms | A balanced sinusoid maps to constant d-axis amplitude |
| Passive network | Two-bus voltage divider and zero row sums |
| Branch accounting | Complex power balance and I²R copper loss |
| Transformer | Open-circuit complex tap ratio and passive real loss |
| AC load flow | High-voltage root of the resistive two-bus quadratic |
| ZIP load flow | Constant-power quadratic operating point |
| Current saturation | Resistive-load voltage equals limited current divided by conductance |
| Battery | Stored energy, asymmetric efficiency and reserve boundaries |
| DC link | Capacitor energy increment equals integrated input/output power |
| RL/LCL filters | Steady impedance and lossless energy derivative |
| PI and relays | Saturation recovery, continuous pickup, latched trip |
| Droop/VSM | Equilibrium relation and initial swing-equation RoCoF |
| Dynamic network | KCL residual at every output sample |
| Symmetric sharing | Identical sources have identical complex injection |
| Relative VSM modes | Stable default and deliberately unstable slow filter |
| Perturbation response | One-source angle perturbation decays at stable tuning |
| Island reconnection | Unsafe phase mismatch is rejected |
| Numerical integration | Tight-step reference on matching event/sample times |
| Serialization | Exact array round trip and report checksums |

## How to reproduce

Install development dependencies and run:

```sh
python -m pytest -q
gridlab stability --mode vsm
gridlab study stability-map --output outputs/stability-map.json
gridlab study convergence --output outputs/convergence.json
```

The convergence study uses the same numerical model with tighter integration
settings. It verifies numerical consistency, not agreement with field measurements.

## Interpreting metrics

Frequency nadir is the minimum over connected source oscillator samples.
RoCoF uses first differences at the saved sample interval; finer sampling can
change the measured maximum. Report the sample interval when comparing results.
No difference is taken across disconnected source intervals.

Voltage-band duration is a trapezoidal estimate from saved in/out-of-band samples.
Energy integration uses trapezoidal integration for continuous saved powers.
Daily dispatch instead treats each reported power as held over its interval.

Disconnected sources have zero injection and frozen controller states. Their
internal frequency is excluded from trace-level summary statistics and figures.

## Known evidence boundaries

No comparison to an independent EMT package or physical inverter has been made.
Source ratings do not automatically impose thermal, SOC, or DC-power constraints
on the phasor solver. Those component and energy experiments are separate.
Changing numerical tolerances cannot resolve missing physical dynamics.
