from gridlab.converter.delay_study import delay_study


def test_delay_map_contains_stable_and_unstable_control_configurations():
    rows = delay_study(periods=(0.00005, 0.0005), delays=(0, 3))
    assert any(row["stable"] for row in rows)
    assert any(not row["stable"] for row in rows)
    assert len(rows) == 4
