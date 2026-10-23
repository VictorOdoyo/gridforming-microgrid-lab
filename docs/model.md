# Model equations and conventions

## Bases and signs

The system base is total three-phase apparent power Sbase, line-to-line RMS
voltage Vbase, and nominal frequency f0. Ibase = Sbase/(sqrt(3) Vbase) and
Zbase = Vbase²/Sbase. Every source uses the same system base. A source rating
is metadata for normalization; gains must already be converted to this base.

Balanced per-unit terminal power is S = V conjugate(I). Positive P and Q denote
source injection; positive load P and Q denote consumption. Internal source EMF
and bus voltage are fundamental-frequency RMS phasors in a frame rotating at f0.
Network and control equations do not synthesize phase waveforms.

## Algebraic network

Each source injects I_k = (E_k exp(j theta_k) - V_bus)/Z_k.
Its Norton admittance contributes 1/Z_k to the source bus diagonal, and its EMF
contributes E_k exp(j theta_k)/Z_k to the current-injection vector.

The system solves Y_total V = J at every derivative evaluation. Passive lines
use a pi model; load admittance is conjugate(S_nominal), so actual demand is
S_nominal |V|². Changing a load scale changes admittance, rather than prescribing
voltage-independent power. Branch losses and source-impedance losses are separate.

The nonlinear limiting variant radially clips each source current and solves
nodal KCL again. It is an algebraic approximation, with no switching dynamics
or detailed current-loop recovery. Unlimited sources follow the linear solution.

## Source states

Each inverter stores [theta, df, E, Pf, Qf]. Angles are relative to the nominal
rotating frame, df is in Hz, E is pu RMS voltage, and filtered powers are system pu.
Droop mode reserves df as an inactive state; its reported frequency is algebraic.

Power measurements follow dPf/dt = (P-Pf)/tau_p and dQf/dt = (Q-Qf)/tau_p.

Droop frequency is df = mp (Pref-Pf) + secondary + sync, where mp has units Hz/pu.
Angle dynamics are dtheta/dt = 2 pi df.

VSM frequency follows:

    (2 H / f0) ddf/dt = Pref - Pf - (df - secondary - sync)/mp

H is in seconds. This reduced swing model includes droop-equivalent damping.
It does not reproduce every virtual synchronous machine implementation.

Voltage dynamics are:

    tau_v dE/dt = ramp(t) [Vref - nq (Qf-Qref)] - E

The black-start ramp rises from zero to one over startup_s. There are no explicit
inner voltage/current regulators in this phasor model. RL and LCL models in the
package are independent SI component experiments.

## Secondary control and synchronization

A shared secondary bias integrates the negative mean enabled-source frequency
deviation. When island synchronization is enabled, its bias is subtracted from
the secondary observation to prevent the two loops canceling one another.
The secondary output is bounded with conditional anti-windup.

The optional utility is a fixed-voltage Thevenin source in the nominal frame.
Phase alignment uses the shortest wrapped phase error, with a bounded frequency
bias. Reconnection requires angle, frequency, RMS magnitude, and energized-bus
criteria. Frequency checks use the enabled-source mean internal frequency.

## Solver and events

SciPy solve_ivp integrates each continuous segment. Event times partition the
integration horizon; source state remains continuous while algebraic quantities
are recomputed with the new configuration. Samples at event times describe the
post-event network. Simultaneous events execute in input order.

Current, terminal power, source status, bus voltage, and KCL residual are recorded.
Reported source frequency is the control oscillator frequency. It need not equal
the instantaneous derivative of bus-voltage phase during a network transient.
