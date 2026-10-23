# Energy-coupled physical models

The SI laboratory complements the balanced phasor network solver. It represents
one battery-fed inverter with an averaged DC/DC stage, DC capacitor, averaged
three-phase bridge, LC filter and passive AC conductance. Optional droop/VSM
states drive the AC voltage-reference angle. It is not a multi-bus EMT solver.

## State and units

The nine physical states are:

| Index | State | Unit |
| --- | --- | --- |
| 0 | Battery SOC | fraction |
| 1 | Battery polarization voltage | V |
| 2 | DC converter inductor current | A |
| 3 | DC capacitor stored energy | J |
| 4 | Lumped pack/converter temperature | Celsius |
| 5, 6 | AC inductor d, q current | peak A |
| 7, 8 | AC capacitor d, q voltage | peak V |

Grid-forming cases add angle in radians, frequency deviation in Hz, filtered
load power in system pu, and a secondary frequency bias in Hz.

Amplitude-invariant dq power is P = 1.5 Re(v conjugate(i)). A balanced dq voltage
magnitude of 325 V corresponds to 398.04 V line-to-line RMS. Current phase RMS is
the dq current magnitude divided by sqrt(2). RMS phasor conventions in the
network solver differ; values are not interchangeable without conversion.

## Battery and DC/DC stage

OCV is piecewise linear in SOC. Series resistance has an illustrative exponential
temperature coefficient. A parallel RC polarization branch stores electrical
energy and dissipates heat. Positive current discharges the pack.

    Vterminal = Voc(SOC) - Vpolarization - R0(T) I
    dSOC/dt = -I / (capacity_Ah * 3600)
    dVpolarization/dt = (I - Vpolarization/R1) / C1
    Ldc dI/dt = Vterminal - duty Vdc - Rdc I
    Pin_to_link = duty I Vdc
    dUdc/dt = Pin_to_link + Psolar - Pinverter_dc
    Vdc = sqrt(2 Udc / Cdc)

The coupled physical energy model uses unit coulomb efficiency. The separate
energy-dispatch model includes empirical charge/discharge efficiency. Combining
those losses without an explicit energy sink would double-count dissipation.

When contactors open, battery current becomes zero and inductor current decays
through a modeled dump resistor. Inductor energy remains continuous.

## AC LC dynamics

The dq frame rotates at the configured nominal electrical angular velocity:

    Lac di/dt = u - v - Rac i - j omega Lac i
    Cac dv/dt = i - Gload v - j omega Cac v

The bridge command is limited to Vdc/sqrt(3) peak magnitude, including during
intermediate plant integration evaluations. DC demand equals instantaneous
three-phase AC input plus nonnegative modeled semiconductor losses.

Two sampled PI loops regulate AC voltage and inductor current. Load-current and
frame-coupling feedforward are explicit. Both loops use vector saturation and
tracking anti-windup. The DC outer voltage PI and inner current PI control the
bidirectional converter separately.

## Grid-forming frequency control

Outer droop/VSM equations use measured AC load power on the declared common
power base. They rotate the physical dq voltage reference; the resulting voltage
and current states determine actual inverter DC demand. Virtual inertia is a
control state, not a physical energy source.

The optional secondary integrator restores the oscillator frequency. Gate blocking
freezes the outer states. This isolated-inverter laboratory has no utility tie;
checked multi-source utility reconnection remains a phasor-network experiment.

## Independent energy evidence

Chemical energy is the exact integral of the tabulated OCV against stored charge.
Stored electrical energy includes DC capacitor, DC inductor, polarization capacitor,
AC inductor and AC capacitor energy.

    chemical_draw + solar_input
        = delivered_load + generated_heat + electrical_storage_change

The audit computes storage from saved states, not from the ODE's derivatives.
Held source powers use interval integration. State-dependent loss and load powers
use endpoint quadrature. Residuals should decrease as plant integration is refined.

Generated heat is an electrical loss. The thermal state separately stores and
removes that heat. Do not add both total generated heat and thermal storage change
to the same electrical balance.

## Sampling and evidence limits

Controllers and supervisors advance at accepted ticks. Signals and events insert
exact boundaries. Internal plant substeps can resolve fast LC decay while holding
controller output constant. A stable plant integrator does not imply stable
sampled control; the discrete pole/delay study addresses that separate question.

There are no switching-device transients, validated cell-aging laws, electrochemical
diffusion PDEs or certified relay models. Carrier/PWM and dead-time utilities are
separate waveform experiments. Parameters are illustrative rather than identified
from a commercial inverter or cell pack.
