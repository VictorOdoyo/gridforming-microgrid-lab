from gridlab.lab.damping_study import damping_study


def test_damping_study_reports_real_and_oscillatory_modes():
    rows = damping_study((0, 2))
    assert rows[1]["minimum_oscillatory_damping"] > rows[0]["minimum_oscillatory_damping"]
    assert all(r["maximum_real_pole"] < 0 for r in rows)
