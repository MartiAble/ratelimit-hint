# Acceptance Stage

## Repository structure check
- `pyproject.toml`
- `README.md`
- `LICENSE`
- `src/ratelimit_hint/__init__.py`
- `src/ratelimit_hint/core.py`
- `tests/test_core.py`
- `docs_PLAN.md`
- `docs_DESIGN.md`

## What was verified locally
- Unit test suite executed with `python -m unittest discover -s tests -v`.
- Editable install executed with `python -m pip install -e .`.

## Limitations
- Heuristics for `RateLimit-Reset` are intentionally generic and may not match every vendor-specific interpretation.
- The library computes retry timing only; it does not perform sleeping, request replay, or transport integration.
- Time skew between server and client can affect absolute timestamp-based headers.
- A GitHub Actions CI workflow was prepared during development, but the file was omitted from the published repository because the available GitHub token lacked `workflow` scope.

## Unverified runtime assumptions
- Python 3.9–3.11 were not executed locally on this host; compatibility is based on syntax and standard-library usage.
- PyPI publication was not performed in this run.
