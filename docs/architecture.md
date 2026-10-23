# Architecture and extension guide

The package has three related but distinct modeling layers.

1. Balanced phasor dynamics: config, network, norton, limited_network, dynamics,
   simulation, events, cases.
2. Independent electrical components and slow energy dispatch: battery, thevenin,
   solar, diesel, dclink, rlfilter, lcl, modulation, thermal, dispatch, daily_energy.
3. Engineering analysis and reproducibility: operating_point, linearize, stability,
   modes, participation, sensitivity, uncertainty, convergence, summary, storage,
   config_io, provenance, plotting, report and CLI.

## Data flow

```mermaid
flowchart LR
    A[Named case or JSON/TOML] --> B[Validated configuration]
    B --> C[Exact event segmentation]
    C --> D[Control differential equations]
    D --> E[Algebraic network solve]
    E --> D
    D --> F[Sampled Result arrays]
    F --> G[Metrics and stability studies]
    F --> H[CSV / NPZ / figures]
    B --> I[Configuration hash and provenance]
    H --> J[Report bundle with checksums]
    I --> J
```

Configuration objects are frozen dataclasses. Each continuous event segment owns
its network and source mask. An ODE callback never mutates event state, relay
timers or battery state; rejected/adaptive integration steps therefore do not
accidentally advance discrete equipment.

## Adding a controller

Implement and analytically test its equations first. Add explicit state meanings
and units, then integrate them into Dynamics. Update operating-point constraints
and inactive-state elimination. Test an asymmetric perturbation as well as
symmetric sharing. Check both mode stability and nonlinear trajectories.

## Adding an event

Define its target, allowed values and ordering semantics. Apply it only at a
segment boundary. Record the changed status where needed. Test non-grid-aligned
event time, time zero, simultaneous events, and an event at the final time.

## Limitations that affect interpretation

- The AC dynamic model is balanced, positive sequence and fundamental frequency.
- Dynamic load demand is constant impedance. ZIP/PQ operating-point experiments
  are separate; they are not silently substituted into dynamic cases.
- Current limiting is algebraic radial saturation.
- Utility voltage has fixed magnitude and nominal frequency.
- Source DC availability, SOC and thermal states do not constrain AC cases.
- There is no PWM switching, harmonic production, fault arc, insulation model,
  negative sequence, detailed protection coordination or hardware interface.
- Synchronization tests are illustrative engineering criteria.
- The solver fails on singular unreferenced islands; inspect topology first.

## Further engineering work

Natural extensions include integrated DC-side energy limits, detailed dq inner
loops, unbalanced networks, explicit inverter saturation recovery, automatic
load shedding, communication delay models, independent EMT cross-validation,
and measured hardware parameter identification. Each needs its own validation.
