# Measurement lag and hidden VSM instability

Equal initial conditions and identical sources constrain a simulation to a
symmetric trajectory. An unstable differential mode may remain unexcited.

The original trial setting used a 50 ms power filter. Linearization of the
two-source VSM benchmark detects a positive-real-part differential mode.
The default is therefore 20 ms. The regression suite checks both the stable
default and the deliberately unstable slower-filter configuration.

An independent time-domain check perturbs only the second source angle by
0.001 rad and observes differential frequency decay. This is local evidence
for this benchmark, not a universal tuning rule. Changes to network reactance,
inertia, droop, filter lag, and voltage loops require renewed analysis.
