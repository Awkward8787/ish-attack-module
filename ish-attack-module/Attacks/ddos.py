"""
EDUCATIONAL USE ONLY.
DoS/DDoS simulation for learning (rate-limited, localhost only).
Simulates many connection attempts within safe limits. Do not use on unauthorized systems.
"""
import socket
import time
from typing import List

from utils.helpers import load_config
from utils.network import is_allowed_target


def _send_requests(host: str, port: int, count: int, timeout: float, results: List[bool]) -> None:
    """Worker: attempt count TCP connections and record success/failure."""
    for _ in range(count):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect((host, port))
                results.append(True)
        except (socket.timeout, socket.error, OSError):
            results.append(False)


def run_ddos_simulation(
    host: str = "127.0.0.1",
    port: int = None,
    duration_seconds: float = None,
    requests_per_second: float = None,
    timeout: float = 0.5,
) -> dict:
    """
    Run a rate-limited "stress" simulation: many short-lived TCP connection attempts.
    Returns stats (total_attempts, successful, failed). EDUCATIONAL USE ONLY. Localhost only.
    """
    if not is_allowed_target(host):
        raise ValueError("Target not allowed. Educational use: 127.0.0.1 or localhost only.")
    config = load_config()
    ddos_cfg = config.get("ddos_simulation", {})
    if port is None:
        port = ddos_cfg.get("target_port", 0)
    if duration_seconds is None:
        duration_seconds = min(float(ddos_cfg.get("duration_seconds_max", 5)), 5.0)
    if requests_per_second is None:
        requests_per_second = min(float(ddos_cfg.get("max_requests_per_second", 10)), 20.0)
    port = max(0, min(65535, port))
    duration_seconds = max(0.1, min(5.0, duration_seconds))
    requests_per_second = max(1, min(20, requests_per_second))

    results: List[bool] = []
    interval = 1.0 / requests_per_second
    end_time = time.monotonic() + duration_seconds
    while time.monotonic() < end_time:
        _send_requests(host, port, 1, timeout, results)
        time.sleep(interval)
    successful = sum(1 for r in results if r)
    return {
        "total_attempts": len(results),
        "successful": successful,
        "failed": len(results) - successful,
    }
