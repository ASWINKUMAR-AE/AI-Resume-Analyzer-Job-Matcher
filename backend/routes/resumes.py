import os
import json
from flask import Blueprint, request, send_file
from database.connection import get_db
from utils.response import api_response
from utils.auth_middleware import token_required, role_required
from utils.file_handler import save_uploaded_file, allowed_file
from ai.parser import ResumeParser
from ai.skill_extractor import SkillExtractor
from ai.resume_scorer import ResumeScorer

resumes_bp = Blueprint("resumes", __name__, url_prefix="/api/resume")

@resumes_bp.route("/upload", methods=["POST"])
@token_required
@role_required("student")
def upload_resume(current_user):
    """
    Handles resume file upload (PDF/DOCX/TXT), performs text extraction,
    section parsing, skill extraction, and ATS health scoring.
    """
    if "resume" not in request.files:
        return api_response(success=False, message="No resume file found in form data (key must be 'resume').", status_code=400)

    file_obj = request.files["resume"]
    if not file_obj or file_obj.filename == "":
        return api_response(success=False, message="No selected file.", status_code=400)

    if not allowed_file(file_obj.filename):
        return api_response(success=False, message="Unsupported file format. Please upload a PDF, DOCX, or TXT resume.", status_code=400)

    student_id = current_user["id"]

    try:
        # 1. Save file safely
        orig_name, file_path, file_type = save_uploaded_file(file_obj, student_id)

        # 2. Extract text
        raw_text = ResumeParser.extract_text(file_path, file_type)
        if not raw_text or len(raw_text.strip()) < 20:
            return api_response(
                success=False,
                message="Unable to extract meaningful text from resume. Ensure the file is not an unsearchable image scan.",
                status_code=422
            )

        # 3. Detect Sections & Contact Information
        sections = ResumeParser.detect_sections(raw_text)
        contact_info = ResumeParser.extract_contact_info(raw_text)
        edu_info = ResumeParser.extract_education_details(sections.get("education", ""), raw_text)
        exp_years = ResumeParser.extract_experience_years(sections.get("experience", ""), raw_text)

        # 4. Extract Skills
        extracted_skills = SkillExtractor.extract_skills(raw_text, sections)

        # 5. Score Resume & Generate Improvement Audit
        score_data = ResumeScorer.score_resume(raw_text, sections, extracted_skills, contact_info)

        # 6. Store in MySQL Database
        with get_db() as conn:
            with conn.cursor() as cursor:
                # Insert Resume Record
                cursor.execute(
                    """
                    INSERT INTO resumes (
                        student_id, file_name, file_path, file_type, raw_text,
                        parsed_sections, resume_score, strengths, weaknesses, recommendations
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        student_id,
                        orig_name,
                        file_path,
                        file_type,
                        raw_text,
                        json.dumps(sections),
                        score_data["resume_score"],
                        json.dumps(score_data["strengths"]),
                        json.dumps(score_data["weaknesses"]),
                        json.dumps(score_data["recommendations"])
                    )
                )
                resume_id = cursor.lastrowid

                # Insert Extracted Skills
                for sk in extracted_skills:
                    cursor.execute(
                        """
                        INSERT INTO extracted_skills (resume_id, skill_name, category, confidence)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (resume_id, sk["skill_name"], sk["category"], sk["confidence"])
                    )

                # Auto-update student profile with detected contact details if currently empty
                cursor.execute("SELECT * FROM student_profiles WHERE user_id = %s", (student_id,))
                prof = cursor.fetchone()
                if prof:
                    phone_to_update = contact_info["phone"] if not prof.get("phone") and contact_info["phone"] else prof.get("phone")
                    linkedin_to_update = contact_info["linkedin_url"] if not prof.get("linkedin_url") and contact_info["linkedin_url"] else prof.get("linkedin_url")
                    github_to_update = contact_info["github_url"] if not prof.get("github_url") and contact_info["github_url"] else prof.get("github_url")
                    degree_to_update = edu_info["degree"] if not prof.get("degree") else prof.get("degree")
                    grad_to_update = edu_info["graduation_year"] if not prof.get("graduation_year") else prof.get("graduation_year")

                    cursor.execute(
                        """
                        UPDATE student_profiles SET
                            phone = %s, linkedin_url = %s, github_url = %s, degree = %s, graduation_year = %s
                        WHERE user_id = %s
                        """,
                        (phone_to_update, linkedin_to_update, github_to_update, degree_to_update, grad_to_update, student_id)
                    )

        return api_response(
            success=True,
            message="Resume analyzed successfully!",
            data={
                "resume_id": resume_id,
                "file_name": orig_name,
                "resume_score": score_data["resume_score"],
                "score_breakdown": score_data["breakdown"],
                "strengths": score_data["strengths"],
                "weaknesses": score_data["weaknesses"],
                "recommendations": score_data["recommendations"],
                "warnings": score_data["warnings"],
                "suggestions": score_data["suggestions"],
                "skills_count": len(extracted_skills),
                "skills": extracted_skills,
                "sections": sections
            },
            status_code=201
        )

    except Exception as e:
        return api_response(success=False, message=f"Resume processing failed: {str(e)}", status_code=500)

@resumes_bp.route("", methods=["GET"])
@token_required
def get_latest_resume(current_user):
    """
    Returns latest parsed resume, skills, sections, and score for current student.
    """
    student_id = request.args.get("student_id") if current_user["role"] in ["company", "admin"] and request.args.get("student_id") else current_user["id"]
    
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, student_id, file_name, file_type, resume_score,
                       parsed_sections, strengths, weaknesses, recommendations, created_at
                FROM resumes
                WHERE student_id = %s
                ORDER BY created_at DESC LIMIT 1
                """,
                (student_id,)
            )
            resume = cursor.fetchone()

            if not resume:
                return api_response(success=True, data=None, message="No resume uploaded yet.")

            cursor.execute(
                "SELECT skill_name, category, confidence FROM extracted_skills WHERE resume_id = %s ORDER BY category, skill_name",
                (resume["id"],)
            )
            skills = cursor.fetchall()

    # Parse JSON fields safely
    for json_field in ["parsed_sections", "strengths", "weaknesses", "recommendations"]:
        val = resume.get(json_field)
        if isinstance(val, str):
            try:
                resume[json_field] = json.loads(val)
            except Exception:
                resume[json_field] = []

    resume["skills"] = skills
    return api_response(success=True, data=resume)

@resumes_bp.route("/download/<int:resume_id>", methods=["GET"])
@token_required
def download_resume(current_user, resume_id):
    """
    Secure file download. Students can download their own resume; companies can download applicants.
    """
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM resumes WHERE id = %s", (resume_id,))
            resume = cursor.fetchone()

    if not resume:
        return api_response(success=False, message="Resume not found.", status_code=404)

    # Permission check: Student owner OR company having application OR admin
    if current_user["role"] == "student" and resume["student_id"] != current_user["id"]:
        return api_response(success=False, message="Access denied.", status_code=403)

    file_path = resume["file_path"]
    if not os.path.exists(file_path):
        return api_response(success=False, message="File not found on server.", status_code=404)

    return send_file(file_path, as_attachment=True, download_name=resume["file_name"])

@resumes_bp.route("/<int:resume_id>", methods=["DELETE"])
@token_required
@role_required("student", "admin")
def delete_resume(current_user, resume_id):
    """
    Deletes resume file and associated records.
    """
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT student_id, file_path FROM resumes WHERE id = %s", (resume_id,))
            resume = cursor.fetchone()
            if not resume:
                return api_response(success=False, message="Resume not found.", status_code=404)

            if current_user["role"] != "admin" and resume["student_id"] != current_user["id"]:
                return api_response(success=False, message="Unauthorized to delete this resume.", status_code=403)

            cursor.execute("DELETE FROM resumes WHERE id = %s", (resume_id,))

    # Remove physical file if exists
    if resume.get("file_path") and os.path.exists(resume["file_path"]):
        try:
            os.remove(resume["file_path"])
        except Exception:
            pass

    return api_response(success=True, message="Resume deleted successfully.")
