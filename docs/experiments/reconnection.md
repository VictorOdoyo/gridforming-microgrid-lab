# Island recovery and synchronization

The island-recovery scenario starts with two islanded VSM sources, trips one at
2 seconds, and requests utility reconnection at 16 seconds.

Secondary frequency control and phase synchronization must be coordinated.
The secondary integrator observes frequency deviation after subtracting the
synchronization bias. Otherwise it can cancel a persistent phase correction,
leaving nominal frequency with an unacceptable phase error.

A close request must satisfy voltage magnitude, frequency, phase-angle and
minimum energized-voltage checks. A failed request raises an error rather than
silently closing. These are simulation criteria, not relay certification settings.
