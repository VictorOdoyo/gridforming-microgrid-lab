from gridlab.lab.case import run_case
from gridlab.lab.cases import converter_step
from gridlab.lab.metrics import summarize


def test_named_inner_loop_step_tracks_four_hundred_volt_line_rms():
    c = converter_step()
    m = summarize(c, run_case(c))
    assert abs(m["final_ac_ll_rms_v"] - 398.042) < 1
    assert m["final_tracking_error_peak_v"] < 1
