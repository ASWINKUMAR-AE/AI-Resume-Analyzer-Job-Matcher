from flask import Blueprint
from utils.response import api_response
from database.connection import check_db_health
from config import Config

health_bp = Blueprint("health", __name__, url_prefix="/api")

@health_bp.route("/health", methods=["GET"])
def health_check():
    """
    System Health Check endpoint reporting backend, database, and AI status.
    """
    db_ok = check_db_health()
    
    status_data = {
        "backend": "running",
        "database": "connected" if db_ok else "disconnected (check XAMPP MySQL)",
        "ai": "available",
        "mysql_host": f"{Config.DB_HOST}:{Config.DB_PORT}",
        "database_name": Config.DB_NAME,
        "features": {
            "tfidf_cosine_matcher": True,
            "skill_extractor": True,
            "resume_health_scorer": True,
            "ai_chat_assistant": True,
            "recommendation_engine": True
        }
    }

    status_code = 200 if db_ok else 503
    return api_response(
        success=db_ok,
        message="All systems operational" if db_ok else "Database connection failed. Please ensure MySQL is running in XAMPP.",
        data=status_data,
        status_code=status_code
    )
