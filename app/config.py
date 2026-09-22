"""
Config

Central application settings, overridable with environment variables.

@author adrianpmdev
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = Path(os.getenv("DB_PATH", BASE_DIR / "data" / "click_reports.db"))
SAMPLE_CLICKS = int(os.getenv("SAMPLE_CLICKS", "500"))
SAMPLE_DAYS = int(os.getenv("SAMPLE_DAYS", "30"))
