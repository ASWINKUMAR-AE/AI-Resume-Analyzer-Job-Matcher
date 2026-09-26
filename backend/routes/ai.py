from flask import Blueprint, request
from database.connection import get_db
from utils.response import api_response
from utils.auth_middleware import token_required, role_required
from ai.recommender import JobRecommender
from ai.matcher import JobMatcher
from ai.assistant import AIAssistant

ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")

@ai_bp.route("/recommendations", methods=["GET"])
@token_required
@role_required("student")
def get_job_recommendations(current_user):
    """
    Returns AI ranked and matched job recommendations for the logged-in student.
    """
    limit = int(request.args.get("limit", "10"))
    try:
        recommendations = JobRecommender.get_recommendations_for_student(current_user["id"], limit=limit)
        return api_response(success=True, data=recommendations)
    except Exception as e:
        return api_response(success=False, message=f"Failed to compute recommendations: {str(e)}", status_code=500)

@ai_bp.route("/match-preview", methods=["POST"])
@token_required
def match_preview(current_user):
    """
    Computes an on-demand, instant explainable AI match score between a candidate's resume and a job.
    """
    data = request.get_json() or {}
    job_id = data.get("job_id")
    if not job_id:
        return api_response(success=False, message="job_id is required.", status_code=400)

    student_id = data.get("student_id") if current_user["role"] in ["company", "admin"] and data.get("student_id") else current_user["id"]

    with get_db() as conn:
        with conn.cursor() as cursor:
            # Fetch Job
            cursor.execute(
                """
                SELECT j.*, c.company_name FROM jobs j
                JOIN company_profiles c ON j.company_id = c.user_id
                WHERE j.id = %s
                """,
                (job_id,)
            )
            job = cursor.fetchone()
            if not job:
                return api_response(success=False, message="Job not found.", status_code=404)

            # Fetch Student Resume & Skills
            cursor.execute("SELECT * FROM resumes WHERE student_id = %s ORDER BY created_at DESC LIMIT 1", (student_id,))
            resume = cursor.fetchone()
            if not resume:
                return api_response(success=False, message="No resume found for candidate.", status_code=404)

            cursor.execute("SELECT skill_name, category FROM extracted_skills WHERE resume_id = %s", (resume["id"],))
            skills = cursor.fetchall()

            cursor.execute("SELECT * FROM student_profiles WHERE user_id = %s", (student_id,))
            profile = cursor.fetchone() or {}

    match_result = JobMatcher.evaluate_match(
        resume_text=resume.get("raw_text", ""),
        resume_skills=skills,
        job_dict=job,
        candidate_profile=profile
    )

    return api_response(success=True, data=match_result)

@ai_bp.route("/chat", methods=["POST"])
@token_required
@role_required("student")
def chat_assistant(current_user):
    """
    Grounded AI Career Assistant endpoint.
    Accepts student prompt and optional target job_id, returning tailored guidance.
    """
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    job_id = data.get("job_id")

    if not message:
        return api_response(success=False, message="Message is required.", status_code=400)

    try:
        reply = AIAssistant.chat(current_user["id"], message, job_id=job_id)
        return api_response(
            success=True,
            data={
                "reply": reply,
                "user_message": message
            }
        )
    except Exception as e:
        return api_response(success=False, message=f"Assistant error: {str(e)}", status_code=500)
