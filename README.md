# Grid-forming Microgrid Lab

A reproducible engineering laboratory for inverter-dominated microgrids.
The main solver represents balanced positive-sequence RMS phasors and reduced
outer-loop controls. Component experiments are explicitly separate from that solver.

Development covers droop and virtual synchronous machine controls, passive networks,
load disturbances, islanding, synchronization, secondary restoration, and quantitative
validation. Switching harmonics and unbalanced electromagnetic transients require
a different model and are outside the phasor solver's claims.

## Development

Requires Python 3.11 or newer.

```sh
python -m pip install -e ".[dev]"
python -m pytest
```

See the evolving engineering documentation and tests for model conventions.
