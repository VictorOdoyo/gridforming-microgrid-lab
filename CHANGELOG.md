# Changelog

## 0.2.0 — energy-coupled physical laboratory

- Added battery OCV/current/polarization dynamics, chemical-energy integration,
  thermal derating, contactor supervision and averaged bidirectional DC conversion.
- Coupled DC storage to an averaged AC bridge and LC filter through instantaneous
  power, with a DC-dependent modulation ceiling and explicit converter losses.
- Added sampled DC and AC cascade control, vector anti-windup, droop/VSM oscillator
  references and secondary frequency restoration.
- Added brownout blocking, healthy-dwell restart, I²t, precharge, staged shedding,
  synchronization dwell and a deenergized-bus-aware frequency meter.
- Added ADC, transport delay, SVPWM, ideal carrier switching and dead-time utilities.
- Added passivity certificates, LQR design, Kalman observation, LCL active damping,
  exact sampled-loop stability maps and fixed-control-rate integration convergence.
- Added twelve named physical experiments, custom JSON cases with initial states,
  typed trace archives, SI CSV telemetry, report bundles and gridlab lab commands.
- Extended CI to cover example code and a physical report from an installed wheel.

The original multi-bus balanced phasor API remains available. Its per-unit RMS
states are separate from the new physical layer's SI peak-dq states. The physical
layer represents one inverter feeding passive conductance, not a full multi-bus
EMT network. Switching-waveform utilities do not convert average hybrid runs into
switching-level simulations.

## 0.1.0 — balanced phasor laboratory

Introduced passive network analysis, droop/VSM controls, exact scheduled events,
black start, generation loss, secondary restoration, checked utility reconnection,
stability analysis, energy dispatch, reproducible reports and validation benchmarks.
