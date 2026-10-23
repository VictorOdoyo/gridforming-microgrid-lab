# Contributing

Start with docs/model.md and docs/validation.md. Describe the physical problem,
units, assumptions, and independent evidence for each numerical change.

Install the development extras and run:

```sh
python -m pip install -e ".[dev]"
python -m pytest -q
ruff check src tests
python -m build
```

Use a focused commit for each coherent capability or correction. Commit a model
with its analytical or behavioral verification. Do not pad history with empty
commits or split inseparable work to reach a count.

New control algorithms need a steady-state reference and a perturbed trajectory.
New scenarios should explain the event, observable response, and limitations.
Treat convergence evidence and physical validation as separate claims.

Generated experiment outputs belong under outputs/ and are ignored. Keep curated
reference results small, state how to regenerate them, and record physical
parameters. Never hand-edit a plot or metric to improve the reported outcome.

Report a bug with a minimal case JSON/TOML, Python/dependency versions, expected
behavior, observed behavior, and solver settings. Include the original error when
a network or operating-point solve fails.
