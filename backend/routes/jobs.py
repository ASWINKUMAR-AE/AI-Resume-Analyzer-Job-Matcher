from flask import Blueprint, request
from database.connection import get_db
from utils.response import api_response
from utils.auth_middleware import token_required, role_required, decode_token
from utils.validators import require_fields
from ai.matcher import JobMatcher

jobs_bp = Blueprint("jobs", __name__, url_prefix="/api/jobs")

def get_optional_current_user():
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        return decode_token(token)
    return None

@jobs_bp.route("", methods=["GET"])
def get_jobs():
    """
    List and filter all active jobs with search, company details,
    and optional AI match scores for logged-in students.
    """
    search = request.args.get("q", "").strip()
    location = request.args.get("location", "").strip()
    job_type = request.args.get("job_type", "").strip()
    company_id = request.args.get("company_id")
    status = request.args.get("status", "active")
    
    current_user = get_optional_current_user()
    student_id = current_user["user_id"] if current_user and current_user.get("role") == "student" else None

    # Load student resume & skills for live matching if student is logged in
    student_resume_text = ""
    student_skills = []
    student_profile = {}
    
    if student_id:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM student_profiles WHERE user_id = %s", (student_id,))
                student_profile = cursor.fetchone() or {}
                cursor.execute(
                    "SELECT id, raw_text FROM resumes WHERE student_id = %s ORDER BY created_at DESC LIMIT 1",
                    (student_id,)
                )
                res = cursor.fetchone()
                if res:
                    student_resume_text = res.get("raw_text", "")
                    cursor.execute(
                        "SELECT skill_name, category FROM extracted_skills WHERE resume_id = %s",
                        (res["id"],)
                    )
                    student_skills = cursor.fetchall()

    with get_db() as conn:
        with conn.cursor() as cursor:
            query = """
                SELECT j.*, c.company_name, c.logo AS company_logo, c.location AS company_location,
                       c.industry AS company_industry,
                       (SELECT COUNT(*) FROM applications a WHERE a.job_id = j.id) AS total_applicants
            """
            if student_id:
                query += f""",
                    (SELECT COUNT(*) FROM saved_jobs sj WHERE sj.job_id = j.id AND sj.student_id = {student_id}) AS is_saved,
                    (SELECT app.status FROM applications app WHERE app.job_id = j.id AND app.student_id = {student_id} LIMIT 1) AS applied_status
                """
            else:
                query += ", 0 AS is_saved, NULL AS applied_status"
                
            query += " FROM jobs j JOIN company_profiles c ON j.company_id = c.user_id WHERE 1=1"
            params = []

            # If company user looking for their own jobs, allow viewing all statuses
            if company_id:
                query += " AND j.company_id = %s"
                params.append(company_id)
            elif status:
                query += " AND j.status = %s"
                params.append(status)

            if search:
                query += " AND (j.title LIKE %s OR j.description LIKE %s OR j.skills LIKE %s OR c.company_name LIKE %s)"
                term = f"%{search}%"
                params.extend([term, term, term, term])

            if location:
                query += " AND (j.location LIKE %s OR c.location LIKE %s)"
                loc_term = f"%{location}%"
                params.extend([loc_term, loc_term])

            if job_type and job_type.lower() != "all":
                query += " AND j.job_type = %s"
                params.append(job_type)

            query += " ORDER BY j.created_at DESC"
            cursor.execute(query, tuple(params))
            jobs = cursor.fetchall()

    # Calculate AI Match score for each job if student has a resume
    for job in jobs:
        job["is_saved"] = bool(job.get("is_saved"))
        if student_id and student_resume_text:
            match_res = JobMatcher.evaluate_match(
                resume_text=student_resume_text,
                resume_skills=student_skills,
                job_dict=job,
                candidate_profile=student_profile
            )
            job["match_score"] = match_res["match_score"]
            job["matched_skills"] = match_res["matched_skills"]
            job["missing_skills"] = match_res["missing_skills"]
            job["why_matched"] = match_res["why_matched_summary"]
        else:
            job["match_score"] = None
            job["matched_skills"] = []
            job["missing_skills"] = []
            job["why_matched"] = ""

    # If sorted by match
    sort_by = request.args.get("sort", "newest")
    if sort_by == "match" and student_id:
        jobs.sort(key=lambda x: x["match_score"] or 0, reverse=True)

    return api_response(success=True, data=jobs)

@jobs_bp.route("/<int:job_id>", methods=["GET"])
def get_job_detail(job_id):
    """
    Returns single job details with company info and candidate AI match breakdown.
    """
    current_user = get_optional_current_user()
    student_id = current_user["user_id"] if current_user and current_user.get("role") == "student" else None

    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT j.*, c.company_name, c.company_email, c.website, c.industry,
                       c.location AS company_location, c.description AS company_description,
                       c.logo AS company_logo, c.verified AS company_verified,
                       (SELECT COUNT(*) FROM applications a WHERE a.job_id = j.id) AS total_applicants
                FROM jobs j
                JOIN company_profiles c ON j.company_id = c.user_id
                WHERE j.id = %s
                """,
                (job_id,)
            )
            job = cursor.fetchone()

    if not job:
        return api_response(success=False, message="Job not found.", status_code=404)

    # Check student application/save status and compute detailed AI match
    ai_evaluation = None
    is_saved = False
    applied_status = None

    if student_id:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM saved_jobs WHERE student_id = %s AND job_id = %s", (student_id, job_id))
                is_saved = bool(cursor.fetchone())

                cursor.execute("SELECT id, status, applied_at, match_score FROM applications WHERE student_id = %s AND job_id = %s", (student_id, job_id))
                app = cursor.fetchone()
                if app:
                    applied_status = app["status"]

                cursor.execute("SELECT * FROM student_profiles WHERE user_id = %s", (student_id,))
                profile = cursor.fetchone() or {}

                cursor.execute("SELECT id, raw_text FROM resumes WHERE student_id = %s ORDER BY created_at DESC LIMIT 1", (student_id,))
                resume = cursor.fetchone()
                if resume:
                    cursor.execute("SELECT skill_name, category FROM extracted_skills WHERE resume_id = %s", (resume["id"],))
                    skills = cursor.fetchall()
                    ai_evaluation = JobMatcher.evaluate_match(
                        resume_text=resume.get("raw_text", ""),
                        resume_skills=skills,
                        job_dict=job,
                        candidate_profile=profile
                    )

    job["is_saved"] = is_saved
    job["applied_status"] = applied_status
    job["ai_evaluation"] = ai_evaluation

    return api_response(success=True, data=job)

@jobs_bp.route("", methods=["POST"])
@token_required
@role_required("company", "admin")
def create_job(current_user):
    """
    Creates a new job post.
    """
    data = request.get_json() or {}
    valid, err = require_fields(data, ["title", "description", "job_type"])
    if not valid:
        return api_response(success=False, message=err, status_code=400)

    company_id = current_user["id"]

    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO jobs (
                    company_id, title, description, requirements, skills, preferred_skills,
                    location, job_type, experience_required, salary_min, salary_max,
                    application_deadline, status
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    company_id,
                    data["title"].strip(),
                    data["description"].strip(),
                    data.get("requirements", "").strip(),
                    data.get("skills", "").strip(),
                    data.get("preferred_skills", "").strip(),
                    data.get("location", "Remote").strip(),
                    data.get("job_type", "Full Time"),
                    data.get("experience_required", "1-3 years"),
                    data.get("salary_min") or None,
                    data.get("salary_max") or None,
                    data.get("application_deadline") or None,
                    data.get("status", "active")
                )
            )
            job_id = cursor.lastrowid

    return api_response(
        success=True,
        message="Job posted successfully!",
        data={"job_id": job_id},
        status_code=201
    )

@jobs_bp.route("/<int:job_id>", methods=["PUT"])
@token_required
@role_required("company", "admin")
def update_job(current_user, job_id):
    """
    Updates an existing job posting.
    """
    data = request.get_json() or {}
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT company_id FROM jobs WHERE id = %s", (job_id,))
            job = cursor.fetchone()
            if not job:
                return api_response(success=False, message="Job not found.", status_code=404)

            if current_user["role"] != "admin" and job["company_id"] != current_user["id"]:
                return api_response(success=False, message="Unauthorized to modify this job.", status_code=403)

            cursor.execute(
                """
                UPDATE jobs SET
                    title = %s,
                    description = %s,
                    requirements = %s,
                    skills = %s,
                    preferred_skills = %s,
                    location = %s,
                    job_type = %s,
                    experience_required = %s,
                    salary_min = %s,
                    salary_max = %s,
                    application_deadline = %s,
                    status = %s
                WHERE id = %s
                """,
                (
                    data.get("title", "").strip(),
                    data.get("description", "").strip(),
                    data.get("requirements", "").strip(),
                    data.get("skills", "").strip(),
                    data.get("preferred_skills", "").strip(),
                    data.get("location", "").strip(),
                    data.get("job_type", "Full Time"),
                    data.get("experience_required", ""),
                    data.get("salary_min") or None,
                    data.get("salary_max") or None,
                    data.get("application_deadline") or None,
                    data.get("status", "active"),
                    job_id
                )
            )

    return api_response(success=True, message="Job updated successfully.")

@jobs_bp.route("/<int:job_id>", methods=["DELETE"])
@token_required
@role_required("company", "admin")
def delete_job(current_user, job_id):
    """
    Deletes a job listing.
    """
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT company_id FROM jobs WHERE id = %s", (job_id,))
            job = cursor.fetchone()
            if not job:
                return api_response(success=False, message="Job not found.", status_code=404)

            if current_user["role"] != "admin" and job["company_id"] != current_user["id"]:
                return api_response(success=False, message="Unauthorized to delete this job.", status_code=403)

            cursor.execute("DELETE FROM jobs WHERE id = %s", (job_id,))

    return api_response(success=True, message="Job deleted successfully.")
