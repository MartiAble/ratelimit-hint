import unittest
from datetime import datetime, timezone

from ratelimit_hint import compute_delay, next_retry_at


class ComputeDelayTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 4, 26, 17, 0, 0, tzinfo=timezone.utc)

    def test_retry_after_seconds_wins(self):
        hint = compute_delay(
            {
                "Retry-After": "12",
                "RateLimit-Reset": "999",
            },
            now=self.now,
        )

        self.assertIsNotNone(hint)
        self.assertEqual(hint.source, "retry-after")
        self.assertEqual(hint.delay_seconds, 12.0)

    def test_retry_after_http_date(self):
        hint = compute_delay(
            {"Retry-After": "Sun, 26 Apr 2026 17:00:10 GMT"},
            now=self.now,
        )

        self.assertIsNotNone(hint)
        self.assertEqual(hint.delay_seconds, 10.0)

    def test_ratelimit_reset_delta_seconds(self):
        hint = compute_delay({"RateLimit-Reset": "45"}, now=self.now)
        self.assertIsNotNone(hint)
        self.assertEqual(hint.source, "ratelimit-reset")
        self.assertEqual(hint.delay_seconds, 45.0)

    def test_x_ratelimit_reset_epoch(self):
        future_epoch = int(self.now.timestamp()) + 90
        hint = compute_delay({"X-RateLimit-Reset": str(future_epoch)}, now=self.now)
        self.assertIsNotNone(hint)
        self.assertEqual(hint.source, "x-ratelimit-reset")
        self.assertEqual(hint.delay_seconds, 90.0)

    def test_cap_and_floor_are_applied(self):
        hint = compute_delay({"Retry-After": "0.5"}, now=self.now, floor=2, cap=10)
        self.assertIsNotNone(hint)
        self.assertEqual(hint.delay_seconds, 2.0)

    def test_invalid_values_return_none(self):
        self.assertIsNone(compute_delay({"Retry-After": "later please"}, now=self.now))

    def test_next_retry_at_returns_datetime(self):
        retry_at = next_retry_at({"Retry-After": "5"}, now=self.now)
        self.assertEqual(retry_at, datetime(2026, 4, 26, 17, 0, 5, tzinfo=timezone.utc))


if __name__ == "__main__":
    unittest.main()
