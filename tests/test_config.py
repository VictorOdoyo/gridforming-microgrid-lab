import pytest

from gridlab.config import Inverter, Microgrid


def test_rejects_duplicate_source_names_and_invalid_time_constants():
    source = Inverter("a", 0)
    with pytest.raises(ValueError):
        Microgrid(1, (), (0.5 + 0j,), (source, source))
    with pytest.raises(ValueError):
        Inverter("a", 0, power_tau=0)


def test_rejects_out_of_range_bus():
    with pytest.raises(ValueError):
        Microgrid(1, (), (0j,), (Inverter("a", 2),))
