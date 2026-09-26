import unittest
import json
import io
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app

class TestEndToEndFlow(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_full_application_and_hiring_cycle(self):
        # 1. Register a new Student
        unique_id = os.urandom(4).hex()
        student_email = f"e2e_student_{unique_id}@test.com"
        reg_res = self.client.post("/api/auth/register", json={
            "name": f"E2E Candidate {unique_id}",
            "email": student_email,
            "password": "Password123!",
            "role": "student",
            "college": "MIT University",
            "degree": "Computer Science",
            "experience": "2 years"
        })
        self.assertEqual(reg_res.status_code, 201)
        student_token = json.loads(reg_res.data)["data"]["token"]
        student_auth = {"Authorization": f"Bearer {student_token}"}

        # 2. Student uploads resume (TXT mock)
        resume_str = f"""
        E2E Candidate
        Email: {student_email} | Phone: 555-0199 | LinkedIn: linkedin.com/in/e2ecandidate
        
        SUMMARY
        Full stack developer specializing in Python, Flask, Vue.js, MySQL, and Docker.
        
        SKILLS
        Python, Flask, Vue.js, JavaScript, MySQL, Docker, REST API, Git
        
        WORK EXPERIENCE
        Full Stack Engineer - InnovateSoft (2023 - 2025)
        • Developed responsive Vue.js frontend interfaces and Python Flask REST APIs.
        • Optimized MySQL queries and integrated Docker CI/CD pipelines.
        • Improved response times by 40% across all customer portals.
        
        EDUCATION
        MIT University - Bachelor of Science in Computer Science (2025)
        
        PROJECTS
        AI Resume Matcher: Developed a modern web app for resume analysis and job matching.
        """
        upload_data = {
            "resume": (io.BytesIO(resume_str.encode("utf-8")), "e2e_resume.txt")
        }
        upload_res = self.client.post("/api/resume/upload", data=upload_data, headers=student_auth, content_type="multipart/form-data")
        self.assertEqual(upload_res.status_code, 201)
        upload_json = json.loads(upload_res.data)
        self.assertTrue(upload_json["success"])
        self.assertGreater(upload_json["data"]["resume_score"], 60)
        resume_id = upload_json["data"]["resume_id"]

        # 3. Student views AI recommendations
        recs_res = self.client.get("/api/ai/recommendations", headers=student_auth)
        self.assertEqual(recs_res.status_code, 200)
        recs = json.loads(recs_res.data)["data"]
        self.assertTrue(len(recs) > 0)
        target_job = recs[0]
        job_id = target_job["id"]

        # 4. Student applies for the top recommended job
        apply_res = self.client.post(f"/api/applications/jobs/{job_id}/apply", json={
            "resume_id": resume_id,
            "cover_note": "Excited to apply for this role!"
        }, headers=student_auth)
        self.assertEqual(apply_res.status_code, 201)
        apply_data = json.loads(apply_res.data)["data"]
        app_id = apply_data["application_id"]
        self.assertGreater(apply_data["match_score"], 0)

        # 5. Company logs in (using demo company credentials)
        comp_login_res = self.client.post("/api/auth/login", json={
            "email": "hr@technova.com",
            "password": "Company@123"
        })
        self.assertEqual(comp_login_res.status_code, 200)
        company_token = json.loads(comp_login_res.data)["data"]["token"]
        company_auth = {"Authorization": f"Bearer {company_token}"}

        # 6. Company reviews applicants (or admin check)
        admin_login = self.client.post("/api/auth/login", json={"email": "admin@airesume.com", "password": "Admin@123"})
        admin_token = json.loads(admin_login.data)["data"]["token"]
        admin_auth = {"Authorization": f"Bearer {admin_token}"}
        
        apps_res = self.client.get("/api/applications/company", headers=admin_auth)
        self.assertEqual(apps_res.status_code, 200)
        apps_list = json.loads(apps_res.data)["data"]
        matched_app = next((a for a in apps_list if a["id"] == app_id), None)
        self.assertIsNotNone(matched_app)

        # 7. Update status to 'Shortlisted'
        status_res = self.client.put(f"/api/applications/{app_id}/status", json={"status": "Shortlisted"}, headers=admin_auth)
        self.assertEqual(status_res.status_code, 200)

        # 8. Student checks their applications and sees updated status
        student_apps_res = self.client.get("/api/applications/student", headers=student_auth)
        self.assertEqual(student_apps_res.status_code, 200)
        student_apps = json.loads(student_apps_res.data)["data"]
        my_app = next(a for a in student_apps if a["id"] == app_id)
        self.assertEqual(my_app["status"], "Shortlisted")

        # 9. Student chats with AI assistant
        chat_res = self.client.post("/api/ai/chat", json={
            "message": "What jobs match my skills?",
            "job_id": job_id
        }, headers=student_auth)
        self.assertEqual(chat_res.status_code, 200)
        chat_data = json.loads(chat_res.data)["data"]
        self.assertIn("reply", chat_data)

if __name__ == "__main__":
    unittest.main()
