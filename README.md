# AI Resume Analyzer & Job Matcher

> **"Analyze Your Resume. Discover Your Skills. Find Your Best-Matching Jobs."**

An enterprise-grade, production-style full-stack web application that combines **Vue 3**, **Flask (Python)**, **XAMPP MySQL**, and an **explainable NLP/AI matching engine** to deliver real-time ATS resume scoring, automated skill extraction, multi-factor job compatibility rankings, and conversational career coaching.

---

## 🌟 Key Features

### 👨‍🎓 For Students
- **Multi-Format Resume Upload**: Upload `.pdf`, `.docx`, or `.txt` resumes with automated parsing.
- **ATS Resume Health Scorer (0-100)**: Evaluates section completeness, quantifiable metrics, action verbs, contact information, and formatting density.
- **Automated Skill Extraction**: Pattern-matches technical skills into normalized taxonomy categories with context confidence ratings.
- **Multi-Factor AI Job Matching**: Computes live explainable compatibility scores for every job listing (Skill Overlap + TF-IDF Text Similarity + Experience + Education).
- **Missing Skills & Learning Suggestions**: Pinpoints exact skill gaps for target roles.
- **Application Tracking**: Real-time status pipeline (`Applied` $\rightarrow$ `Under Review` $\rightarrow$ `Shortlisted` $\rightarrow$ `Interview` $\rightarrow$ `Selected` / `Rejected`).
- **Saved / Bookmarked Jobs**: One-click position bookmarking.
- **Grounded AI Career Coach**: Context-aware chat assistant referencing the candidate's real resume and active jobs.

### 🏢 For Employers / Companies
- **Company Branding & Profile**: Custom profile, industry, website, and location metadata.
- **Job Posting & Management**: Publish vacancies with required and preferred tech stacks, salary ranges, and deadlines.
- **AI-Ranked Applicant Screening**: Candidates automatically sorted by compatibility percentage.
- **Applicant AI Inspection**: View candidate profile, download original resume, review cover note, and inspect skill breakdowns.
- **Hiring Pipeline Status Management**: Update status (`Shortlisted`, `Interview`, `Selected`, `Rejected`) with instant feedback to candidates.
- **Recruitment Analytics**: Dashboard metrics for applicants by job, average candidate match scores, and interview conversion ratios.

### ⚡ For Platform Administrators
- **System Overview Dashboard**: Total users, active jobs, submitted applications, and AI analyses counts.
- **User Account Management**: Search, audit, and toggle active/inactive account status.
- **Job Listing Oversight**: Moderate and remove inappropriate postings across companies.
- **Applications Oversight**: Cross-platform application monitoring.

---

## 🏗️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | Vue 3 (Composition API), Vite, Pinia, Vue Router, Vanilla CSS Design System, Lucide Icons, Chart.js |
| **Backend** | Python 3, Flask, Flask-CORS, PyMySQL, Cryptography, PyJWT, Werkzeug |
| **AI / NLP** | TF-IDF Vectorizer, Cosine Similarity, `pypdf`, `python-docx`, Skill Taxonomy Engine |
| **Database** | MySQL (via XAMPP), Auto-Initialization, Schema Migrations, Safe Seeding |

---

## 📁 Repository Structure

```
ai-resume-job-matcher/
├── backend/
│   ├── ai/                      # NLP parsing, skill taxonomy, resume scoring, matching, assistant
│   ├── database/                # Connection pooling, schema.sql, seed.sql
│   ├── routes/                  # REST API Blueprints (auth, students, companies, jobs, resumes, etc.)
│   ├── tests/                   # Automated unit & end-to-end test suite
│   ├── utils/                   # JWT auth middleware, validators, file uploads, response builders
│   ├── uploads/resumes/         # Local resume file storage
│   ├── app.py                   # Main Flask application entry point
│   ├── config.py                # App configuration & environment variables
│   ├── init_db.py               # Database auto-setup and seeding script
│   └── requirements.txt         # Backend Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── api/                 # Axios client and centralized endpoint wrappers
│   │   ├── assets/              # Modern CSS design system & glassmorphism tokens
│   │   ├── components/common/   # Navbar, Footer, Toast, MatchScoreBadge, Modal, Loader, EmptyState
│   │   ├── router/              # Vue Router with role-based navigation guards
│   │   ├── stores/              # Pinia state stores (auth, toast)
│   │   └── views/               # Public, Student, Company, and Admin views
│   ├── package.json
│   └── vite.config.js
│
├── docs/                        # Complete technical documentation
│   ├── architecture.md
│   ├── database.md
│   ├── api.md
│   ├── ai-model.md
│   └── setup.md
│
├── .env.example
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Start XAMPP MySQL
Ensure the **MySQL** service is started in your **XAMPP Control Panel** (listening on `localhost:3306`).

### 2. Run the Backend
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python init_db.py --seed
python app.py
```
*Backend runs on `http://127.0.0.1:5000`.*

### 3. Run the Frontend
```bash
cd frontend
npm install
npm run dev
```
*Frontend runs on `http://localhost:5173`.*

---

## 🔑 Demo Accounts

Use these pre-configured accounts (or use the one-click demo buttons on the login page):

- **Student**: `alex.student@example.com` / `Student@123`
- **Company**: `hr@technova.com` / `Company@123`
- **Admin**: `admin@airesume.com` / `Admin@123`

---

## 🧪 Running Tests

Run the automated backend test suite:
```bash
cd backend
python -m unittest discover -s tests -p "test_*.py"
```

---

## 📄 License
MIT License. Built for educational, production, and recruitment engineering workflows.
