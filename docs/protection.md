# Protection and failure semantics

These supervisors exercise engineering logic in simulations. They do not provide
certified protection settings or replace a device-specific fault study.

## Battery contactor

BMS checks SOC and pack temperature. A trip latches until explicit reset and a
healthy hysteresis band. Soft current derating operates inside the hard trip
boundaries. Actual inductor current can temporarily exceed a newly reduced
reference; the physical model does not clip stored magnetic energy away.

A tripped DC converter routes its inductor current through an illustrative dump
resistor. Polarization relaxes at open circuit. Saved contactor status distinguishes
battery current from residual converter-inductor current.

## Inverter gate blocking

Low DC voltage or excessive temperature blocks the averaged bridge command.
Restart requires an explicit request, recovered DC voltage and temperature, and
a healthy dwell interval. During blocking, the average bridge is represented by
zero commanded voltage and the LC plant freewheels into its passive load.

This is not an arc, diode-commutation, physical AC-breaker or insulation model.
An AC voltage decay plot therefore demonstrates the modeled blocking sequence,
not proof of physical galvanic isolation.

## Time-qualified decisions

The definite-time relay resets pickup timing when a measurement becomes healthy.
The I-squared-time model accumulates normalized excess-current stress and cools
below pickup. It is deliberately not labeled as an IEC/IEEE curve.

Synchronization qualification combines phase angle, frequency, voltage magnitude
and energized-bus checks with a continuous healthy dwell. The phasor event driver
uses instantaneous SyncCheck criteria; SyncRelay is a separate sampled supervisor.

## Load shedding

Stages have independent thresholds, fractions and delays. Once tripped, a stage
remains shed until explicit restoration. The hybrid Python driver can apply the
stages to AC voltage magnitude; startup pickup is inhibited for the first 30 ms.
For a different startup sequence, use a supervisor matched to that sequence.

The built-in high-conductance regression also checks that plant integration
substeps resolve the fast passive LC decay. Numerical divergence must not be
reported as a physical fault.

## Measurement limits

The phasor frequency meter uses successive phase increments, rejects low-voltage
samples, and resets across a dead-bus interval. Frequency excursions must remain
within the phase-increment Nyquist limit. A discontinuous phase jump can appear
as a frequency spike and requires separate interpretation.

CT/PT saturation, relay communication, breaker travel time, negative sequence,
ground faults and device-specific ride-through are outside these supervisors.


## Rearm inrush interlock

A main-contact reset request remains pending while DC voltage is below the
precharge closing threshold. A modeled resistor path supplies limited capacitor
charging current, then the main converter resumes DC regulation. AC gating still
waits for its separate healthy-voltage dwell. Electrical audits include precharge
resistor losses and battery current.

Earlier trial recovery traces exposed a large boost-stage inrush when the battery
was directly reconnected to a link below pack voltage. The precharge regression
retains an explicit peak-current acceptance check alongside energy closure.
