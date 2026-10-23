from dataclasses import replace

from gridlab.cases import generator_trip
from gridlab.events import run_events
from gridlab.summary import summarize


def test_disconnected_internal_frequency_does_not_corrupt_report():
    c = generator_trip()
    r = run_events(c.config, c.events, 3, sample_s=0.1, max_step=0.05)
    f = r.frequency_hz.copy()
    f[~r.enabled] = -999
    assert summarize(replace(r, frequency_hz=f)) == summarize(r)
