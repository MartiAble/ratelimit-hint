from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Mapping, Optional


@dataclass(frozen=True)
class DelayHint:
    delay_seconds: float
    source: str
    retry_at: datetime
    raw_value: str


_HEADER_CANDIDATES = (
    "retry-after",
    "ratelimit-reset",
    "x-ratelimit-reset",
)


def compute_delay(
    headers: Mapping[str, str],
    *,
    now: Optional[datetime] = None,
    cap: Optional[float] = None,
    floor: float = 0.0,
) -> Optional[DelayHint]:
    """Compute the next retry delay from common rate-limit headers.

    Precedence:
    1. Retry-After
    2. RateLimit-Reset
    3. X-RateLimit-Reset

    Supported formats:
    - Retry-After: integer seconds or HTTP-date
    - RateLimit-Reset: integer delta seconds or future epoch timestamp
    - X-RateLimit-Reset: epoch timestamp (common vendor behavior)
    """
    base_now = _normalize_now(now)
    lowered = {str(key).lower(): str(value).strip() for key, value in headers.items()}

    for header in _HEADER_CANDIDATES:
        raw = lowered.get(header)
        if not raw:
            continue

        delay = _parse_delay(header, raw, base_now)
        if delay is None:
            continue

        bounded = max(float(floor), delay)
        if cap is not None:
            bounded = min(bounded, float(cap))

        return DelayHint(
            delay_seconds=bounded,
            source=header,
            retry_at=base_now + timedelta_seconds(bounded),
            raw_value=raw,
        )

    return None


def next_retry_at(headers: Mapping[str, str], *, now: Optional[datetime] = None) -> Optional[datetime]:
    hint = compute_delay(headers, now=now)
    return hint.retry_at if hint else None


def _parse_delay(header: str, raw: str, now: datetime) -> Optional[float]:
    if header == "retry-after":
        return _parse_retry_after(raw, now)

    if header == "ratelimit-reset":
        return _parse_reset_value(raw, now, prefer_delta=True)

    if header == "x-ratelimit-reset":
        return _parse_reset_value(raw, now, prefer_delta=False)

    return None


def _parse_retry_after(raw: str, now: datetime) -> Optional[float]:
    seconds = _parse_float(raw)
    if seconds is not None:
        return max(0.0, seconds)

    try:
        parsed = parsedate_to_datetime(raw)
    except (TypeError, ValueError, IndexError, OverflowError):
        return None

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    return max(0.0, (parsed.astimezone(timezone.utc) - now).total_seconds())


def _parse_reset_value(raw: str, now: datetime, *, prefer_delta: bool) -> Optional[float]:
    value = _parse_float(raw)
    if value is None:
        return None

    if prefer_delta and value < 1_000_000_000:
        return max(0.0, value)

    if not prefer_delta and value >= 1_000_000_000:
        return max(0.0, value - now.timestamp())

    epoch_candidate = value - now.timestamp()
    if epoch_candidate >= 0:
        return epoch_candidate

    return max(0.0, value)


def _parse_float(raw: str) -> Optional[float]:
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def _normalize_now(now: Optional[datetime]) -> datetime:
    if now is None:
        return datetime.now(timezone.utc)

    if now.tzinfo is None:
        return now.replace(tzinfo=timezone.utc)

    return now.astimezone(timezone.utc)


def timedelta_seconds(seconds: float):
    from datetime import timedelta

    return timedelta(seconds=seconds)
