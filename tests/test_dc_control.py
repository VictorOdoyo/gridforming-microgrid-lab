from gridlab.dc.control import DCControl
from gridlab.dc.system import DCSystem


def test_bms_trip_blocks_converter_and_healthy_operation_requests_support():
    plant, c = DCSystem(), DCControl()
    state = plant.initial()
    duty, closed = c.step(plant, state, 50000, 0.0001)
    assert closed and 0 < duty < 1 and c.reference_a > 0
    state[0] = 0.09
    duty, closed = c.step(plant, state, 50000, 0.0001)
    assert not closed and duty == 0 and c.reference_a == 0
