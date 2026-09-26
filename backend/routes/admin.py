from flask import Blueprint, request
from database.connection import get_db
from utils.response import api_response
from utils.auth_middleware import token_required, role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

@admin_bp.route("/dashboard", methods=["GET"])
@token_required
@role_required("admin")
def get_admin_dashboard(current_user):
    """
    Returns platform-wide metrics and stats for admin dashboard.
    """
    with get_db() as conn:
        with conn.cursor() as cursor:
            # Users counts
            cursor.execute("SELECT COUNT(*) AS total_users FROM users")
            total_users = cursor.fetchone()["total_users"]

            cursor.execute("SELECT COUNT(*) AS total_students FROM users WHERE role = 'student'")
            total_students = cursor.fetchone()["total_students"]

            cursor.execute("SELECT COUNT(*) AS total_companies FROM users WHERE role = 'company'")
            total_companies = cursor.fetchone()["total_companies"]

            # Jobs counts
            cursor.execute("SELECT COUNT(*) AS total_jobs, SUM(CASE WHEN status='active' THEN 1 ELSE 0 END) AS active_jobs FROM jobs")
            job_stats = cursor.fetchone()

            # Applications counts
            cursor.execute("SELECT COUNT(*) AS total_applications, AVG(match_score) AS avg_match_score FROM applications")
            app_stats = cursor.fetchone()

            # Resumes & AI Analysis counts
            cursor.execute("SELECT COUNT(*) AS total_resumes, AVG(resume_score) AS avg_resume_score FROM resumes")
            resume_stats = cursor.fetchone()

            cursor.execute("SELECT COUNT(*) AS total_ai_analyses FROM ai_analysis")
            total_ai = cursor.fetchone()["total_ai_analyses"]

            # Recent Users
            cursor.execute("SELECT id, name, email, role, status, created_at FROM users ORDER BY created_at DESC LIMIT 5")
            recent_users = cursor.fetchall()

            # Recent Applications
            cursor.execute(
                """
                SELECT a.id, a.match_score, a.status, a.applied_at,
                       j.title AS job_title, c.company_name, u.name AS candidate_name
                FROM applications a
                JOIN jobs j ON a.job_id = j.id
                JOIN company_profiles c ON j.company_id = c.user_id
                JOIN users u ON a.student_id = u.id
                ORDER BY a.applied_at DESC
                LIMIT 5
                """
            )
            recent_apps = cursor.fetchall()

    return api_response(
        success=True,
        data={
            "stats": {
                "total_users": total_users,
                "total_students": total_students,
                "total_companies": total_companies,
                "total_jobs": job_stats["total_jobs"] or 0,
                "active_jobs": job_stats["active_jobs"] or 0,
                "total_applications": app_stats["total_applications"] or 0,
                "avg_match_score": round(float(app_stats["avg_match_score"] or 0), 1),
                "total_resumes": resume_stats["total_resumes"] or 0,
                "avg_resume_score": round(float(resume_stats["avg_resume_score"] or 0), 1),
                "total_ai_analyses": total_ai
            },
            "recent_users": recent_users,
            "recent_applications": recent_apps
        }
    )

@admin_bp.route("/users", methods=["GET"])
@token_required
@role_required("admin")
def get_admin_users(current_user):
    """
    Lists users with role and status filtering and search.
    """
    role = request.args.get("role")
    search = request.args.get("q", "").strip()

    with get_db() as conn:
        with conn.cursor() as cursor:
            query = "SELECT id, name, email, role, status, created_at, updated_at FROM users WHERE 1=1"
            params = []

            if role and role.lower() != "all":
                query += " AND role = %s"
                params.append(role)

            if search:
                query += " AND (name LIKE %s OR email LIKE %s)"
                params.extend([f"%{search}%", f"%{search}%"])

            query += " ORDER BY created_at DESC"
            cursor.execute(query, tuple(params))
            users = cursor.fetchall()

    return api_response(success=True, data=users)

@admin_bp.route("/users/<int:user_id>/status", methods=["PUT"])
@token_required
@role_required("admin")
def update_user_status(current_user, user_id):
    """
    Activates or deactivates a user account.
    """
    data = request.get_json() or {}
    new_status = data.get("status")
    if new_status not in ["active", "inactive", "pending"]:
        return api_response(success=False, message="Invalid status. Allowed: 'active', 'inactive', 'pending'", status_code=400)

    if user_id == current_user["id"]:
        return api_response(success=False, message="Admin cannot deactivate their own account.", status_code=400)

    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE users SET status = %s WHERE id = %s", (new_status, user_id))

    return api_response(success=True, message=f"User status updated to {new_status}.")

@admin_bp.route("/jobs", methods=["GET"])
@token_required
@role_required("admin")
def get_admin_jobs(current_user):
    """
    Lists all jobs on the platform.
    """
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT j.*, c.company_name, u.email AS company_email,
                       (SELECT COUNT(*) FROM applications a WHERE a.job_id = j.id) AS total_applicants
                FROM jobs j
                JOIN company_profiles c ON j.company_id = c.user_id
                JOIN users u ON j.company_id = u.id
                ORDER BY j.created_at DESC
                """
            )
            jobs = cursor.fetchall()

    return api_response(success=True, data=jobs)

@admin_bp.route("/jobs/<int:job_id>", methods=["DELETE"])
@token_required
@role_required("admin")
def delete_admin_job(current_user, job_id):
    """
    Moderates and deletes a job listing.
    """
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM jobs WHERE id = %s", (job_id,))

    return api_response(success=True, message="Job removed by administrator.")

@admin_bp.route("/applications", methods=["GET"])
@token_required
@role_required("admin")
def get_admin_applications(current_user):
    """
    Lists all job applications across the platform.
    """
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT a.id, a.match_score, a.status, a.applied_at,
                       j.title AS job_title, c.company_name,
                       u.name AS candidate_name, u.email AS candidate_email,
                       r.file_name AS resume_file_name, r.resume_score
                FROM applications a
                JOIN jobs j ON a.job_id = j.id
                JOIN company_profiles c ON j.company_id = c.user_id
                JOIN users u ON a.student_id = u.id
                JOIN resumes r ON a.resume_id = r.id
                ORDER BY a.applied_at DESC
                """
            )
            apps = cursor.fetchall()

    return api_response(success=True, data=apps)
