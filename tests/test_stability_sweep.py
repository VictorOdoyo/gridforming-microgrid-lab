from gridlab.stability_sweep import stability_sweep


def test_stability_map_contains_stable_and_unstable_regions():
    rows = stability_sweep((2,), (0.02, 0.05))
    assert all(row.error is None for row in rows)
    assert rows[0].result["stable"]
    assert not rows[1].result["stable"]
