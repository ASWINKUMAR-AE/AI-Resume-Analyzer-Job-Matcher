import json
from flask import Blueprint, request
from database.connection import get_db
from utils.response import api_response
from utils.auth_middleware import token_required, role_required
from ai.matcher import JobMatcher

applications_bp = Blueprint("applications", __name__, url_prefix="/api/applications")

@applications_bp.route("/jobs/<int:job_id>/apply", methods=["POST"])
@token_required
@role_required("student")
def apply_for_job(current_user, job_id):
    """
    Submits a job application for the student, calculates the live AI match score,
    and records the analysis snapshot in both applications and ai_analysis tables.
    """
    student_id = current_user["id"]
    data = request.get_json() or {}
    cover_note = data.get("cover_note", "")

    with get_db() as conn:
        with conn.cursor() as cursor:
            # 1. Verify Job exists and is active
            cursor.execute("SELECT * FROM jobs WHERE id = %s AND status = 'active'", (job_id,))
            job = cursor.fetchone()
            if not job:
                return api_response(success=False, message="Job posting not found or is no longer active.", status_code=404)

            # 2. Check if already applied
            cursor.execute("SELECT id, status FROM applications WHERE student_id = %s AND job_id = %s", (student_id, job_id))
            existing_app = cursor.fetchone()
            if existing_app:
                return api_response(
                    success=False,
                    message=f"You have already applied for this job. Current status: {existing_app['status']}.",
                    status_code=409
                )

            # 3. Get Student's Resume
            resume_id = data.get("resume_id")
            if resume_id:
                cursor.execute("SELECT * FROM resumes WHERE id = %s AND student_id = %s", (resume_id, student_id))
            else:
                cursor.execute("SELECT * FROM resumes WHERE student_id = %s ORDER BY created_at DESC LIMIT 1", (student_id,))
            resume = cursor.fetchone()

            if not resume:
                return api_response(
                    success=False,
                    message="Please upload your resume first before applying for this job.",
                    status_code=400
                )

            # 4. Fetch Skills & Profile for Match Scoring
            cursor.execute("SELECT skill_name, category FROM extracted_skills WHERE resume_id = %s", (resume["id"],))
            skills = cursor.fetchall()
            cursor.execute("SELECT * FROM student_profiles WHERE user_id = %s", (student_id,))
            profile = cursor.fetchone() or {}

            # 5. Compute AI Match Score
            match_res = JobMatcher.evaluate_match(
                resume_text=resume.get("raw_text", ""),
                resume_skills=skills,
                job_dict=job,
                candidate_profile=profile
            )

            # 6. Insert Application Record
            cursor.execute(
                """
                INSERT INTO applications (job_id, student_id, resume_id, match_score, status, cover_note)
                VALUES (%s, %s, %s, %s, 'Applied', %s)
                """,
                (job_id, student_id, resume["id"], match_res["match_score"], cover_note)
            )
            app_id = cursor.lastrowid

            # 7. Insert AI Analysis Snapshot
            cursor.execute(
                """
                INSERT INTO ai_analysis (
                    student_id, resume_id, job_id, match_score, matched_skills,
                    missing_skills, strengths, weaknesses, recommendations, score_breakdown
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    student_id,
                    resume["id"],
                    job_id,
                    match_res["match_score"],
                    json.dumps(match_res["matched_skills"]),
                    json.dumps(match_res["missing_skills"]),
                    json.dumps(match_res["strengths"]),
                    json.dumps(match_res["weaknesses"]),
                    json.dumps(match_res["recommendations"]),
                    json.dumps(match_res["score_breakdown"])
                )
            )

    return api_response(
        success=True,
        message="Application submitted successfully!",
        data={
            "application_id": app_id,
            "match_score": match_res["match_score"],
            "status": "Applied",
            "matched_skills": match_res["matched_skills"],
            "why_matched": match_res["why_matched_summary"]
        },
        status_code=201
    )

@applications_bp.route("/student", methods=["GET"])
@token_required
@role_required("student")
def get_student_applications(current_user):
    """
    Returns all job applications submitted by the logged-in student.
    """
    student_id = current_user["id"]
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT a.id, a.job_id, a.resume_id, a.match_score, a.status, a.applied_at, a.updated_at,
                       j.title AS job_title, j.location AS job_location, j.job_type, j.status AS job_status,
                       c.company_name, c.logo AS company_logo, r.file_name AS resume_file_name
                FROM applications a
                JOIN jobs j ON a.job_id = j.id
                JOIN company_profiles c ON j.company_id = c.user_id
                JOIN resumes r ON a.resume_id = r.id
                WHERE a.student_id = %s
                ORDER BY a.applied_at DESC
                """,
                (student_id,)
            )
            apps = cursor.fetchall()

    return api_response(success=True, data=apps)

@applications_bp.route("/company", methods=["GET"])
@token_required
@role_required("company", "admin")
def get_company_applications(current_user):
    """
    Returns applicants for jobs posted by the company with filtering, search,
    status filtering, and AI match ranking.
    """
    company_id = current_user["id"]
    job_id = request.args.get("job_id")
    status = request.args.get("status")
    search = request.args.get("q", "").strip()

    with get_db() as conn:
        with conn.cursor() as cursor:
            query = """
                SELECT a.id, a.job_id, a.student_id, a.resume_id, a.match_score, a.status,
                       a.applied_at, a.cover_note,
                       j.title AS job_title, j.job_type,
                       u.name AS candidate_name, u.email AS candidate_email,
                       sp.phone AS candidate_phone, sp.location AS candidate_location,
                       sp.college, sp.degree, sp.experience, sp.linkedin_url, sp.github_url,
                       r.file_name AS resume_file_name, r.resume_score
                FROM applications a
                JOIN jobs j ON a.job_id = j.id
                JOIN users u ON a.student_id = u.id
                LEFT JOIN student_profiles sp ON u.id = sp.user_id
                JOIN resumes r ON a.resume_id = r.id
                WHERE 1=1
            """
            params = []
            
            if current_user["role"] != "admin":
                query += " AND j.company_id = %s"
                params.append(company_id)

            if job_id:
                query += " AND a.job_id = %s"
                params.append(job_id)

            if status and status.lower() != "all":
                query += " AND a.status = %s"
                params.append(status)

            if search:
                query += " AND (u.name LIKE %s OR u.email LIKE %s OR j.title LIKE %s OR sp.degree LIKE %s)"
                term = f"%{search}%"
                params.extend([term, term, term, term])

            query += " ORDER BY a.match_score DESC, a.applied_at DESC"
            cursor.execute(query, tuple(params))
            applicants = cursor.fetchall()

    return api_response(success=True, data=applicants)

@applications_bp.route("/<int:app_id>", methods=["GET"])
@token_required
def get_application_detail(current_user, app_id):
    """
    Retrieves full details of a specific application including AI match breakdown.
    """
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT a.*, j.title AS job_title, j.company_id, j.description AS job_description,
                       j.skills AS job_skills, j.requirements AS job_requirements,
                       c.company_name, u.name AS candidate_name, u.email AS candidate_email,
                       sp.phone, sp.location, sp.college, sp.degree, sp.graduation_year,
                       sp.experience, sp.bio, sp.linkedin_url, sp.github_url,
                       r.file_name AS resume_file_name, r.file_path AS resume_file_path,
                       r.raw_text AS resume_text, r.resume_score
                FROM applications a
                JOIN jobs j ON a.job_id = j.id
                JOIN company_profiles c ON j.company_id = c.user_id
                JOIN users u ON a.student_id = u.id
                LEFT JOIN student_profiles sp ON u.id = sp.user_id
                JOIN resumes r ON a.resume_id = r.id
                WHERE a.id = %s
                """,
                (app_id,)
            )
            app = cursor.fetchone()

            if not app:
                return api_response(success=False, message="Application not found.", status_code=404)

            # Authorization Check
            role = current_user["role"]
            if role == "student" and app["student_id"] != current_user["id"]:
                return api_response(success=False, message="Access denied.", status_code=403)
            if role == "company" and app["company_id"] != current_user["id"]:
                return api_response(success=False, message="Access denied.", status_code=403)

            # Fetch AI Analysis snapshot
            cursor.execute(
                "SELECT * FROM ai_analysis WHERE student_id = %s AND job_id = %s ORDER BY created_at DESC LIMIT 1",
                (app["student_id"], app["job_id"])
            )
            analysis = cursor.fetchone()

            # Extracted Skills for the candidate
            cursor.execute(
                "SELECT skill_name, category FROM extracted_skills WHERE resume_id = %s",
                (app["resume_id"],)
            )
            candidate_skills = cursor.fetchall()

    if analysis:
        for fld in ["matched_skills", "missing_skills", "strengths", "weaknesses", "recommendations", "score_breakdown"]:
            if isinstance(analysis.get(fld), str):
                try:
                    analysis[fld] = json.loads(analysis[fld])
                except Exception:
                    pass
        app["ai_analysis"] = analysis
    else:
        app["ai_analysis"] = None

    app["candidate_skills"] = candidate_skills
    return api_response(success=True, data=app)

@applications_bp.route("/<int:app_id>/status", methods=["PUT"])
@token_required
@role_required("company", "admin")
def update_application_status(current_user, app_id):
    """
    Updates the hiring status of an application.
    Statuses: 'Applied', 'Under Review', 'Shortlisted', 'Interview', 'Selected', 'Rejected'
    """
    data = request.get_json() or {}
    new_status = data.get("status")
    allowed_statuses = ['Applied', 'Under Review', 'Shortlisted', 'Interview', 'Selected', 'Rejected']

    if new_status not in allowed_statuses:
        return api_response(
            success=False,
            message=f"Invalid status '{new_status}'. Allowed: {', '.join(allowed_statuses)}",
            status_code=400
        )

    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT a.id, j.company_id FROM applications a
                JOIN jobs j ON a.job_id = j.id
                WHERE a.id = %s
                """,
                (app_id,)
            )
            app = cursor.fetchone()
            if not app:
                return api_response(success=False, message="Application not found.", status_code=404)

            if current_user["role"] != "admin" and app["company_id"] != current_user["id"]:
                return api_response(success=False, message="Unauthorized to modify this application.", status_code=403)

            cursor.execute("UPDATE applications SET status = %s WHERE id = %s", (new_status, app_id))

    return api_response(
        success=True,
        message=f"Application status updated to '{new_status}' successfully.",
        data={"application_id": app_id, "new_status": new_status}
    )
