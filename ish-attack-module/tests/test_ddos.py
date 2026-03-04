"""
Tests for ddos simulation module. EDUCATIONAL USE ONLY.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Attacks.ddos import run_ddos_simulation


class TestDdos(unittest.TestCase):
    def test_ddos_rejects_disallowed_target(self):
        """run_ddos_simulation must raise for non-localhost."""
        with self.assertRaises(ValueError) as ctx:
            run_ddos_simulation(host="8.8.8.8")
        self.assertIn("not allowed", str(ctx.exception))

    def test_ddos_returns_stats(self):
        """Simulation returns dict with total_attempts, successful, failed."""
        stats = run_ddos_simulation(
            host="127.0.0.1",
            port=0,
            duration_seconds=0.2,
            requests_per_second=5,
        )
        self.assertIsInstance(stats, dict)
        self.assertIn("total_attempts", stats)
        self.assertIn("successful", stats)
        self.assertIn("failed", stats)
        self.assertEqual(
            stats["total_attempts"], stats["successful"] + stats["failed"]
        )
        self.assertGreaterEqual(stats["total_attempts"], 1)


if __name__ == "__main__":
    unittest.main()
