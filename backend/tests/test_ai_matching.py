import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai.skill_extractor import SkillExtractor
from ai.resume_scorer import ResumeScorer
from ai.matcher import JobMatcher

class TestAIMatchingAndScoring(unittest.TestCase):
    def test_skill_extraction(self):
        sample_text = """
        PROFESSIONAL SUMMARY
        Experienced Full Stack Developer with 3+ years in Python, Flask, Vue.js, TypeScript, and MySQL.
        Built REST APIs and deployed scalable Docker containers on AWS cloud with CI/CD GitHub Actions.
        SKILLS
        Languages: Python, JavaScript, TypeScript, SQL, HTML, CSS
        Frameworks: Vue.js, Flask, Tailwind CSS, Express.js
        Databases: MySQL, PostgreSQL, MongoDB, Redis
        Cloud & Tools: AWS, Docker, Kubernetes, Git, Linux
        """
        extracted = SkillExtractor.extract_skills(sample_text)
        skill_names = [s["skill_name"] for s in extracted]
        
        self.assertIn("Python", skill_names)
        self.assertIn("Flask", skill_names)
        self.assertIn("Vue.js", skill_names)
        self.assertIn("MySQL", skill_names)
        self.assertIn("Docker", skill_names)
        self.assertIn("AWS", skill_names)
        self.assertIn("Git", skill_names)

    def test_resume_scoring(self):
        sample_text = """
        Alex Rivera
        Email: alex@example.com | Phone: 555-0199 | LinkedIn: linkedin.com/in/alex-dev | GitHub: github.com/alex-dev
        
        SUMMARY
        Passionate software engineer focused on building robust AI web platforms.
        
        SKILLS
        Python, Flask, Vue.js, JavaScript, MySQL, Docker, AWS, Git, REST API
        
        WORK EXPERIENCE
        Software Engineer Intern - TechCo (2023 - 2024)
        • Developed full stack web applications using Vue 3 and Python Flask.
        • Improved database query performance by 35% using MySQL indexing.
        • Engineered automated CI/CD deployment pipelines on AWS reducing deployment time by 50%.
        
        EDUCATION
        Stanford University - Bachelor of Science in Computer Science (2025)
        
        PROJECTS
        AI Resume Matcher: Architected an end-to-end NLP job matcher with 95% classification accuracy.
        """
        sections = {
            "summary": "Passionate software engineer",
            "skills": "Python, Flask, Vue.js, JavaScript, MySQL, Docker, AWS, Git, REST API",
            "experience": "Software Engineer Intern - TechCo (2023 - 2024)",
            "education": "Stanford University - Bachelor of Science in Computer Science",
            "projects": "AI Resume Matcher"
        }
        contact = {
            "email": "alex@example.com",
            "phone": "555-0199",
            "linkedin_url": "linkedin.com/in/alex-dev",
            "github_url": "github.com/alex-dev"
        }
        skills = SkillExtractor.extract_skills(sample_text, sections)
        score_result = ResumeScorer.score_resume(sample_text, sections, skills, contact)
        
        self.assertGreaterEqual(score_result["resume_score"], 75)
        self.assertTrue(len(score_result["strengths"]) > 0)
        self.assertIn("section_completeness", score_result["breakdown"])

    def test_job_matcher_eval(self):
        resume_text = "Experienced in Python, Flask, Vue.js, MySQL, REST API, Git, Docker."
        resume_skills = ["Python", "Flask", "Vue.js", "MySQL", "REST API", "Git"]
        
        job_dict = {
            "title": "Full Stack Python Developer",
            "description": "Seeking Python and Vue.js full stack developer to build REST APIs and MySQL databases.",
            "requirements": "Bachelor in CS, Python, Flask, Vue.js, MySQL, REST API, Docker.",
            "skills": "Python, Flask, Vue.js, MySQL, REST API, Docker",
            "experience_required": "1-3 years"
        }
        candidate_profile = {"degree": "Bachelor of Science", "experience": "2 years"}
        
        match_result = JobMatcher.evaluate_match(resume_text, resume_skills, job_dict, candidate_profile)
        
        self.assertGreater(match_result["match_score"], 70.0)
        self.assertIn("Python", match_result["matched_skills"])
        self.assertIn("Flask", match_result["matched_skills"])
        self.assertIn("Vue.js", match_result["matched_skills"])
        self.assertIn("Docker", match_result["missing_skills"])

if __name__ == "__main__":
    unittest.main()
