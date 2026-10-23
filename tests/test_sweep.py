from gridlab.sweep import parameter_grid, run_sweep

def test_failed_cases_remain_in_results():
    cases = parameter_grid({"x": [0, 2], "y": [1, 3]})
    trials = run_sweep(lambda x, y: y/x, cases)
    assert len(trials) == 4
    assert sum(t.error is not None for t in trials) == 2
    assert trials[2].result == .5
