# Research and numerical references

The implementation is original reduced-model software. The references below
provide context; this repository does not claim exact reproduction of a paper's
complete inverter implementation or experimental results.

1. **Research Roadmap on Grid-Forming Inverters** (2020), NREL/TP-5D00-73476.
   [Publication record](https://research-hub.nlr.gov/en/publications/research-roadmap-on-grid-forming-inverters/)
   and [report](https://www.nrel.gov/docs/fy21osti/73476.pdf).
   Context for grid-forming controls, system integration, and validation needs.

2. Aidar Zhetessov, **Grid-Forming Control of Power Converters: Equivalence Proof
   through Simplified Models** (2023).
   [arXiv:2311.17926](https://arxiv.org/abs/2311.17926).
   Discusses relationships among control laws near a selected nominal point.
   That local equivalence is not assumed to hold during limiting or reconnection.

3. **SciPy solve_ivp documentation**.
   [Official API reference](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html).
   Defines adaptive tolerances, integration methods, dense output and maximum step.
   This laboratory implements scheduled discontinuities by splitting integrations.

4. **SciPy continuous Lyapunov solver**.
   [Official API reference](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.solve_continuous_lyapunov.html).
   The energy certificate uses A-transpose P + P A = -I for a Hurwitz subsystem.

## Traceability to code

- Droop and swing equations: droop.py, vsm.py, dynamics.py; derivations in model.md.
- Local operating point and relative-state reduction: operating_point.py, stability.py.
- Measurement-lag instability: experiments/vsm-stability.md and test_vsm_stability.py.
- Event timing and reconnection: events.py, synchronization.py and their regression tests.
- Network and component verification: validation.md maps each invariant to evidence.

All gain defaults are illustrative benchmark parameters. They are not values
extracted from a particular commercial inverter or installation.
