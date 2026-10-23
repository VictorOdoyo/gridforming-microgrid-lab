from gridlab.protection.shedding import StagedShedding


def test_stage_timing_latches_and_explicit_restore():
    s = StagedShedding()
    assert s.step(0.85, 0.01) == 1
    assert s.step(0.85, 0.01) == 0.75
    assert s.step(0.7, 0.01) == 0.5
    assert s.step(1, 0.1) == 0.5
    s.restore()
    assert s.step(1, 0.1) == 1
