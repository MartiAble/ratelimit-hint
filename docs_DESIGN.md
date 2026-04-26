# Spec / Design Stage

## DX goals
- One-function entry point for the common case.
- Accept plain dict-like HTTP headers.
- Return a typed, inspectable result instead of a bare number.
- Stay dependency-free.

## Public API shape
- `compute_delay(headers, *, now=None, cap=None, floor=0.0) -> DelayHint | None`
- `next_retry_at(headers, *, now=None) -> datetime | None`
- `DelayHint(delay_seconds, source, retry_at, raw_value)`

## README structure
1. What the package does
2. Installation
3. Quick start
4. Supported headers and precedence
5. API reference
6. Testing
7. Limitations
8. License

## Package architecture
- `src/ratelimit_hint/__init__.py` — public exports and version.
- `src/ratelimit_hint/core.py` — parsing logic and dataclass.
- `tests/test_core.py` — unit coverage for supported header formats and boundary behavior.
- `.github/workflows/ci.yml` — planned multi-version Python CI (not published because the available GitHub token lacked `workflow` scope).

## Design choices
- Header lookup is case-insensitive.
- `Retry-After` has highest precedence because it is the clearest explicit retry signal.
- `RateLimit-Reset` supports both delta-seconds and future epoch timestamps as a practical compatibility heuristic.
- Naive datetimes are treated as UTC.
