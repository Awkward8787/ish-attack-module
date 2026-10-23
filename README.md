<p align="center">
  <img src="assets/banner.png" alt="ish-attack-module" width="100%">
</p>

# ish-attack-module

**Educational CLI module for localhost-only demos of common network concepts (Alpine iSH friendly).**

[![License: All Rights Reserved](https://img.shields.io/badge/license-all%20rights%20reserved-lightgrey)](#license)
![Python](https://img.shields.io/badge/Python-3776AB&logo=python&logoColor=white)
![Educational](https://img.shields.io/badge/Educational-111111)

**Educational use only.** Operations are restricted to `127.0.0.1` / `localhost` (and `allowed_targets` in `config/settings.json`). Do not use against systems you do not own or have written permission to test.

## Features

- Interactive menu and subcommands for localhost-only demos
- Hard target allowlist (`127.0.0.1` / `localhost` + config)
- Caps on rates, ports, and durations
- pytest suite under `ish-attack-module/tests/`
- Designed to run in Alpine iSH on iOS without pip install

## Tech stack

- Python 3 (stdlib)
- Optional pytest

## How it works

```mermaid
flowchart LR
  student[Student on iSH / local Python] --> cli[CLI menu]
  cli --> guard[Target allowlist check]
  guard -->|localhost only| demo[Capped educational demo]
  guard -->|other host| refuse[Refuse]
  demo --> report[Local console report]
```

Every run checks the target against the allowlist before any demo starts. Non-localhost hosts are refused. Caps keep demos short and local.

## How to run

```bash
cd ish-attack-module
python3 main.py --help
```

See `python3 main.py --help` and `config/settings.json` for available educational demos and allowlisted targets. Use only on localhost.

## Status

Public. Educational / localhost-only. Not a general attack tool.

## License

All rights reserved. Educational use only.
