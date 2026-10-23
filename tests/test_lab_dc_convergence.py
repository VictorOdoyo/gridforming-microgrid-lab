from gridlab.lab.dc_convergence import dc_convergence


def test_fixed_control_rate_integration_converges_toward_tight_reference():
    rows = dc_convergence((1, 4), duration=0.03)
    assert rows[1]["maximum_capacitor_energy_error_j"] < rows[0]["maximum_capacitor_energy_error_j"]
    assert rows[0]["maximum_inductor_error_a"] < 0.01
