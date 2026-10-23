from gridlab.lab.cases import converter_step, dc_step
from gridlab.lab.timing import retime


def test_shortened_case_retains_signal_event_at_its_final_sample():
    c = retime(dc_step(), 0.1)
    assert c.signals["demand_w"](0.1) == 60000
    assert c.signals["demand_w"](0.099) == 30000
    ramp = retime(converter_step(), 0.01)
    assert ramp.signals["reference_v"](0.01) == 162.5
