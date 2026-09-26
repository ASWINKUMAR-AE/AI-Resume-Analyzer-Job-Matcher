# Local Setup & Installation Guide

This guide describes how to run the full **AI Resume Analyzer & Job Matcher** application locally on Windows with XAMPP MySQL.

---

## 1. Prerequisites

1. **XAMPP** (with Apache and MySQL enabled)
2. **Python 3.10+** (Python 3.11, 3.12, 3.13, 3.14 supported)
3. **Node.js 18+** and **npm**

---

## 2. Step 1: Start XAMPP MySQL

1. Open **XAMPP Control Panel**.
2. Click **Start** on the **MySQL** module.
3. Ensure MySQL is running on default port `3306`.

---

## 3. Step 2: Backend Setup

1. Open a terminal and navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # On Windows CMD:
   .\venv\Scripts\activate.bat
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Verify or copy the environment configuration:
   ```bash
   copy ..\.env.example .env
   ```

5. Initialize the MySQL Database and Demo Data:
   ```bash
   python init_db.py --seed
   ```

6. Start the Flask Backend:
   ```bash
   python app.py
   ```
   *The backend will start on `http://127.0.0.1:5000`.*

---

## 4. Step 3: Frontend Setup

1. Open a second terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install npm packages:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   *The frontend will launch on `http://localhost:5173`.*

---

## 5. Demo Accounts

For quick manual testing, use the following pre-seeded credentials (or click the instant demo buttons on the Login page):

| Role | Email | Password | Description |
|---|---|---|---|
| **Student** | `alex.student@example.com` | `Student@123` | Alex Rivera (CS Graduate with Python & Vue skills) |
| **Company** | `hr@technova.com` | `Company@123` | TechNova Solutions HR |
| **Company** | `careers@zethub.com` | `Company@123` | ZetHub Technologies Recruitment |
| **Admin** | `admin@airesume.com` | `Admin@123` | System Administrator |

---

## 6. Running Automated Backend Tests

To run the full unit and end-to-end test suite:
```bash
cd backend
python -m unittest discover -s tests -p "test_*.py"
```
