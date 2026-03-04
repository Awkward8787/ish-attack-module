"""
EDUCATIONAL USE ONLY.
Port scanning simulation for learning. Only scans allowed targets (e.g. localhost).
Do not use against systems you do not own or have explicit permission to test.
"""
import socket
from typing import List, Tuple

from utils.helpers import load_config, validate_target
from utils.network import is_allowed_target


def port_scan(host: str = "127.0.0.1", max_ports: int = None, timeout: float = None) -> List[Tuple[int, bool]]:
    """
    Scan a limited range of ports on host via TCP connect.
    Returns list of (port, is_open). EDUCATIONAL USE ONLY. Localhost only.
    """
    if not is_allowed_target(host):
        raise ValueError("Target not allowed. Educational use: 127.0.0.1 or localhost only.")
    config = load_config()
    ps = config.get("port_scan", {})
    if max_ports is None:
        max_ports = ps.get("max_ports", 1024)
    if timeout is None:
        timeout = float(ps.get("timeout_seconds", 1.0))
    max_ports = min(max(1, max_ports), 1024)
    results = []
    for port in range(1, max_ports + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect((host, port))
                results.append((port, True))
        except (socket.timeout, socket.error, OSError):
            results.append((port, False))
    return results
