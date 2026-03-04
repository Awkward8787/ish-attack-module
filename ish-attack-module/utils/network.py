"""
EDUCATIONAL USE ONLY.
Network utilities for ish-attack-module. All operations restricted to allowed targets (e.g. localhost).
"""
import socket
from typing import Optional

from .helpers import load_config, validate_target


def is_allowed_target(host: str) -> bool:
    """Return True only if host is in config allowed_targets (e.g. 127.0.0.1, localhost)."""
    return validate_target(host, load_config())


def check_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    """
    Attempt TCP connect to host:port. Returns True if connection succeeds.
    FOR EDUCATIONAL USE ONLY. Only call with allowed targets (e.g. 127.0.0.1).
    """
    if not is_allowed_target(host):
        raise ValueError("Target not in allowed list. Educational use: localhost/127.0.0.1 only.")
    if not (0 <= port <= 65535):
        raise ValueError("Port must be 0-65535")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            return True
    except (socket.timeout, socket.error, OSError):
        return False
