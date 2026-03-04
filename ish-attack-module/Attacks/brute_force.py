"""
EDUCATIONAL USE ONLY.
Brute-force simulation for learning (e.g. dictionary/login attempt concepts).
Uses a small wordlist and only allowed targets. Do not use on unauthorized systems.
"""
import time
from typing import Callable, List, Optional

from utils.helpers import load_config, validate_target
from utils.network import is_allowed_target


# Small educational wordlist (never use real credentials)
DEFAULT_WORDLIST = ["admin", "password", "123456", "test", "guest", "root", "user"]


def brute_force_attempt(
    host: str = "127.0.0.1",
    port: int = 0,
    wordlist: List[str] = None,
    check_fn: Callable[[str], bool] = None,
    max_attempts: int = None,
    delay_seconds: float = None,
) -> Optional[str]:
    """
    Simulate brute-force by trying each word from wordlist against check_fn.
    If check_fn is None, runs in demo mode: tries words and returns None (no real auth).
    EDUCATIONAL USE ONLY. Restricted to allowed targets and attempt limits.
    """
    if not is_allowed_target(host):
        raise ValueError("Target not allowed. Educational use: 127.0.0.1 or localhost only.")
    config = load_config()
    bf = config.get("brute_force", {})
    if max_attempts is None:
        max_attempts = bf.get("max_attempts", 100)
    if delay_seconds is None:
        delay_seconds = float(bf.get("delay_between_attempts_seconds", 0.1))
    words = wordlist or DEFAULT_WORDLIST
    check = check_fn or (lambda _: False)
    for i, word in enumerate(words):
        if i >= max_attempts:
            break
        if check(word):
            return word
        time.sleep(delay_seconds)
    return None
