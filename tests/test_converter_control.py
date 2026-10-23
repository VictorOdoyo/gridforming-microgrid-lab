import numpy as np

from gridlab.converter.control import Cascade
from gridlab.converter.lc import LCPlant


def test_control_respects_physical_current_and_modulation_limits():
    p = LCPlant()
    c = Cascade.tuned(p, maximum_current_a=10)
    command = c.step(p, np.zeros(4), 325, 700, 0.1, 0.00005)
    assert abs(c.current_reference) <= 10
    assert abs(command) <= 700 / np.sqrt(3)
