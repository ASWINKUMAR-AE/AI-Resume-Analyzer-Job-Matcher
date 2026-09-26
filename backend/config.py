import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask Settings
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-ai-resume-matcher-2026")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-ai-resume-matcher-key")
    JWT_ACCESS_TOKEN_EXPIRES_HOURS = int(os.getenv("JWT_EXPIRES_HOURS", "24"))
    
    # MySQL Database Settings (XAMPP default)
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_NAME = os.getenv("DB_NAME", "ai_resume_matcher")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    
    # Upload Settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads", "resumes")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10")) * 1024 * 1024  # 10MB default
    ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
    
    # AI & Match Settings
    AI_FALLBACK_LOCAL = True
    MIN_MATCH_SCORE_THRESHOLD = 20.0
    
    # External LLM / AI API (Optional)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
