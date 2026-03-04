#!/usr/bin/env python3
"""
EDUCATIONAL USE ONLY.
CLI for ish-attack-module. Use in Alpine iSH terminal: python main.py [command] [options].
All operations restricted to localhost/allowed_targets.
"""
from __future__ import print_function

import argparse
import sys
import os

# Ensure package root is on path when run as script from any cwd
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from Attacks import port_scan, brute_force_attempt, run_ddos_simulation
from utils import load_config, is_allowed_target


def cmd_port_scan(host: str, max_ports: int, timeout: float) -> int:
    """Run port scan and print (port, open) list."""
    if not is_allowed_target(host):
        print("Error: Target not allowed. Use 127.0.0.1 or localhost only.", file=sys.stderr)
        return 1
    results = port_scan(host=host, max_ports=max_ports, timeout=timeout)
    open_ports = [p for p, open_ in results if open_]
    print("Port scan {} (max_ports={}):".format(host, max_ports))
    for port, is_open in results:
        print("  port {}: {}".format(port, "open" if is_open else "closed"))
    if open_ports:
        print("Open: {}".format(open_ports))
    return 0


def cmd_brute_force(host: str, wordlist: list, max_attempts: int, delay: float) -> int:
    """Run brute-force simulation (demo mode; no real auth)."""
    if not is_allowed_target(host):
        print("Error: Target not allowed. Use 127.0.0.1 or localhost only.", file=sys.stderr)
        return 1
    result = brute_force_attempt(
        host=host,
        wordlist=wordlist or None,
        max_attempts=max_attempts,
        delay_seconds=delay,
    )
    print("Brute-force simulation on {} (demo mode):".format(host))
    print("  Result: {}".format("matched " + repr(result) if result else "no match (demo)"))
    return 0


def cmd_ddos(host: str, port: int, duration: float, rps: float) -> int:
    """Run rate-limited DDoS simulation."""
    if not is_allowed_target(host):
        print("Error: Target not allowed. Use 127.0.0.1 or localhost only.", file=sys.stderr)
        return 1
    stats = run_ddos_simulation(
        host=host,
        port=port,
        duration_seconds=duration,
        requests_per_second=rps,
    )
    print("DDoS simulation {}:{} for {:.1f}s @ {:.1f} req/s:".format(host, port, duration, rps))
    print("  total_attempts: {}".format(stats["total_attempts"]))
    print("  successful: {}".format(stats["successful"]))
    print("  failed: {}".format(stats["failed"]))
    return 0


def main() -> int:
    cfg = load_config()
    ps = cfg.get("port_scan", {})
    bf = cfg.get("brute_force", {})
    ddos = cfg.get("ddos_simulation", {})

    parser = argparse.ArgumentParser(
        description="ish-attack-module CLI (EDUCATIONAL USE ONLY). Localhost/allowed targets only."
    )
    sub = parser.add_subparsers(dest="command", help="command")

    # port-scan
    p_scan = sub.add_parser("port-scan", help="TCP port scan (localhost)")
    p_scan.add_argument("--host", default="127.0.0.1", help="Target host (default: 127.0.0.1)")
    p_scan.add_argument("--max-ports", type=int, default=ps.get("max_ports", 1024), help="Max ports to scan")
    p_scan.add_argument("--timeout", type=float, default=ps.get("timeout_seconds", 1.0), help="Timeout per port (s)")

    # brute-force
    p_bf = sub.add_parser("brute-force", help="Brute-force simulation (demo)")
    p_bf.add_argument("--host", default="127.0.0.1", help="Target host")
    p_bf.add_argument("--wordlist", type=str, default="", help="Comma-separated words (default: built-in)")
    p_bf.add_argument("--max-attempts", type=int, default=bf.get("max_attempts", 100), help="Max attempts")
    p_bf.add_argument("--delay", type=float, default=bf.get("delay_between_attempts_seconds", 0.1), help="Delay between attempts (s)")

    # ddos
    p_ddos = sub.add_parser("ddos", help="Rate-limited DDoS simulation")
    p_ddos.add_argument("--host", default="127.0.0.1", help="Target host")
    p_ddos.add_argument("--port", type=int, default=ddos.get("target_port", 80), help="Target port")
    p_ddos.add_argument("--duration", type=float, default=min(float(ddos.get("duration_seconds_max", 5)), 5.0), help="Duration (s)")
    p_ddos.add_argument("--rps", type=float, default=min(float(ddos.get("max_requests_per_second", 10)), 20.0), help="Requests per second")

    args = parser.parse_args()

    if args.command == "port-scan":
        return cmd_port_scan(args.host, args.max_ports, args.timeout)
    if args.command == "brute-force":
        wordlist = [w.strip() for w in args.wordlist.split(",") if w.strip()] or None
        return cmd_brute_force(args.host, wordlist, args.max_attempts, args.delay)
    if args.command == "ddos":
        return cmd_ddos(args.host, args.port, args.duration, args.rps)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
