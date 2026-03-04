"""
Tests for port_scan module. EDUCATIONAL USE ONLY.
"""
import sys
import os
import unittest

# Ensure package root is on path when running tests
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Attacks.port_scan import port_scan
from utils.helpers import load_config, validate_target
from utils.network import is_allowed_target


class TestPortScan(unittest.TestCase):
    def test_allowed_target_only(self):
        """port_scan must raise for disallowed targets."""
        with self.assertRaises(ValueError) as ctx:
            port_scan(host="192.168.1.1")
        self.assertIn("not allowed", str(ctx.exception))

    def test_port_scan_localhost_returns_list(self):
        """port_scan(127.0.0.1) returns list of (port, bool)."""
        results = port_scan(host="127.0.0.1", max_ports=5)
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 5)
        for item in results:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 2)
            port, is_open = item
            self.assertIsInstance(port, int)
            self.assertIn(port, range(1, 6))
            self.assertIsInstance(is_open, bool)

    def test_validate_target_localhost(self):
        self.assertTrue(validate_target("127.0.0.1"))
        self.assertTrue(validate_target("localhost"))

    def test_validate_target_rejected(self):
        self.assertFalse(validate_target("8.8.8.8"))
        self.assertFalse(validate_target("example.com"))

    def test_is_allowed_target(self):
        self.assertTrue(is_allowed_target("127.0.0.1"))
        self.assertFalse(is_allowed_target("192.168.0.1"))


if __name__ == "__main__":
    unittest.main()
