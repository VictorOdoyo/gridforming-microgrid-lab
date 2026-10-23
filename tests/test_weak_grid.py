from gridlab.weak_grid import weak_grid_study


def test_grid_strength_sweep_records_distinct_network_conditions():
    rows = weak_grid_study((0.05, 0.4), duration=2)
    assert rows[0]["scr"] > rows[1]["scr"]
    assert rows[0]["minimum_pu"] != rows[1]["minimum_pu"]
    assert all(row["nadir_hz"] > 48 for row in rows)
