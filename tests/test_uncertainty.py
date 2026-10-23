from gridlab.uncertainty import latin_hypercube, percentiles


def test_seed_and_stratification():
    a = latin_hypercube({"x": (0, 1), "y": (10, 20)}, 10, 3)
    assert a == latin_hypercube({"x": (0, 1), "y": (10, 20)}, 10, 3)
    assert sorted(int(p["x"] * 10) for p in a) == list(range(10))
    assert percentiles([1, 2, 3])[50] == 2
