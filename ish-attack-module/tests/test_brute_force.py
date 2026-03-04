"""
Tests for brute_force module. EDUCATIONAL USE ONLY.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Attacks.brute_force import brute_force_attempt, DEFAULT_WORDLIST
from utils.network import is_allowed_target


class TestBruteForce(unittest.TestCase):
    def test_brute_force_rejects_disallowed_target(self):
        """brute_force_attempt must raise for non-localhost."""
        with self.assertRaises(ValueError) as ctx:
            brute_force_attempt(host="10.0.0.1")
        self.assertIn("not allowed", str(ctx.exception))

    def test_brute_force_demo_returns_none(self):
        """With no check_fn, brute_force_attempt runs demo and returns None."""
        result = brute_force_attempt(
            host="127.0.0.1", wordlist=["a", "b"], max_attempts=10
        )
        self.assertIsNone(result)

    def test_brute_force_returns_word_when_check_passes(self):
        """When check_fn returns True for a word, that word is returned."""
        result = brute_force_attempt(
            host="127.0.0.1",
            wordlist=["wrong", "correct", "other"],
            check_fn=lambda w: w == "correct",
            max_attempts=10,
            delay_seconds=0,
        )
        self.assertEqual(result, "correct")

    def test_default_wordlist_exists(self):
        self.assertIsInstance(DEFAULT_WORDLIST, list)
        self.assertGreaterEqual(len(DEFAULT_WORDLIST), 1)


if __name__ == "__main__":
    unittest.main()
