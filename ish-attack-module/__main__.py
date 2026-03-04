# Run ish-attack-module CLI. EDUCATIONAL USE ONLY.
# From inside ish-attack-module: python main.py [port-scan|brute-force|ddos] [options]
# Or: python -m main
import sys
import os

_here = os.path.dirname(os.path.abspath(__file__))
if _here not in sys.path:
    sys.path.insert(0, _here)

from main import main
sys.exit(main())
