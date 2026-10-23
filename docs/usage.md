# Running experiments

Use Python 3.11 or newer and install from the repository root:

```sh
python -m pip install -e ".[dev]"
gridlab list
gridlab run --case island-recovery --mode vsm --output outputs/recovery
gridlab run --config examples/custom-island.toml --output outputs/custom
gridlab compare --output outputs/control-comparison
gridlab stability --case load-step --mode vsm
```

Open outputs/recovery/index.html in a browser. Its adjacent files contain the
original trace, case, metrics and provenance. NPZ loading does not enable pickle.

## Built-in cases

| Case | Purpose |
| --- | --- |
| load-step | Equal sharing and primary frequency offset |
| secondary-restoration | Integral restoration after demand growth |
| generator-trip | Source isolation and survivor pickup |
| black-start | Dead-bus energization and staged load pickup |
| island-recovery | Source outage, coordinated synchronization, checked reclose |
| radial-feeder | Remote load step and unequal source ratings |
| overload | Current ceiling and consequent bus-voltage depression |

All named cases accept --mode droop or --mode vsm. Controller behavior can differ
by case; the model equations explain how the two modes use source states.

## Editing cases

```sh
gridlab export-case --case radial-feeder --output outputs/feeder.json
gridlab run --config outputs/feeder.json --output outputs/feeder-run
gridlab inspect outputs/feeder-run/trace.npz
```

Complex impedances, load powers and grid voltages are [real, imag] pairs in case
files. An unlimited source current is JSON null. Unknown dataclass parameters
produce an error. Bus and source indices start at zero.

## Study commands

```sh
gridlab study weak-grid --output outputs/weak-grid.json
gridlab study stability-map --output outputs/stability-map.json
gridlab study convergence --output outputs/convergence.json
gridlab study robustness --count 20 --seed 42 --output outputs/robustness.json
gridlab study daily-energy --output outputs/daily-energy.json
```

The daily energy study is a separate solar/battery/diesel dispatch model with
five-minute held-power intervals. It does not run fast AC dynamics for a full day.
The robustness study records failures; percentile results describe successful
bounded parameter trials, rather than a probability of real-world reliability.

## Python API

```python
from gridlab.cases import radial_feeder
from gridlab.events import run_events
from gridlab.summary import summarize

case = radial_feeder("vsm")
trace = run_events(case.config, case.events, case.duration)
print(summarize(trace))
```

Use sample_s for output resolution and max_step for the maximum internal solver
step. Adaptive error tolerances also affect the actual steps. Event times always
split integration segments. A shortened CLI --duration omits later events and
saves the shortened case in the report.

## Troubleshooting

A singular network usually means an island has no voltage reference and no
effective passive grounding. A rejected reclose means at least one synchronization
criterion is unmet. A failed nonlinear current-limit solve reports its KCL
residual; reduce loading or examine the network rather than accepting bad output.
