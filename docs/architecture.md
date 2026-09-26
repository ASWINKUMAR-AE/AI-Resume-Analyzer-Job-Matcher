# System Architecture

## 1. High-Level Architecture

The **AI Resume Analyzer & Job Matcher** application is constructed using a decoupled modern multi-tier architecture:

```
+-------------------------------------------------------------+
|                      Vue 3 + Vite Frontend                  |
|  - Pinia Stores (Auth, Toast, Resume, Jobs)                |
|  - Vue Router (Role-Based Guards: Student, Company, Admin) |
|  - Axios API Interceptors & Reactive UI Components          |
+------------------------------+------------------------------+
                               | REST JSON API (HTTP/JWT)
                               v
+-------------------------------------------------------------+
|                     Flask Backend (Python)                  |
|  - Blueprints: Auth, Students, Companies, Jobs, Resumes,   |
|    Applications, AI, Admin, Health                          |
|  - Security & Middleware: JWT Token Auth, Role Auth, CORS   |
|  - File Upload Handler & Validation                         |
+---------------+-----------------------------+---------------+
                |                             |
                v                             v
+-------------------------------+  +--------------------------+
|       Local AI / NLP Engine   |  |   MySQL Database (XAMPP) |
|  - Parser: PDF, DOCX, TXT     |  |   - Host: localhost:3306 |
|  - Skill Taxonomy & Aliases   |  |   - DB: ai_resume_matcher|
|  - TF-IDF & Cosine Similarity |  |   - Auto-Init & Seeding  |
|  - Resume ATS Health Scorer   |  +--------------------------+
|  - Explainable Match Engine   |
|  - Grounded AI Career Coach   |
+-------------------------------+
```

---

## 2. Component Breakdown

### Frontend (Vue 3 + Vite)
- **Framework**: Vue 3 Composition API with `<script setup>`
- **Routing**: Vue Router 4 with navigation guards enforcing authentication and role permissions (`student`, `company`, `admin`).
- **State Management**: Pinia stores (`auth`, `toast`).
- **Styling**: Vanilla CSS design system with curated HSL color tokens, glassmorphism, responsive grid layout, and zero horizontal scrolling.

### Backend (Python + Flask)
- **Modular Structure**:
  - `app.py`: Application entry point and blueprint loader.
  - `config.py`: Environment-driven configuration.
  - `init_db.py`: Automatic schema verification, table creation, and demo data seeding.
  - `database/connection.py`: Context manager connection pooling with PyMySQL.
  - `routes/`: Dedicated REST endpoint blueprints.
  - `utils/`: JWT authorization, input validators, secure file uploads, standardized response builders.

### AI / NLP Subsystem
- **Parser (`parser.py`)**: Multi-format document text extractor with header recognition for structural section detection (Summary, Skills, Experience, Education, Projects).
- **Skill Extractor (`skill_extractor.py`)**: Taxonomy pattern matching with synonym aliases and context-weighted confidence scoring.
- **Resume Scorer (`resume_scorer.py`)**: 0-100 ATS health scorer evaluating section completeness, quantifiable impact metrics, action verbs, and contact info.
- **Job Matcher (`matcher.py`)**: Multi-factor explainable algorithm combining TF-IDF cosine text similarity (30%), skill overlap (45%), experience match (15%), and education match (10%).
- **Career Coach Assistant (`assistant.py`)**: Grounded chat engine referencing student's real profile data with 100% offline local fallback.
