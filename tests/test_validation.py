import pytest
from gridlab.cases import load_step
from gridlab.events import Event, run_events
from gridlab.simulation import simulate

@pytest.mark.parametrize("kwargs", [{"rtol": 0}, {"atol": -1}, {"max_step": float("nan")},
                                    {"sample_s": 1e-12}])
def test_invalid_solver_options_rejected_before_integration(kwargs):
    config = load_step().config
    for solver in (simulate, run_events):
        with pytest.raises(ValueError):
            solver(config, **kwargs)

def test_fractional_event_target_is_rejected():
    with pytest.raises(ValueError):
        Event(1, "load_scale", 2, .5)
