# REST API Documentation

Base URL: `http://localhost:5000/api`

All JSON endpoints return standardized payloads:
```json
{
  "success": true,
  "message": "Human readable message",
  "data": {}
}
```

---

## 1. Authentication Endpoints

### `POST /auth/register`
Creates a student or company account with automatic profile record creation.
- **Request Body**:
  ```json
  {
    "name": "Alex Rivera",
    "email": "alex@example.com",
    "password": "Password123!",
    "role": "student",
    "college": "Stanford University",
    "degree": "B.S. in Computer Science",
    "graduation_year": 2025,
    "experience": "1-2 years"
  }
  ```
- **Response (201)**: Returns `{ token, user }`.

### `POST /auth/login`
- **Request Body**: `{ "email": "alex@example.com", "password": "Password123!" }`
- **Response (200)**: Returns `{ token, user }`.

### `GET /auth/me`
- **Headers**: `Authorization: Bearer <token>`
- **Response (200)**: Returns authenticated user profile information.

### `POST /auth/change-password`
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**: `{ "old_password": "...", "new_password": "..." }`

---

## 2. Student Endpoints

### `GET /student/dashboard`
- **Headers**: `Authorization: Bearer <token>` (Student)
- **Response (200)**: Aggregates latest resume, resume health score, detected skills, stats (applied, shortlisted, interviews, saved), and top AI recommended jobs.

### `GET /student/skills`
- **Response (200)**: Returns categorized skills matrix with confidence ratings for student's resume.

### `GET /student/saved-jobs`
- **Response (200)**: List of bookmarked jobs.

### `POST /student/saved-jobs/:job_id`
- **Response (200)**: Toggles bookmark status (`is_saved: true/false`).

---

## 3. Resume & AI Endpoints

### `POST /resume/upload`
- **Headers**: `Content-Type: multipart/form-data`, `Authorization: Bearer <token>`
- **Form Data**: `resume` (PDF, DOCX, TXT file)
- **Response (201)**: Returns extracted sections, detected skills list, 0-100 ATS health score, strengths, weaknesses, and improvement suggestions.

### `GET /resume`
- **Response (200)**: Returns current student's latest parsed resume record.

### `GET /resume/download/:resume_id`
- **Response (200)**: Securely serves original resume file as attachment.

---

## 4. Jobs & Recommendations

### `GET /jobs`
- **Query Parameters**:
  - `q`: search string (title, skills, company)
  - `location`: filter by location
  - `job_type`: Full Time, Internship, Remote, etc.
  - `sort`: `newest` or `match` (if student token is attached)
- **Response (200)**: List of jobs with dynamic AI match percentage for authenticated students.

### `GET /jobs/:id`
- **Response (200)**: Detailed job breakdown with company details, requirements, and full AI multi-factor match analysis.

### `POST /jobs`
- **Headers**: `Authorization: Bearer <token>` (Company)
- **Request Body**: `{ title, description, skills, location, job_type, salary_min, salary_max, ... }`

### `GET /ai/recommendations`
- **Response (200)**: Returns jobs ranked descending by student's AI match score with "Why Matched" explanations.

### `POST /ai/chat`
- **Headers**: `Authorization: Bearer <token>` (Student)
- **Request Body**: `{ "message": "What skills am I missing for Frontend Engineer?", "job_id": 2 }`
- **Response (200)**: Returns grounded career advice based on student's actual resume and targeted job requirements.

---

## 5. Applications Endpoints

### `POST /applications/jobs/:job_id/apply`
- **Headers**: `Authorization: Bearer <token>` (Student)
- **Request Body**: `{ "cover_note": "Excited to apply..." }`
- **Response (201)**: Submits application with live AI match snapshot.

### `GET /applications/student`
- **Response (200)**: Returns student's submitted applications with live status.

### `GET /applications/company`
- **Headers**: `Authorization: Bearer <token>` (Company)
- **Query Parameters**: `job_id`, `status`, `q`
- **Response (200)**: Returns ranked applicant list for company's job postings.

### `PUT /applications/:app_id/status`
- **Headers**: `Authorization: Bearer <token>` (Company)
- **Request Body**: `{ "status": "Shortlisted" }` (Allowed: `Applied`, `Under Review`, `Shortlisted`, `Interview`, `Selected`, `Rejected`)

---

## 6. Admin Endpoints

### `GET /admin/dashboard`
- **Response (200)**: Platform stats (total users, students, companies, jobs, resumes, average match score).

### `GET /admin/users`
- **Response (200)**: Paginated/filtered platform users.

### `PUT /admin/users/:id/status`
- **Request Body**: `{ "status": "active" | "inactive" }`

### `DELETE /admin/jobs/:id`
- **Response (200)**: Moderates and deletes job posting.

---

## 7. System Health Endpoint

### `GET /health`
- **Response (200)**:
  ```json
  {
    "success": true,
    "message": "All systems operational",
    "data": {
      "backend": "running",
      "database": "connected",
      "ai": "available",
      "mysql_host": "localhost:3306",
      "database_name": "ai_resume_matcher"
    }
  }
  ```
