import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from init_db import init_database
from utils.response import api_response

# Import Route Blueprints
from routes.auth import auth_bp
from routes.students import students_bp
from routes.companies import companies_bp
from routes.jobs import jobs_bp
from routes.resumes import resumes_bp
from routes.applications import applications_bp
from routes.ai import ai_bp
from routes.admin import admin_bp
from routes.health import health_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for frontend clients
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Register Blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(companies_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(resumes_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(admin_bp)

    # Global Error Handlers
    @app.errorhandler(404)
    def handle_404(e):
        return api_response(success=False, message="The requested API endpoint was not found.", status_code=404)

    @app.errorhandler(405)
    def handle_405(e):
        return api_response(success=False, message="Method Not Allowed for this endpoint.", status_code=405)

    @app.errorhandler(413)
    def handle_413(e):
        return api_response(success=False, message="Uploaded file exceeds maximum allowed size (10MB).", status_code=413)

    @app.errorhandler(Exception)
    def handle_global_exception(e):
        # Prevent exposing raw internal trace in production while giving meaningful error
        return api_response(
            success=False,
            message="An unexpected server error occurred. Please try again.",
            error=str(e),
            status_code=500
        )

    return app

# Ensure database is verified/initialized on application bootstrap
try:
    init_database(seed_demo=False)
except Exception as e:
    print(f"[!] Warning during DB startup check: {e}")

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"[*] Starting AI Resume Analyzer & Job Matcher Backend on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
