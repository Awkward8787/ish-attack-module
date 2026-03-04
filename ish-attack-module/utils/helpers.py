"""
EDUCATIONAL USE ONLY.
Helper utilities for ish-attack-module. Do not use against systems without authorization.
"""
import json
import os
from typing import Any, Dict

# Default path to config relative to this package
_CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "config")
_DEFAULT_SETTINGS_PATH = os.path.join(_CONFIG_DIR, "settings.json")


def load_config(path: str = None) -> Dict[str, Any]:
    """Load settings from config/settings.json. Returns dict with defaults if file missing."""
    if path is None:
        path = _DEFAULT_SETTINGS_PATH
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "allowed_targets": ["127.0.0.1", "localhost"],
            "port_scan": {"timeout_seconds": 1.0, "max_ports": 1024},
            "brute_force": {"max_attempts": 100, "delay_between_attempts_seconds": 0.1},
            "ddos_simulation": {
                "max_requests_per_second": 10,
                "duration_seconds_max": 5,
                "target_port": 80,
            },
        }


def validate_target(target: str, config: Dict[str, Any] = None) -> bool:
    """Return True only if target is in allowed_targets (e.g. localhost/127.0.0.1)."""
    if config is None:
        config = load_config()
    allowed = config.get("allowed_targets", ["127.0.0.1", "localhost"])
    normalized = (target or "").strip().lower()
    if normalized in ("localhost", "127.0.0.1"):
        return True
    return normalized in [a.strip().lower() for a in allowed]
