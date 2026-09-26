from database.connection import get_db
from ai.matcher import JobMatcher

class JobRecommender:
    @staticmethod
    def get_recommendations_for_student(student_id, resume_id=None, limit=10):
        """
        Ranks all active jobs for a student based on AI match score.
        """
        with get_db() as conn:
            with conn.cursor() as cursor:
                # 1. Fetch student's profile
                cursor.execute(
                    "SELECT * FROM student_profiles WHERE user_id = %s", (student_id,)
                )
                profile = cursor.fetchone() or {}

                # 2. Fetch student's resume
                if resume_id:
                    cursor.execute(
                        "SELECT * FROM resumes WHERE id = %s AND student_id = %s",
                        (resume_id, student_id)
                    )
                else:
                    cursor.execute(
                        "SELECT * FROM resumes WHERE student_id = %s ORDER BY created_at DESC LIMIT 1",
                        (student_id,)
                    )
                resume = cursor.fetchone()

                if not resume:
                    # If no resume uploaded yet, return recent active jobs
                    cursor.execute(
                        """
                        SELECT j.*, c.company_name, c.logo AS company_logo, c.location AS company_location
                        FROM jobs j
                        JOIN company_profiles c ON j.company_id = c.user_id
                        WHERE j.status = 'active'
                        ORDER BY j.created_at DESC
                        LIMIT %s
                        """,
                        (limit,)
                    )
                    recent_jobs = cursor.fetchall()
                    for job in recent_jobs:
                        job["match_score"] = 50.0
                        job["why_matched"] = "Recommended entry: Upload your resume to unlock accurate AI skill matching."
                        job["matched_skills"] = []
                        job["missing_skills"] = [s.strip() for s in (job.get("skills") or "").split(",") if s.strip()]
                    return recent_jobs

                # 3. Fetch extracted skills for this resume
                cursor.execute(
                    "SELECT skill_name, category, confidence FROM extracted_skills WHERE resume_id = %s",
                    (resume["id"],)
                )
                skills = cursor.fetchall()
                raw_text = resume.get("raw_text", "")

                # 4. Fetch all active jobs with company details
                cursor.execute(
                    """
                    SELECT j.*, c.company_name, c.logo AS company_logo, c.location AS company_location,
                           (SELECT COUNT(*) FROM saved_jobs sj WHERE sj.job_id = j.id AND sj.student_id = %s) AS is_saved,
                           (SELECT app.status FROM applications app WHERE app.job_id = j.id AND app.student_id = %s LIMIT 1) AS applied_status
                    FROM jobs j
                    JOIN company_profiles c ON j.company_id = c.user_id
                    WHERE j.status = 'active'
                    ORDER BY j.created_at DESC
                    """,
                    (student_id, student_id)
                )
                all_jobs = cursor.fetchall()

                ranked_jobs = []
                for job in all_jobs:
                    eval_result = JobMatcher.evaluate_match(
                        resume_text=raw_text,
                        resume_skills=skills,
                        job_dict=job,
                        candidate_profile=profile
                    )
                    
                    job_copy = dict(job)
                    job_copy["match_score"] = eval_result["match_score"]
                    job_copy["matched_skills"] = eval_result["matched_skills"]
                    job_copy["missing_skills"] = eval_result["missing_skills"]
                    job_copy["score_breakdown"] = eval_result["score_breakdown"]
                    job_copy["strengths"] = eval_result["strengths"]
                    job_copy["weaknesses"] = eval_result["weaknesses"]
                    job_copy["recommendations"] = eval_result["recommendations"]
                    job_copy["why_matched"] = eval_result["why_matched_summary"]
                    job_copy["is_saved"] = bool(job.get("is_saved"))
                    job_copy["applied_status"] = job.get("applied_status")
                    
                    ranked_jobs.append(job_copy)

                # Sort by match_score descending
                ranked_jobs.sort(key=lambda x: x["match_score"], reverse=True)
                return ranked_jobs[:limit]
