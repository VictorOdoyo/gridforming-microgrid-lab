# Physical laboratory guide

Install the project normally, then use the lab command group:

```sh
gridlab lab list
gridlab lab run --case hybrid-step --output outputs/physical-step
gridlab lab run --case hybrid-restart --output outputs/physical-restart
gridlab lab run --case hybrid-cloud --output outputs/physical-cloud
gridlab lab run --case hybrid-secondary --output outputs/physical-secondary
```

The report directory includes an HTML view, PNG/SVG figures, a CSV with named SI
state columns, a typed pickle-free NPZ archive, case JSON, metrics, provenance,
and checksums. Actual termination is reported when a DC-only run browns out early.

## Available experiments

| Case | Purpose |
| --- | --- |
| dc-step | 30 to 60 kW demand step and DC voltage recovery |
| dc-reversal | Change discharge into regenerative charging |
| dc-contactor | Trip and explicitly rearm the battery contactor |
| dc-hot-pack | Soft thermal derating before hard temperature protection |
| converter-step | Sampled AC cascade tracking after a conductance step |
| converter-sag | DC supply sag, modulation saturation and recovery |
| hybrid-step | Grid-forming physical battery-to-AC load response |
| hybrid-outage | Battery trip, DC hold-up and latched gate blocking |
| hybrid-restart | Battery rearm, capacitor recharge and guarded AC restart |
| hybrid-cloud | Solar surplus charging followed by a cloud transition |
| hybrid-low-soc | Limited SOC reserve cannot act as an unlimited source |
| hybrid-secondary | Frequency restoration with actual DC energy demand |

## Custom cases

```sh
gridlab lab export-case --case hybrid-cloud --output outputs/cloud.json
gridlab lab run --config outputs/cloud.json --output outputs/custom-cloud
gridlab lab inspect outputs/custom-cloud/trace.npz
gridlab lab run --case hybrid-step --mode droop --output outputs/physical-droop
```

Physical JSON cases use schema_version 1, a model kind, nested plant parameters,
signals, optional initial_state, event schedule, duration and control period.
Unknown signals, invalid physical domains and incompatible event types fail early.

Signals support right-continuous steps or linear interpolation. Every signal knot
is inserted into the control/integration timeline. Shortening a case preserves
interpolation slope and changes exactly at the new final time.

The DC laboratory uses DCEvent kinds demand_w, trip and reset. The hybrid
laboratory uses conductance, reference_v, battery-trip, battery-reset and gate-reset.
Converter experiments use signals instead of supervisor events.

An initial_state is stored explicitly when supplied. State units and ordering are
listed in physical-model.md. A zero-energy DC capacitor requires a precharge
experiment; the active DC current controller cannot start from zero link voltage.

## Studies

```sh
gridlab lab study sample-delay --output outputs/sample-delay.json
gridlab lab study dc-convergence --output outputs/dc-convergence.json
gridlab lab study observer --output outputs/observer.json
gridlab lab study active-damping --output outputs/active-damping.json
```

The DC convergence study refines only physical integration while retaining the
same digital control ticks. The sampled-delay study instead changes the digital
control period and command transport delay; it is a stability study, not a pure
integration convergence experiment.

## Python use

```python
from gridlab.lab.cases import hybrid_step
from gridlab.lab.case import run_case
from gridlab.lab.metrics import summarize

case = hybrid_step("vsm")
trace = run_case(case)
print(summarize(case, trace))
```

Direct simulation APIs also accept measurement chains, controller objects or
staged shedding where appropriate. Those custom Python objects are outside the
portable JSON schema; record their parameters separately when using them.
