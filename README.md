# ratelimit-hint

Tiny Python helpers to compute retry delays from HTTP rate-limit headers.

`ratelimit-hint` turns common HTTP backoff headers into a structured result you can use in API clients, SDKs, and cron jobs without dragging in a bigger retry framework.

## Why

APIs rarely agree on one header format:

- `Retry-After: 30`
- `Retry-After: Sun, 26 Apr 2026 17:00:10 GMT`
- `RateLimit-Reset: 45`
- `X-RateLimit-Reset: 1777222810`

This package gives you one small function that normalizes those signals into a concrete delay.

## Installation

```bash
pip install ratelimit-hint
```

## Quick start

```python
from ratelimit_hint import compute_delay

headers = {
    "Retry-After": "12",
}

hint = compute_delay(headers)

if hint:
    print(hint.delay_seconds)  # 12.0
    print(hint.source)         # retry-after
    print(hint.retry_at)       # timezone-aware UTC datetime
```

## Supported headers and precedence

The parser checks headers in this order:

1. `Retry-After`
2. `RateLimit-Reset`
3. `X-RateLimit-Reset`

Supported formats:

- `Retry-After`: integer/float seconds or HTTP-date
- `RateLimit-Reset`: delta seconds or future epoch timestamp
- `X-RateLimit-Reset`: epoch timestamp

Header matching is case-insensitive.

## API

### `compute_delay(headers, *, now=None, cap=None, floor=0.0)`

Returns `DelayHint | None`.

Arguments:

- `headers`: any dict-like mapping of header names to values
- `now`: override current time for deterministic tests or simulations
- `cap`: optional maximum delay in seconds
- `floor`: optional minimum delay in seconds

### `DelayHint`

```python
DelayHint(
    delay_seconds: float,
    source: str,
    retry_at: datetime,
    raw_value: str,
)
```

### `next_retry_at(headers, *, now=None)`

Convenience helper that returns just the computed retry timestamp.

## Example with fallback headers

```python
from ratelimit_hint import compute_delay

headers = {
    "X-RateLimit-Reset": "1777222810",
}

hint = compute_delay(headers, cap=300)

if hint:
    print(f"sleep for {hint.delay_seconds:.0f}s")
```

## Testing

The package was verified locally with editable install + `unittest`. A GitHub Actions workflow was also prepared during development, but it is not included in the published repository because the available GitHub token did not have `workflow` scope.


```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

## Limitations

- `RateLimit-Reset` is interpreted with a generic heuristic because vendors do not fully agree on the format.
- The package computes timing only; it does not sleep, retry, or integrate with a specific HTTP client.
- Absolute timestamp headers depend on reasonable clock sync between client and server.

## License

MIT
