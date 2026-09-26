import os
import requests
from config import Config
from database.connection import get_db
from ai.recommender import JobRecommender

class AIAssistant:
    @staticmethod
    def chat(student_id, message, job_id=None):
        """
        Answers student career questions using their real profile, skills, and job data.
        """
        # 1. Gather student context from database
        context = AIAssistant._gather_student_context(student_id, job_id)
        
        # 2. Check if external LLM is configured (OpenAI or Gemini)
        if Config.OPENAI_API_KEY:
            try:
                response = AIAssistant._call_openai(message, context)
                if response:
                    return response
            except Exception:
                pass
                
        if Config.GEMINI_API_KEY:
            try:
                response = AIAssistant._call_gemini(message, context)
                if response:
                    return response
            except Exception:
                pass

        # 3. Local Grounded NLP Assistant (100% Offline Reliable Fallback)
        return AIAssistant._local_grounded_response(message, context)

    @staticmethod
    def _gather_student_context(student_id, job_id=None):
        ctx = {
            "name": "Student",
            "skills": [],
            "resume_score": 0,
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "target_job": None,
            "top_recommendations": []
        }
        
        with get_db() as conn:
            with conn.cursor() as cursor:
                # Student user & profile
                cursor.execute(
                    """
                    SELECT u.name, u.email, sp.college, sp.degree, sp.experience
                    FROM users u
                    LEFT JOIN student_profiles sp ON u.id = sp.user_id
                    WHERE u.id = %s
                    """,
                    (student_id,)
                )
                user_info = cursor.fetchone()
                if user_info:
                    ctx["name"] = user_info.get("name") or "Student"
                    ctx["degree"] = user_info.get("degree")
                    ctx["experience"] = user_info.get("experience")
                    
                # Latest resume
                cursor.execute(
                    "SELECT * FROM resumes WHERE student_id = %s ORDER BY created_at DESC LIMIT 1",
                    (student_id,)
                )
                resume = cursor.fetchone()
                if resume:
                    ctx["resume_score"] = resume.get("resume_score", 0)
                    # Extracted skills
                    cursor.execute(
                        "SELECT skill_name, category FROM extracted_skills WHERE resume_id = %s",
                        (resume["id"],)
                    )
                    skills_rows = cursor.fetchall()
                    ctx["skills"] = [s["skill_name"] for s in skills_rows]
                    
                # Target Job if specified
                if job_id:
                    cursor.execute(
                        """
                        SELECT j.*, c.company_name
                        FROM jobs j
                        JOIN company_profiles c ON j.company_id = c.user_id
                        WHERE j.id = %s
                        """,
                        (job_id,)
                    )
                    ctx["target_job"] = cursor.fetchone()
                    
        # Get top recommendations
        try:
            recs = JobRecommender.get_recommendations_for_student(student_id, limit=3)
            ctx["top_recommendations"] = recs
        except Exception:
            pass

        return ctx

    @staticmethod
    def _local_grounded_response(message, ctx):
        msg_lower = message.lower().strip()
        name = ctx.get("name", "Student")
        skills = ctx.get("skills", [])
        resume_score = ctx.get("resume_score", 0)
        target_job = ctx.get("target_job")
        top_recs = ctx.get("top_recommendations", [])

        # Match Intent: Job Recommendations
        if any(w in msg_lower for w in ["what jobs", "recommend", "best job", "matching job", "match my skills"]):
            if not skills:
                return (
                    f"Hello {name}! I noticed you haven't uploaded a resume yet. "
                    "Upload your resume in PDF or DOCX format, and I'll automatically extract your skills "
                    "and match you with open roles!"
                )
            if top_recs:
                job_list_str = "\n".join([
                    f"• **{j['title']}** at *{j['company_name']}* ({j['match_score']}% Match)\n  → Matched: {', '.join(j.get('matched_skills', [])[:3])}"
                    for j in top_recs
                ])
                return (
                    f"Based on your profile and {len(skills)} detected skills ({', '.join(skills[:5])}), "
                    f"here are your top AI job matches:\n\n{job_list_str}\n\n"
                    "Would you like advice on how to improve your score for any specific role?"
                )
            return f"You currently have {len(skills)} skills detected. Check out the **Recommended Jobs** section for live listings!"

        # Match Intent: Missing Skills / Skills Gap
        if any(w in msg_lower for w in ["missing", "what should i learn", "skill gap", "learn next", "need to learn"]):
            if target_job:
                req_skills = [s.strip() for s in (target_job.get("skills") or "").split(",") if s.strip()]
                missing = [s for s in req_skills if s not in skills]
                if missing:
                    return (
                        f"For the **{target_job.get('title')}** position at *{target_job.get('company_name')}*, "
                        f"you are currently missing these target skills:\n\n" +
                        "\n".join([f"• **{m}**" for m in missing]) +
                        f"\n\n💡 **Action Step**: Building a small demo project with {missing[0]} or earning a foundational certification can significantly boost your match score!"
                    )
                return f"Great news! You already possess all core required skills for **{target_job.get('title')}**!"
            elif top_recs and top_recs[0].get("missing_skills"):
                top_job = top_recs[0]
                missing = top_job.get("missing_skills", [])
                return (
                    f"Looking at your top match (**{top_job['title']}**), the most impactful skills you could learn next are:\n\n" +
                    "\n".join([f"• **{m}**" for m in missing[:4]]) +
                    "\n\nAdding these to your technical repertoire will open up more high-matching opportunities."
                )
            return "To see missing skills, browse to any job details page or ask me about a specific position!"

        # Match Intent: Resume Score Improvement
        if any(w in msg_lower for w in ["improve", "score", "better resume", "resume health", "ats"]):
            if resume_score == 0:
                return "Please upload your resume to the **Resume Analysis** section first to generate your initial score and customized audit!"
            return (
                f"Your current Resume Health Score is **{resume_score}/100**.\n\n"
                "Here are key ways to boost it to 90+:\n"
                "1. **Quantify Results**: Replace passive bullets with metrics (e.g. *'Engineered a REST API with Flask that cut load times by 35%'*).\n"
                "2. **Add Missing Skills**: Ensure tools, databases, and cloud services you know are explicitly listed in your Skills section.\n"
                "3. **Contact Details**: Ensure your LinkedIn profile and GitHub repository URLs are clearly visible in the header.\n"
                "4. **Action Verbs**: Begin bullet points with strong verbs like *Architected, Engineered, Optimized, Deployed*."
            )

        # Match Intent: Why Match %
        if any(w in msg_lower for w in ["why did i get", "why match", "why score", "why 82%", "explain score"]):
            if target_job:
                return (
                    f"Your match score for **{target_job.get('title')}** is calculated using our explainable multi-factor formula:\n\n"
                    "• **Skill Overlap (45% weight)**: Compares required tech stack against your extracted skills.\n"
                    "• **TF-IDF Text Similarity (30% weight)**: Evaluates semantic relevance between your resume content and the job description.\n"
                    "• **Experience Alignment (15% weight)**: Compares your years of experience with the role level.\n"
                    "• **Education Alignment (10% weight)**: Verifies degree and field of study prerequisites."
                )
            return (
                "Our AI calculates job match scores using: **45% Skill Match + 30% TF-IDF Text Similarity + 15% Experience Match + 10% Education Match**."
            )

        # General Greetings & Assistant Overview
        return (
            f"Hello {name}! I am your AI Career & Resume Assistant. 🚀\n\n"
            "You can ask me:\n"
            "• *'What jobs match my skills?'*\n"
            "• *'What skills am I missing for this role?'*\n"
            "• *'How can I improve my resume score?'*\n"
            "• *'Why did I get this match percentage?'*\n\n"
            "How can I assist you with your job search today?"
        )

    @staticmethod
    def _call_openai(message, context):
        import json
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {Config.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        system_prompt = (
            "You are an expert AI Career Coach for an AI Resume Analyzer and Job Matcher platform. "
            f"Candidate Name: {context.get('name')}. "
            f"Candidate Skills: {', '.join(context.get('skills', []))}. "
            f"Resume Score: {context.get('resume_score')}/100. "
            "Be encouraging, concise, actionable, and grounded in the candidate's actual data."
        )
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "max_tokens": 350,
            "temperature": 0.7
        }
        res = requests.post(url, headers=headers, json=payload, timeout=8)
        if res.status_code == 200:
            data = res.json()
            return data["choices"][0]["message"]["content"]
        return None

    @staticmethod
    def _call_gemini(message, context):
        import json
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={Config.GEMINI_API_KEY}"
        system_prompt = (
            "You are an expert AI Career Coach. "
            f"Candidate Name: {context.get('name')}. "
            f"Candidate Skills: {', '.join(context.get('skills', []))}. "
            f"Resume Score: {context.get('resume_score')}/100. "
            "Answer the student's question concisely."
        )
        payload = {
            "contents": [{
                "parts": [{"text": f"{system_prompt}\n\nUser Question: {message}"}]
            }]
        }
        res = requests.post(url, json=payload, timeout=8)
        if res.status_code == 200:
            data = res.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        return None
