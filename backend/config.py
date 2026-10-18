import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BACKEND_DIR / "data" / "uploads"
PROCESSED_DIR = BACKEND_DIR / "data" / "processed"
OUTPUT_DIR = BACKEND_DIR / "data" / "outputs"

# Ensure data directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load .env file if available
load_dotenv(BASE_DIR / ".env")

class Settings(BaseModel):
    APP_NAME: str = "ParallaxFlow OCR - Production Handwriting Engine"
    API_PREFIX: str = "/api"
    DEFAULT_ENGINE: str = "gemini"  # "gemini" or "easyocr"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "")
    DEFAULT_GEMINI_MODEL: str = "gemini-3.5-flash-lite"
    MAX_CONCURRENT_PAGES: int = 4
    RENDER_DPI: int = 300

settings = Settings()
