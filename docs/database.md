# Database Design & Schema Reference

Target RDBMS: **MySQL (XAMPP)**
Database Name: `ai_resume_matcher`
Default Port: `3306`

---

## 1. Relational Entity Diagram

```
+---------------+       +--------------------+       +------------------+
|     users     | <---> |  student_profiles  |       |  extracted_skills|
|---------------| 1   1 |--------------------|       |------------------|
| id (PK)       |       | id (PK)            |       | id (PK)          |
| name          |       | user_id (FK)       |       | resume_id (FK)   |
| email (UQ)    |       | college            |       | skill_name       |
| password_hash |       | degree             |       | category         |
| role          |       | experience         |       | confidence       |
| status        |       +--------------------+       +--------+---------+
+-------+-------+                                             |
        | 1                                                   | *
        |                                            +--------v---------+
        | 1             +--------------------+       |     resumes      |
        +-------------> |  company_profiles  |       |------------------|
        |               |--------------------|       | id (PK)          |
        |               | id (PK)            |       | student_id (FK)  |
        |               | user_id (FK)       |       | file_name        |
        |               | company_name       |       | file_path        |
        |               | industry           |       | raw_text         |
        |               +--------------------+       | resume_score     |
        |                                            +--------+---------+
        | *                                                   | 1
+-------v-------+       +--------------------+                |
|     jobs      | <---> |    applications    | <--------------+
|---------------| 1   * |--------------------|
| id (PK)       |       | id (PK)            |
| company_id(FK)|       | job_id (FK)        |
| title         |       | student_id (FK)    |
| description   |       | resume_id (FK)     |
| requirements  |       | match_score        |
| skills        |       | status             |
| job_type      |       +--------------------+
| salary_min    |
| salary_max    |       +--------------------+
| status        |       |    ai_analysis     |
+---------------+       |--------------------|
                        | id (PK)            |
                        | student_id (FK)    |
                        | job_id (FK)        |
                        | resume_id (FK)     |
                        | match_score        |
                        | score_breakdown    |
                        +--------------------+
```

---

## 2. Table Definitions

### 1. `users`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier |
| `name` | VARCHAR(150) | NOT NULL | User's full or representative name |
| `email` | VARCHAR(191) | NOT NULL, UNIQUE | User login email address |
| `password_hash` | VARCHAR(255) | NOT NULL | Secure salted password hash |
| `role` | ENUM('student', 'company', 'admin') | NOT NULL | Account access role |
| `status` | ENUM('active', 'inactive', 'pending') | DEFAULT 'active' | Account state |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Registration timestamp |

### 2. `student_profiles`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Profile identifier |
| `user_id` | INT | NOT NULL, UNIQUE, FK -> `users.id` | Cascading user reference |
| `phone` | VARCHAR(30) | NULL | Contact phone number |
| `location` | VARCHAR(150) | NULL | City/State/Country |
| `college` | VARCHAR(200) | NULL | Academic institution |
| `degree` | VARCHAR(150) | NULL | Major / Degree program |
| `graduation_year`| INT | NULL | Graduation year |
| `experience` | VARCHAR(100) | NULL | Experience level / years |
| `bio` | TEXT | NULL | Candidate career summary |
| `linkedin_url` | VARCHAR(255) | NULL | Professional profile URL |
| `github_url` | VARCHAR(255) | NULL | Code portfolio URL |
| `portfolio_url`| VARCHAR(255) | NULL | Personal website URL |

### 3. `company_profiles`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Company profile identifier |
| `user_id` | INT | NOT NULL, UNIQUE, FK -> `users.id` | Cascading user reference |
| `company_name` | VARCHAR(200) | NOT NULL | Registered company title |
| `company_email`| VARCHAR(191) | NULL | Official recruitment email |
| `website` | VARCHAR(255) | NULL | Company portal link |
| `industry` | VARCHAR(100) | NULL | Primary domain |
| `location` | VARCHAR(150) | NULL | Headquarters / Office location |
| `description` | TEXT | NULL | Mission and products |
| `verified` | TINYINT(1) | DEFAULT 0 | Verification status |

### 4. `resumes`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Resume identifier |
| `student_id` | INT | NOT NULL, FK -> `users.id` | Candidate user reference |
| `file_name` | VARCHAR(255) | NOT NULL | Original sanitized filename |
| `file_path` | VARCHAR(500) | NOT NULL | Local storage path |
| `file_type` | VARCHAR(50) | NOT NULL | Extension (pdf/docx/txt) |
| `raw_text` | LONGTEXT | NULL | Extracted raw text |
| `parsed_sections`| JSON | NULL | Detected structural sections |
| `resume_score` | INT | DEFAULT 0 | 0-100 ATS Health Score |
| `strengths` | JSON | NULL | Bulleted profile strengths |
| `weaknesses` | JSON | NULL | Improvement suggestions |
| `recommendations`| JSON | NULL | Actionable advice |

### 5. `extracted_skills`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Skill record ID |
| `resume_id` | INT | NOT NULL, FK -> `resumes.id` | Associated resume |
| `skill_name` | VARCHAR(100) | NOT NULL | Canonical normalized skill name |
| `category` | VARCHAR(100) | DEFAULT 'General' | Skill taxonomy domain |
| `confidence` | FLOAT | DEFAULT 1.0 | Context confidence (0.85-1.0) |

### 6. `jobs`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Job post ID |
| `company_id` | INT | NOT NULL, FK -> `users.id` | Posting company reference |
| `title` | VARCHAR(200) | NOT NULL | Job title |
| `description` | LONGTEXT | NOT NULL | Full job description |
| `requirements` | TEXT | NULL | Key requirements |
| `skills` | TEXT | NULL | Required skills (comma-separated) |
| `preferred_skills`| TEXT | NULL | Preferred skills |
| `location` | VARCHAR(150) | NULL | Role location or Remote |
| `job_type` | ENUM(...) | DEFAULT 'Full Time' | Work arrangement |
| `experience_required`| VARCHAR(100) | NULL | Years/level needed |
| `salary_min` | DECIMAL(12, 2)| NULL | Minimum compensation |
| `salary_max` | DECIMAL(12, 2)| NULL | Maximum compensation |
| `status` | ENUM('active','closed','draft') | DEFAULT 'active' | Listing status |

### 7. `applications`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Application identifier |
| `job_id` | INT | NOT NULL, FK -> `jobs.id` | Target vacancy |
| `student_id` | INT | NOT NULL, FK -> `users.id` | Applicant |
| `resume_id` | INT | NOT NULL, FK -> `resumes.id` | Submitted resume |
| `match_score` | FLOAT | DEFAULT 0 | Live AI Match Score % |
| `status` | ENUM(...) | DEFAULT 'Applied' | Applied/Review/Shortlisted/Interview/Selected/Rejected |
| `cover_note` | TEXT | NULL | Optional message to employer |
| `applied_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Submission timestamp |

### 8. `saved_jobs`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Save record ID |
| `student_id` | INT | NOT NULL, FK -> `users.id` | Student reference |
| `job_id` | INT | NOT NULL, FK -> `jobs.id` | Saved job reference |
| UNIQUE KEY `unique_student_job` (`student_id`, `job_id`) | Ensures a job is only saved once per student. |

### 9. `ai_analysis`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Analysis snapshot ID |
| `student_id` | INT | NOT NULL, FK -> `users.id` | Student reference |
| `resume_id` | INT | NOT NULL, FK -> `resumes.id` | Evaluated resume |
| `job_id` | INT | NOT NULL, FK -> `jobs.id` | Evaluated job |
| `match_score` | FLOAT | DEFAULT 0 | Composite compatibility score |
| `matched_skills`| JSON | NULL | Overlapping skills |
| `missing_skills`| JSON | NULL | Target skills gap |
| `score_breakdown`| JSON | NULL | Multi-factor weights breakdown |
