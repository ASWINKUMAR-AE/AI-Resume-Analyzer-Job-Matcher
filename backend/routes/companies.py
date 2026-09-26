from flask import Blueprint, request
from database.connection import get_db
from utils.response import api_response
from utils.auth_middleware import token_required, role_required

companies_bp = Blueprint("companies", __name__, url_prefix="/api/company")

@companies_bp.route("/profile", methods=["GET"])
@token_required
@role_required("company", "admin")
def get_company_profile(current_user):
    """
    Returns company profile details.
    """
    company_id = request.args.get("company_id") if current_user["role"] == "admin" and request.args.get("company_id") else current_user["id"]
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT u.id, u.name, u.email, u.role, u.status, u.created_at,
                       cp.company_name, cp.company_email, cp.phone, cp.website,
                       cp.industry, cp.location, cp.description, cp.logo, cp.verified
                FROM users u
                LEFT JOIN company_profiles cp ON u.id = cp.user_id
                WHERE u.id = %s
                """,
                (company_id,)
            )
            profile = cursor.fetchone()

    if not profile:
        return api_response(success=False, message="Company profile not found.", status_code=404)

    return api_response(success=True, data=profile)

@companies_bp.route("/profile", methods=["PUT"])
@token_required
@role_required("company")
def update_company_profile(current_user):
    """
    Updates company profile details.
    """
    data = request.get_json() or {}
    user_id = current_user["id"]

    with get_db() as conn:
        with conn.cursor() as cursor:
            if data.get("company_name"):
                cursor.execute("UPDATE users SET name = %s WHERE id = %s", (data["company_name"].strip(), user_id))

            cursor.execute(
                """
                UPDATE company_profiles SET
                    company_name = %s,
                    company_email = %s,
                    phone = %s,
                    website = %s,
                    industry = %s,
                    location = %s,
                    description = %s,
                    logo = %s
                WHERE user_id = %s
                """,
                (
                    data.get("company_name", current_user["name"]),
                    data.get("company_email", current_user["email"]),
                    data.get("phone", ""),
                    data.get("website", ""),
                    data.get("industry", ""),
                    data.get("location", ""),
                    data.get("description", ""),
                    data.get("logo", ""),
                    user_id
                )
            )

    return api_response(success=True, message="Company profile updated successfully.")

@companies_bp.route("/dashboard", methods=["GET"])
@token_required
@role_required("company")
def get_company_dashboard(current_user):
    """
    Returns dashboard statistics, jobs list, and recent applications for the company.
    """
    user_id = current_user["id"]
    with get_db() as conn:
        with conn.cursor() as cursor:
            # 1. Jobs Counts
            cursor.execute(
                """
                SELECT 
                    COUNT(*) AS total_jobs,
                    SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) AS active_jobs,
                    SUM(CASE WHEN status = 'closed' THEN 1 ELSE 0 END) AS closed_jobs
                FROM jobs WHERE company_id = %s
                """,
                (user_id,)
            )
            job_stats = cursor.fetchone()

            # 2. Applications Counts & Status Breakdown
            cursor.execute(
                """
                SELECT 
                    COUNT(a.id) AS total_applications,
                    SUM(CASE WHEN a.status = 'Applied' THEN 1 ELSE 0 END) AS applied_count,
                    SUM(CASE WHEN a.status = 'Under Review' THEN 1 ELSE 0 END) AS under_review_count,
                    SUM(CASE WHEN a.status = 'Shortlisted' THEN 1 ELSE 0 END) AS shortlisted_count,
                    SUM(CASE WHEN a.status = 'Interview' THEN 1 ELSE 0 END) AS interview_count,
                    SUM(CASE WHEN a.status = 'Selected' THEN 1 ELSE 0 END) AS selected_count,
                    SUM(CASE WHEN a.status = 'Rejected' THEN 1 ELSE 0 END) AS rejected_count,
                    AVG(a.match_score) AS avg_match_score
                FROM applications a
                JOIN jobs j ON a.job_id = j.id
                WHERE j.company_id = %s
                """,
                (user_id,)
            )
            app_stats = cursor.fetchone()

            # 3. Recent Applications
            cursor.execute(
                """
                SELECT a.id, a.job_id, a.student_id, a.match_score, a.status, a.applied_at,
                       j.title AS job_title, u.name AS candidate_name, u.email AS candidate_email,
                       sp.college, sp.degree, sp.experience, sp.location
                FROM applications a
                JOIN jobs j ON a.job_id = j.id
                JOIN users u ON a.student_id = u.id
                LEFT JOIN student_profiles sp ON u.id = sp.user_id
                WHERE j.company_id = %s
                ORDER BY a.applied_at DESC
                LIMIT 8
                """,
                (user_id,)
            )
            recent_apps = cursor.fetchall()

            # 4. Applications by Job for Charts
            cursor.execute(
                """
                SELECT j.id, j.title, COUNT(a.id) AS applicant_count, AVG(a.match_score) AS avg_score
                FROM jobs j
                LEFT JOIN applications a ON j.id = a.job_id
                WHERE j.company_id = %s
                GROUP BY j.id, j.title
                ORDER BY applicant_count DESC
                LIMIT 6
                """,
                (user_id,)
            )
            apps_by_job = cursor.fetchall()

    return api_response(
        success=True,
        data={
            "stats": {
                "total_jobs": job_stats["total_jobs"] or 0,
                "active_jobs": job_stats["active_jobs"] or 0,
                "closed_jobs": job_stats["closed_jobs"] or 0,
                "total_applications": app_stats["total_applications"] or 0,
                "shortlisted": app_stats["shortlisted_count"] or 0,
                "interviews": app_stats["interview_count"] or 0,
                "selected": app_stats["selected_count"] or 0,
                "under_review": app_stats["under_review_count"] or 0,
                "avg_match_score": round(float(app_stats["avg_match_score"] or 0), 1)
            },
            "recent_applications": recent_apps,
            "apps_by_job": apps_by_job
        }
    )
