# ish-attack-module

**EDUCATIONAL USE ONLY.** This module demonstrates basic concepts of port scanning, brute-force attempts, and DoS simulation for learning purposes only. Do **not** use against any system you do not own or have explicit written permission to test. Unauthorized access to computer systems is illegal.

Designed for use in a **terminal environment**, especially **Alpine iSH** on iOS: all features work from the command line and via Python imports.

## Disclaimer

- All "attack" code is restricted to **localhost (127.0.0.1)** or targets listed in `config/settings.json` under `allowed_targets`.
- Rates, ports, and durations are limited by configuration to prevent misuse.
- Use only in lab environments or on your own machines for education.

## Alpine iSH (iOS) setup

1. Install **iSH** from the App Store (Alpine Linux terminal).
2. Install Python 3 (if not present):
   ```bash
   apk add python3 py3-pip
   ```
3. Copy or clone this repo into a folder (e.g. `ish-attack-module`).
4. From that folder, run the CLI or tests:
   ```bash
   cd ish-attack-module
   python3 main.py --help
   python3 main.py port-scan --max-ports 10
   python3 main.py brute-force --max-attempts 5
   python3 main.py ddos --duration 2 --rps 5
   ```

No pip install required: the module runs from the directory. Optional: `pip install pytest` for `pytest tests/ -v`.

## CLI (terminal)

From inside `ish-attack-module`:

```bash
# Help
python3 main.py --help
python3 main.py port-scan --help
python3 main.py brute-force --help
python3 main.py ddos --help

# Port scan (localhost, limited ports)
python3 main.py port-scan --host 127.0.0.1 --max-ports 20

# Brute-force simulation (demo; no real auth)
python3 main.py brute-force --host 127.0.0.1 --wordlist "admin,test,root" --max-attempts 10

# DDoS simulation (rate-limited, localhost)
python3 main.py ddos --host 127.0.0.1 --port 80 --duration 3 --rps 10
```

Alternative: `python3 -m main port-scan --max-ports 5` (same as above when run from `ish-attack-module`).

## Programmatic use

```bash
cd ish-attack-module
```

```python
# From Attacks subpackage
from Attacks import port_scan, brute_force_attempt, run_ddos_simulation

print(port_scan("127.0.0.1", max_ports=5))
# [(1, False), (2, False), ...]

result = brute_force_attempt("127.0.0.1", wordlist=["a", "b"], check_fn=lambda w: w == "b")
# result == "b"

stats = run_ddos_simulation("127.0.0.1", port=80, duration_seconds=1, requests_per_second=5)
# {"total_attempts": 5, "successful": 0, "failed": 5}
```

```python
# Utils: config and target checks
from utils import load_config, validate_target, is_allowed_target, check_port_open

cfg = load_config()
assert is_allowed_target("127.0.0.1")
assert not is_allowed_target("8.8.8.8")
open_22 = check_port_open("127.0.0.1", 22)
```

## Structure

- **config/settings.json** – Allowed targets and limits (timeouts, max attempts, etc.).
- **main.py** – CLI entrypoint for terminal use (port-scan, brute-force, ddos).
- **utils/** – Helpers and network checks (`load_config`, `validate_target`, `is_allowed_target`, `check_port_open`).
- **Attacks/** – Educational modules:
  - `port_scan` – TCP connect-style port scan (localhost only).
  - `brute_force` – Dictionary-style attempt simulation with optional check function.
  - `ddos` – Rate-limited connection simulation (localhost only).
- **tests/** – Unit tests (unittest); run with unittest or pytest.

## Config

Edit `config/settings.json` to change:

- `allowed_targets` – Only these hosts are accepted (default: `127.0.0.1`, `localhost`).
- `port_scan.timeout_seconds`, `port_scan.max_ports`
- `brute_force.max_attempts`, `brute_force.delay_between_attempts_seconds`
- `ddos_simulation.max_requests_per_second`, `duration_seconds_max`, `target_port` (default 80)

## Verification

From `ish-attack-module`:

```bash
# Unit tests (no extra deps)
python3 -m unittest discover -s tests -v

# With pytest (pip install pytest)
python3 -m pytest tests/ -v
```

Smoke test:

```bash
python3 -c "from Attacks import port_scan, brute_force_attempt, run_ddos_simulation; print(port_scan('127.0.0.1', max_ports=3))"
```

- **Acceptance:** All modules run only against allowed targets; CLI and programmatic use work; tests pass.
