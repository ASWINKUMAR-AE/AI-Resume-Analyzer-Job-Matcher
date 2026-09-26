from flask import Blueprint, request
from database.connection import get_db
from utils.response import api_response
from utils.auth_middleware import token_required, role_required
from ai.recommender import JobRecommender

students_bp = Blueprint("students", __name__, url_prefix="/api/student")

@students_bp.route("/profile", methods=["GET"])
@token_required
@role_required("student", "admin")
def get_student_profile(current_user):
    """
    Returns student profile details.
    """
    user_id = request.args.get("user_id") if current_user["role"] == "admin" and request.args.get("user_id") else current_user["id"]
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT u.id, u.name, u.email, u.role, u.status, u.created_at,
                       sp.phone, sp.location, sp.education, sp.college, sp.degree,
                       sp.graduation_year, sp.experience, sp.bio, sp.linkedin_url,
                       sp.github_url, sp.portfolio_url, sp.profile_image
                FROM users u
                LEFT JOIN student_profiles sp ON u.id = sp.user_id
                WHERE u.id = %s
                """,
                (user_id,)
            )
            profile = cursor.fetchone()

    if not profile:
        return api_response(success=False, message="Student profile not found.", status_code=404)

    return api_response(success=True, data=profile)

@students_bp.route("/profile", methods=["PUT"])
@token_required
@role_required("student")
def update_student_profile(current_user):
    """
    Updates student profile information.
    """
    data = request.get_json() or {}
    user_id = current_user["id"]

    with get_db() as conn:
        with conn.cursor() as cursor:
            # Update user name if provided
            if data.get("name"):
                cursor.execute("UPDATE users SET name = %s WHERE id = %s", (data["name"].strip(), user_id))

            # Update student profile
            cursor.execute(
                """
                UPDATE student_profiles SET
                    phone = %s,
                    location = %s,
                    education = %s,
                    college = %s,
                    degree = %s,
                    graduation_year = %s,
                    experience = %s,
                    bio = %s,
                    linkedin_url = %s,
                    github_url = %s,
                    portfolio_url = %s
                WHERE user_id = %s
                """,
                (
                    data.get("phone", ""),
                    data.get("location", ""),
                    data.get("education", ""),
                    data.get("college", ""),
                    data.get("degree", ""),
                    data.get("graduation_year") or None,
                    data.get("experience", ""),
                    data.get("bio", ""),
                    data.get("linkedin_url", ""),
                    data.get("github_url", ""),
                    data.get("portfolio_url", ""),
                    user_id
                )
            )

    return api_response(success=True, message="Profile updated successfully.")

@students_bp.route("/dashboard", methods=["GET"])
@token_required
@role_required("student")
def get_student_dashboard(current_user):
    """
    Aggregates full statistics for the student dashboard.
    """
    user_id = current_user["id"]
    with get_db() as conn:
        with conn.cursor() as cursor:
            # 1. Latest Resume
            cursor.execute(
                """
                SELECT id, file_name, resume_score, created_at
                FROM resumes WHERE student_id = %s
                ORDER BY created_at DESC LIMIT 1
                """,
                (user_id,)
            )
            resume = cursor.fetchone()

            # 2. Extracted Skills Count & Categories
            skills = []
            if resume:
                cursor.execute(
                    "SELECT skill_name, category, confidence FROM extracted_skills WHERE resume_id = %s",
                    (resume["id"],)
                )
                skills = cursor.fetchall()

            # 3. Application Stats
            cursor.execute(
                """
                SELECT 
                    COUNT(*) AS total_applied,
                    SUM(CASE WHEN status = 'Shortlisted' THEN 1 ELSE 0 END) AS shortlisted_count,
                    SUM(CASE WHEN status = 'Interview' THEN 1 ELSE 0 END) AS interview_count,
                    SUM(CASE WHEN status = 'Selected' THEN 1 ELSE 0 END) AS selected_count,
                    SUM(CASE WHEN status = 'Under Review' THEN 1 ELSE 0 END) AS under_review_count
                FROM applications WHERE student_id = %s
                """,
                (user_id,)
            )
            app_stats = cursor.fetchone()

            # 4. Saved Jobs Count
            cursor.execute("SELECT COUNT(*) AS saved_count FROM saved_jobs WHERE student_id = %s", (user_id,))
            saved_count = cursor.fetchone()["saved_count"]

    # 5. Top Recommended Jobs
    try:
        recommended_jobs = JobRecommender.get_recommendations_for_student(user_id, limit=4)
    except Exception:
        recommended_jobs = []

    return api_response(
        success=True,
        data={
            "user": current_user,
            "resume": resume,
            "resume_score": resume.get("resume_score", 0) if resume else 0,
            "skills": skills,
            "skills_count": len(skills),
            "stats": {
                "total_applied": app_stats["total_applied"] or 0,
                "shortlisted": app_stats["shortlisted_count"] or 0,
                "interview": app_stats["interview_count"] or 0,
                "selected": app_stats["selected_count"] or 0,
                "under_review": app_stats["under_review_count"] or 0,
                "saved_jobs": saved_count
            },
            "recommended_jobs": recommended_jobs
        }
    )

@students_bp.route("/skills", methods=["GET"])
@token_required
@role_required("student")
def get_student_skills(current_user):
    """
    Returns all detected skills categorized for the student's latest resume.
    """
    user_id = current_user["id"]
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM resumes WHERE student_id = %s ORDER BY created_at DESC LIMIT 1",
                (user_id,)
            )
            resume = cursor.fetchone()
            if not resume:
                return api_response(success=True, data={"skills": [], "categories": {}})

            cursor.execute(
                "SELECT skill_name, category, confidence FROM extracted_skills WHERE resume_id = %s ORDER BY category, skill_name",
                (resume["id"],)
            )
            skills = cursor.fetchall()

    # Group by category
    categories = {}
    for s in skills:
        cat = s.get("category", "General")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(s)

    return api_response(
        success=True,
        data={
            "skills": skills,
            "total_count": len(skills),
            "categories": categories
        }
    )

@students_bp.route("/saved-jobs", methods=["GET"])
@token_required
@role_required("student")
def get_saved_jobs(current_user):
    """
    Returns list of saved/bookmarked jobs for the student.
    """
    user_id = current_user["id"]
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT j.*, c.company_name, c.logo AS company_logo, c.location AS company_location,
                       sj.created_at AS saved_at
                FROM saved_jobs sj
                JOIN jobs j ON sj.job_id = j.id
                JOIN company_profiles c ON j.company_id = c.user_id
                WHERE sj.student_id = %s
                ORDER BY sj.created_at DESC
                """,
                (user_id,)
            )
            jobs = cursor.fetchall()

    return api_response(success=True, data=jobs)

@students_bp.route("/saved-jobs/<int:job_id>", methods=["POST"])
@token_required
@role_required("student")
def toggle_save_job(current_user, job_id):
    """
    Toggles save/bookmark state for a job.
    """
    user_id = current_user["id"]
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM saved_jobs WHERE student_id = %s AND job_id = %s",
                (user_id, job_id)
            )
            existing = cursor.fetchone()
            if existing:
                cursor.execute(
                    "DELETE FROM saved_jobs WHERE student_id = %s AND job_id = %s",
                    (user_id, job_id)
                )
                return api_response(success=True, message="Job removed from saved jobs.", data={"is_saved": False})
            else:
                cursor.execute(
                    "INSERT INTO saved_jobs (student_id, job_id) VALUES (%s, %s)",
                    (user_id, job_id)
                )
                return api_response(success=True, message="Job bookmarked successfully!", data={"is_saved": True})
