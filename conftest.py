"""Pytest path setup.

The modules in `scripts/` are dual-purpose: they run standalone as stdin/stdout
filters (`python scripts/compare_ads.py < ads.json`) and are imported as
`scripts.<module>` by the test suite. Standalone execution puts `scripts/` on
`sys.path` automatically, so the modules import their siblings by bare name.
Package-style imports do not, so add the directory here to keep both entry
points working.
"""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
