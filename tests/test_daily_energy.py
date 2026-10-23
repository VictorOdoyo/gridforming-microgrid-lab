import pytest

from gridlab.daily_energy import daily_energy


def test_daily_dispatch_balances_every_interval_and_obeys_energy_limits():
    report = daily_energy(600)
    for r in report["intervals"]:
        assert r["solar_kw"] + r["battery_kw"] + r["diesel_kw"] + r["unmet_kw"] == pytest.approx(r["load_kw"])
        assert 0.1 - 1e-12 <= r["soc"] <= 0.9 + 1e-12
    assert report["summary"]["unmet_kwh"] == 0
    assert report["summary"]["diesel_kwh"] < report["summary"]["load_kwh"]
    assert sum(r["interval_s"] for r in report["intervals"]) == 86400
