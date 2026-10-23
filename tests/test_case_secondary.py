from gridlab.cases import load_step, secondary_restoration
from gridlab.events import run_events

def test_secondary_recovers_nominal_after_same_disturbance():
    case = secondary_restoration()
    r = run_events(case.config, case.events, case.duration)
    assert abs(r.frequency_hz[-1].mean()-50) < .002
    primary = load_step()
    p = run_events(primary.config, primary.events, 5)
    assert abs(p.frequency_hz[-1].mean()-50) > .1
