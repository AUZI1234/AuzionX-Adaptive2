"""Deterministic research foundation tests; synthetic fixtures are not market evidence."""
import unittest
from datetime import datetime, timezone, timedelta
from Research.data.validate_ticks import Tick, validate_ticks
from Research.features.causal_features import causal_features

BASE = datetime(2024, 1, 1, tzinfo=timezone.utc)
def t(i, bid, ask, seconds=None): return Tick(BASE + timedelta(seconds=i if seconds is None else seconds), bid, ask)

class TickValidationTests(unittest.TestCase):
    def test_duplicate_ticks(self): self.assertEqual(validate_ticks([t(0, 1, 2), t(1, 1, 2), t(1, 1, 2)])["duplicates"], 1)
    def test_missing_gap(self): self.assertEqual(validate_ticks([t(0, 1, 2), t(100, 1, 2)], 60)["gaps"], 1)
    def test_out_of_order(self): self.assertFalse(validate_ticks([t(1, 1, 2), t(0, 1, 2)])["valid"])
    def test_timestamp_collision(self): self.assertEqual(validate_ticks([t(0, 1, 2), t(0, 1.1, 2.1)])["timestamp_collisions"], 1)
    def test_spread_spike(self): self.assertGreater(t(0, 1, 3).spread, t(1, 1, 2).spread)
    def test_invalid_crossed_quote(self): self.assertFalse(validate_ticks([t(0, 2, 1)])["valid"])

class CausalFeatureTests(unittest.TestCase):
    def test_zero_movement(self): self.assertEqual(causal_features([t(0, 1, 2), t(1, 1, 2)])[1].signed_tick, 0)
    def test_rapid_movement(self): self.assertGreater(causal_features([t(0, 1, 2), t(1, 2, 3)])[1].short_return, 0)
    def test_acceleration_and_deceleration_inputs(self):
        rows = causal_features([t(0, 1, 2), t(1, 2, 3), t(2, 4, 5), t(3, 4.5, 5.5)])
        self.assertIsNotNone(rows[2].acceleration); self.assertIsNotNone(rows[3].acceleration)
    def test_reconnect_gap_is_not_filled(self): self.assertIsNone(causal_features([t(0, 1, 2), t(100, 2, 3)])[1].realized_volatility)
    def test_future_append_does_not_change_prior_rows(self):
        base = [t(0, 1, 2), t(1, 1.1, 2.1)]
        before = causal_features(base)
        after = causal_features(base + [t(2, 9, 10)])
        self.assertEqual(before, after[:2])

if __name__ == "__main__": unittest.main()
