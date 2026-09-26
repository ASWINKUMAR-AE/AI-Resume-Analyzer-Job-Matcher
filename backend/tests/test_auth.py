import unittest
import json
import os
import sys

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from database.connection import get_db

class TestAuthAndFlow(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_health_check(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["backend"], "running")
        self.assertEqual(data["data"]["database"], "connected")

    def test_admin_login(self):
        payload = {
            "email": "admin@airesume.com",
            "password": "Admin@123"
        }
        res = self.client.post("/api/auth/login", json=payload)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["user"]["role"], "admin")
        self.assertIn("token", data["data"])

    def test_student_registration_and_login(self):
        test_email = f"test_student_{os.urandom(3).hex()}@example.com"
        reg_payload = {
            "name": "Integration Test Student",
            "email": test_email,
            "password": "SecurePassword123!",
            "role": "student",
            "college": "MIT",
            "degree": "Computer Science",
            "experience": "1-2 years"
        }
        reg_res = self.client.post("/api/auth/register", json=reg_payload)
        self.assertEqual(reg_res.status_code, 201)
        reg_data = json.loads(reg_res.data)
        self.assertTrue(reg_data["success"])
        self.assertIn("token", reg_data["data"])

        # Login with newly created student
        login_res = self.client.post("/api/auth/login", json={"email": test_email, "password": "SecurePassword123!"})
        self.assertEqual(login_res.status_code, 200)
        login_data = json.loads(login_res.data)
        self.assertTrue(login_data["success"])
        self.assertEqual(login_data["data"]["user"]["email"], test_email)

    def test_duplicate_email_fails(self):
        reg_payload = {
            "name": "Duplicate Test",
            "email": "admin@airesume.com",
            "password": "Password123!",
            "role": "student"
        }
        res = self.client.post("/api/auth/register", json=reg_payload)
        self.assertEqual(res.status_code, 409)

if __name__ == "__main__":
    unittest.main()
