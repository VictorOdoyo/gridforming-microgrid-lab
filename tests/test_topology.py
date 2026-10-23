from gridlab.network import Line
from gridlab.topology import islands, unpowered_islands

def test_open_breaker_creates_island():
    lines = [Line(0, 1, .1, .2), Line(1, 2, .1, .2, enabled=False)]
    assert islands(3, lines) == [(0, 1), (2,)]
    assert unpowered_islands(3, lines, [0]) == [(2,)]
