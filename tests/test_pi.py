from gridlab.pi import PI

def test_saturation_does_not_store_unbounded_error():
    pi = PI(1, 2, -1, 1)
    for _ in range(1000):
        assert pi.step(10, .01) == 1
    assert pi.integral == 0
    assert pi.step(-.1, .01) < 0

def test_zero_error_retains_integral():
    pi = PI(0, 1)
    assert pi.step(1, 1) == 1
    assert pi.step(0, 1) == 1
