import os
from pathlib import Path

from dotenv import load_dotenv

# Project root: hr_gatepass_agent/
BASE_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BASE_DIR / "uploads"
DATABASE_PATH = BASE_DIR / "checkpoints.sqlite"

load_dotenv(BASE_DIR / ".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
SARVAM_API_KEY=os.getenv("SARVAM_API_KEY")
SARVAM_MODEL=os.getenv("SARVAM_MODEL","sarvam-105b")

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
EXPECTED_PDF_COUNT = 2

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
