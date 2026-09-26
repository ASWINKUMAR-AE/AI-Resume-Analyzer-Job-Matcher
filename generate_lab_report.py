import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCX_OUTPUT_PATH = r"d:\resume_ai\AI_Resume_Analyzer_Job_Matcher_Lab_Report.docx"
SCREENSHOTS_DIR = r"d:\resume_ai\report_screenshots"
VCET_LOGO_PATH = os.path.join(SCREENSHOTS_DIR, "extracted_img_0_0.png")

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_page_border(section):
    sectPr = section._sectPr
    pgBorders = parse_xml(
        f'<w:pgBorders {nsdecls("w")}>'
        '<w:top w:val="single" w:sz="8" w:space="20" w:color="000000"/>'
        '<w:left w:val="single" w:sz="8" w:space="20" w:color="000000"/>'
        '<w:bottom w:val="single" w:sz="8" w:space="20" w:color="000000"/>'
        '<w:right w:val="single" w:sz="8" w:space="20" w:color="000000"/>'
        '</w:pgBorders>'
    )
    sectPr.append(pgBorders)

def create_report():
    doc = Document()

    # Configure Section: A4 Portrait, 0.8 in margins
    section = doc.sections[0]
    section.page_width = Inches(8.27)   # A4 width
    section.page_height = Inches(11.69) # A4 height
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.85)
    section.right_margin = Inches(0.85)
    add_page_border(section)

    # Base style
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(11)
    font.color.rgb = RGBColor(0, 0, 0)

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(18)
    run = p.add_run("AI RESUME ANALYZER & JOB MATCHER")
    run.bold = True
    run.font.size = Pt(15)

    # College Logo 1
    if os.path.exists(VCET_LOGO_PATH):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(0)
        p_logo.paragraph_format.space_after = Pt(16)
        p_logo.add_run().add_picture(VCET_LOGO_PATH, width=Inches(1.3))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run("MINI PROJECT")
    run.bold = True
    run.font.size = Pt(13)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run("21CS410-Artificial Intelligence and Machine Learning Laboratory")
    run.bold = True
    run.font.size = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(36)
    run = p.add_run("(for the Academic Year 2025-26)")
    run.italic = True
    run.font.size = Pt(11)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(36)
    run = p.add_run("Done by")
    run.italic = True
    run.font.size = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(36)
    run = p.add_run("ASWIN KUMAR T A – 913124104302")
    run.bold = True
    run.font.size = Pt(13)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run("Department of Computer Science and Engineering")
    run.bold = True
    run.font.size = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run("VELAMMAL COLLEGE OF ENGINEERING AND TECHNOLOGY")
    run.bold = True
    run.font.size = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run("VIRAGANOOR, MADURAI-625009")
    run.bold = True
    run.font.size = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(14)
    run = p.add_run("(AUTONOMOUS)")
    run.bold = True
    run.font.size = Pt(12)

    if os.path.exists(VCET_LOGO_PATH):
        p_logo2 = doc.add_paragraph()
        p_logo2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo2.paragraph_format.space_before = Pt(0)
        p_logo2.paragraph_format.space_after = Pt(0)
        p_logo2.add_run().add_picture(VCET_LOGO_PATH, width=Inches(1.15))

    doc.add_page_break()

    # =========================================================================
    # PAGE 2: BONAFIDE CERTIFICATE
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run("VELAMMAL COLLEGE OF ENGINEERING AND TECHNOLOGY,")
    run.bold = True
    run.font.size = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run("MADURAI-625009.")
    run.bold = True
    run.font.size = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run("(Autonomous)")
    run.font.size = Pt(11)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING")
    run.bold = True
    run.font.size = Pt(12)

    if os.path.exists(VCET_LOGO_PATH):
        p_logo3 = doc.add_paragraph()
        p_logo3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo3.paragraph_format.space_before = Pt(0)
        p_logo3.paragraph_format.space_after = Pt(12)
        p_logo3.add_run().add_picture(VCET_LOGO_PATH, width=Inches(1.2))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(16)
    run = p.add_run("2025-26")
    run.bold = True
    run.font.size = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(10)
    run = p.add_run("BONAFIDE CERTIFICATE")
    run.bold = True
    run.font.size = Pt(13)
    run.font.color.rgb = RGBColor(16, 76, 112) # Subtle teal/blue matching reference

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(16)
    run = p.add_run("This is to certify that the mini project work titled")
    run.italic = True
    run.font.size = Pt(11)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(16)
    run = p.add_run("AI RESUME ANALYZER & JOB MATCHER")
    run.bold = True
    run.font.size = Pt(13)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(16)
    run = p.add_run("Was done by")
    run.italic = True
    run.font.size = Pt(11)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(24)
    run = p.add_run("ASWIN KUMAR T A – 913124104302")
    run.bold = True
    run.font.size = Pt(13)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(120)
    p.paragraph_format.line_spacing = 1.3
    run = p.add_run(
        "of fourth semester –Computer Science and Engineering Department in partial fulfillment of "
        "the requirement of 21CS410-Artificial Intelligence and Machine Learning Laboratory during the year 2025-26."
    )
    run.font.size = Pt(11)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run("Course in-charge")
    run.bold = True
    run.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 3: AIM & CONCEPTS INVOLVED
    # =========================================================================
    p_header = doc.add_paragraph()
    p_header.paragraph_format.space_before = Pt(0)
    p_header.paragraph_format.space_after = Pt(2)
    run1 = p_header.add_run("EX .NO: 10")
    run1.bold = True
    run1.font.size = Pt(11)
    run_space = p_header.add_run("                            ")
    run2 = p_header.add_run("AI RESUME ANALYZER & JOB MATCHER")
    run2.bold = True
    run2.font.size = Pt(11)

    p_date = doc.add_paragraph()
    p_date.paragraph_format.space_before = Pt(0)
    p_date.paragraph_format.space_after = Pt(16)
    run_d = p_date.add_run("DATE: 26/09/26")
    run_d.bold = True
    run_d.font.size = Pt(11)

    # AIM
    p_aim_t = doc.add_paragraph()
    p_aim_t.paragraph_format.space_before = Pt(6)
    p_aim_t.paragraph_format.space_after = Pt(4)
    run_aim_h = p_aim_t.add_run("AIM:")
    run_aim_h.bold = True
    run_aim_h.underline = True
    run_aim_h.font.size = Pt(11)

    p_aim = doc.add_paragraph()
    p_aim.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_aim.paragraph_format.space_before = Pt(0)
    p_aim.paragraph_format.space_after = Pt(14)
    p_aim.paragraph_format.line_spacing = 1.2
    run = p_aim.add_run(
        "To design and develop an AI-powered Resume Analyzer and Job Matcher that uses Natural Language Processing "
        "and Machine Learning techniques to analyze resumes, extract candidate skills, calculate resume quality, "
        "and match students with suitable job opportunities while providing separate interfaces for students and companies."
    )
    run.font.size = Pt(10.5)

    # CONCEPTS INVOLVED
    p_con_t = doc.add_paragraph()
    p_con_t.paragraph_format.space_before = Pt(6)
    p_con_t.paragraph_format.space_after = Pt(6)
    run_con_h = p_con_t.add_run("CONCEPTS INVOLVED:")
    run_con_h.bold = True
    run_con_h.underline = True
    run_con_h.font.size = Pt(11)

    concepts = [
        ("• Artificial Intelligence and Machine Learning (AI/ML):",
         "Provides automated intelligence for career readiness, resume scoring, and profile-job vector matching."),
        ("• Natural Language Processing (NLP):",
         "Used to clean, tokenize, and extract meaningful semantic textual patterns from unstructured resume files and job descriptions."),
        ("• Resume Text Extraction:",
         "Multi-format document parsing engine supporting PDF, DOCX, and TXT using PyPDF and python-docx."),
        ("• Skill Extraction Taxonomy:",
         "Hierarchical domain taxonomy matching candidate skills across Web, Mobile, Backend, Database, Cloud, and AI categories."),
        ("• TF-IDF Vectorization:",
         "Transforms document corpus into statistical Term Frequency-Inverse Document Frequency numerical feature vectors."),
        ("• Cosine Similarity Metric:",
         "Calculates angular cosine distance between candidate resume vectors and employer job vectors to produce an accurate match percentage."),
        ("• Resume Quality & ATS Health Scoring:",
         "Evaluates section completeness, formatting hygiene, keyword density, and technical depth with explainable suggestions."),
        ("• Role-Based Access Control (RBAC):",
         "Ensures isolated security, authentication, and tailored dashboards for Students, Employers, and Administrators."),
        ("• RESTful API Architecture (Flask Backend):",
         "Handles server-side business logic, JWT authentication, NLP execution pipelines, and database interactions."),
        ("• Relational Database Management (MySQL & XAMPP):",
         "Maintains ACID-compliant structured storage for users, profiles, resumes, skills, job postings, and applications.")
    ]

    for title, desc in concepts:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.space_before = Pt(2)
        p_c.paragraph_format.space_after = Pt(2)
        p_c.paragraph_format.line_spacing = 1.15
        r1 = p_c.add_run(title + "\n")
        r1.bold = True
        r1.font.size = Pt(10.5)
        r2 = p_c.add_run("        " + desc)
        r2.font.size = Pt(10)

    doc.add_page_break()

    # =========================================================================
    # PAGE 4+: FILES USED & PROGRAM SOURCE CODE
    # =========================================================================
    p_f_t = doc.add_paragraph()
    p_f_t.paragraph_format.space_before = Pt(0)
    p_f_t.paragraph_format.space_after = Pt(6)
    r_f = p_f_t.add_run("FILES USED:")
    r_f.bold = True
    r_f.underline = True
    r_f.font.size = Pt(11)

    files_list = [
        ("Frontend (Vue 3 + Vite):", [
            "frontend/src/views/public/LandingView.vue",
            "frontend/src/views/public/LoginView.vue",
            "frontend/src/views/public/RegisterView.vue",
            "frontend/src/views/student/StudentDashboardView.vue",
            "frontend/src/views/student/ResumeUploadView.vue",
            "frontend/src/views/student/SkillsView.vue",
            "frontend/src/views/student/JobDetailView.vue",
            "frontend/src/views/company/CompanyDashboardView.vue",
            "frontend/src/views/company/CreateJobView.vue",
            "frontend/src/views/company/ApplicantsView.vue"
        ]),
        ("Backend (Python + Flask):", [
            "backend/app.py",
            "backend/config.py",
            "backend/database/db.py",
            "backend/routes/auth_routes.py",
            "backend/routes/resume_routes.py",
            "backend/routes/job_routes.py",
            "backend/routes/application_routes.py"
        ]),
        ("AI / ML & NLP Engine:", [
            "backend/ai/resume_parser.py",
            "backend/ai/skill_extractor.py",
            "backend/ai/matcher.py",
            "backend/ai/skills_taxonomy.py"
        ]),
        ("Database & Schema:", [
            "database/schema.sql",
            "backend/init_db.py"
        ])
    ]

    for category, flist in files_list:
        p_cat = doc.add_paragraph()
        p_cat.paragraph_format.space_before = Pt(3)
        p_cat.paragraph_format.space_after = Pt(2)
        r_cat = p_cat.add_run(category)
        r_cat.bold = True
        r_cat.font.size = Pt(10.5)

        for fname in flist:
            p_file = doc.add_paragraph()
            p_file.paragraph_format.space_before = Pt(0)
            p_file.paragraph_format.space_after = Pt(1)
            p_file.paragraph_format.left_indent = Inches(0.25)
            r_fname = p_file.add_run("• " + fname)
            r_fname.font.name = 'Consolas'
            r_fname.font.size = Pt(9.5)

    p_prog_t = doc.add_paragraph()
    p_prog_t.paragraph_format.space_before = Pt(12)
    p_prog_t.paragraph_format.space_after = Pt(6)
    r_pr = p_prog_t.add_run("PROGRAM:")
    r_pr.bold = True
    r_pr.underline = True
    r_pr.font.size = Pt(11)

    code_sections = [
        ("db.py (Database Connection & MySQL Pool):", """import pymysql
from dbutils.pooled_db import PooledDB
from config import Config

pool = PooledDB(
    creator=pymysql,
    maxconnections=10,
    mincached=2,
    host=Config.DB_HOST,
    port=Config.DB_PORT,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    database=Config.DB_NAME,
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True
)

def get_db():
    return pool.connection()"""),

        ("auth_routes.py (Authentication & JWT Token Generation):", """from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, datetime
from config import Config
from database.db import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    role = data.get('role', 'student')
    
    if not name or not email or not password:
        return jsonify({"success": False, "message": "Missing required fields"}), 400
        
    pwd_hash = generate_password_hash(password)
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
            (name, email, pwd_hash, role)
        )
        user_id = cursor.lastrowid
        if role == 'student':
            cursor.execute("INSERT INTO student_profiles (user_id, college, degree) VALUES (%s, %s, %s)",
                           (user_id, data.get('college'), data.get('degree')))
        elif role == 'company':
            cursor.execute("INSERT INTO company_profiles (user_id, company_name) VALUES (%s, %s)",
                           (user_id, name))
    return jsonify({"success": True, "message": "Registered successfully"}), 201"""),

        ("resume_parser.py (Multi-Format Resume Text Extraction):", """import os
from pypdf import PdfReader
import docx

def extract_text_from_file(file_path, file_type):
    file_type = file_type.lower()
    if file_type == 'pdf':
        text = ""
        reader = PdfReader(file_path)
        for page in reader.pages:
            t = page.extract_text()
            if t: text += t + "\\n"
        return text.strip()
    elif file_type in ['docx', 'doc']:
        doc = docx.Document(file_path)
        text = "\\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        return text.strip()
    elif file_type == 'txt':
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read().strip()
    return \"\""""),

        ("skill_extractor.py (Taxonomy-Based NLP Skill Extraction):", """import re
from ai.skills_taxonomy import SKILLS_TAXONOMY

def extract_skills_from_text(raw_text):
    clean_text = raw_text.lower()
    extracted_skills = []
    
    for category, skill_dict in SKILLS_TAXONOMY.items():
        for canonical_skill, aliases in skill_dict.items():
            pattern = r'\\b' + re.escape(canonical_skill.lower()) + r'\\b'
            if re.search(pattern, clean_text):
                extracted_skills.append({
                    "skill_name": canonical_skill,
                    "category": category,
                    "confidence": 0.95
                })
                continue
            for alias in aliases:
                if re.search(r'\\b' + re.escape(alias.lower()) + r'\\b', clean_text):
                    extracted_skills.append({
                        "skill_name": canonical_skill,
                        "category": category,
                        "confidence": 0.90
                    })
                    break
    return extracted_skills"""),

        ("matcher.py (TF-IDF & Cosine Similarity Job Matching Pipeline):", """from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_job_compatibility(candidate_skills, resume_text, job_skills, job_description):
    cand_set = set([s.lower().strip() for s in candidate_skills])
    job_set = set([s.lower().strip() for s in job_skills])
    
    matched = cand_set.intersection(job_set)
    missing = job_set - cand_set
    
    # 1. Skill Match Ratio (60% weight)
    skill_score = (len(matched) / len(job_set)) * 100.0 if job_set else 70.0
    
    # 2. TF-IDF Cosine Semantic Similarity (40% weight)
    vectorizer = TfidfVectorizer(stop_words='english')
    corpus = [resume_text or " ".join(candidate_skills), job_description or " ".join(job_skills)]
    tfidf_matrix = vectorizer.fit_transform(corpus)
    cosine_sim = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]) * 100.0
    
    overall_match = round(0.60 * skill_score + 0.40 * cosine_sim, 1)
    
    return {
        "match_score": min(100.0, max(0.0, overall_match)),
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "skill_score": round(skill_score, 1),
        "semantic_similarity": round(cosine_sim, 1)
    }"""),

        ("job_routes.py (Company Job Posting & AI Compatibility Evaluation):", """from flask import Blueprint, request, jsonify
from database.db import get_db
from ai.matcher import calculate_job_compatibility

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/create', methods=['POST'])
def create_job():
    data = request.get_json() or {}
    company_id = data.get('company_id')
    title = data.get('title')
    skills = data.get('skills')
    desc = data.get('description')
    
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute(
            \"\"\"INSERT INTO jobs 
               (company_id, title, job_type, location, experience_required, skills, description, salary_min, salary_max) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)\"\"\",
            (company_id, title, data.get('job_type', 'Full Time'), data.get('location'),
             data.get('experience_required'), skills, desc, data.get('salary_min'), data.get('salary_max'))
        )
        job_id = cursor.lastrowid
    return jsonify({"success": True, "job_id": job_id, "message": "Job published"}), 201""")
    ]

    for title, code_str in code_sections:
        p_c_t = doc.add_paragraph()
        p_c_t.paragraph_format.space_before = Pt(8)
        p_c_t.paragraph_format.space_after = Pt(2)
        r_c_t = p_c_t.add_run(title)
        r_c_t.bold = True
        r_c_t.font.name = 'Consolas'
        r_c_t.font.size = Pt(10)

        # Code block
        p_code = doc.add_paragraph()
        p_code.paragraph_format.space_before = Pt(0)
        p_code.paragraph_format.space_after = Pt(6)
        p_code.paragraph_format.line_spacing = 1.05
        p_code.paragraph_format.left_indent = Inches(0.15)
        
        r_code = p_code.add_run(code_str)
        r_code.font.name = 'Consolas'
        r_code.font.size = Pt(8.5)

    doc.add_page_break()

    # =========================================================================
    # OUTPUT: SCREENSHOTS
    # =========================================================================
    p_out_t = doc.add_paragraph()
    p_out_t.paragraph_format.space_before = Pt(0)
    p_out_t.paragraph_format.space_after = Pt(12)
    r_out = p_out_t.add_run("OUTPUT:")
    r_out.bold = True
    r_out.underline = True
    r_out.font.size = Pt(12)

    screenshots_data = [
        ("01_student_registration.png", "Fig 1: Student Account Registration Interface"),
        ("02_student_login.png", "Fig 2: Student Authentication & Sign In"),
        ("03_student_dashboard.png", "Fig 3: Student Interactive Dashboard"),
        ("04_student_profile.png", "Fig 4: Student Technical Profile & Details"),
        ("05_resume_upload_view.png", "Fig 5: AI Resume Analyzer & ATS Audit Dropzone"),
        ("06_resume_upload_processing.png", "Fig 6: Resume Upload & Real-time NLP Processing"),
        ("07_ai_resume_analysis.png", "Fig 7: AI Resume Health Score & Comprehensive Audit"),
        ("08_extracted_skills_matrix.png", "Fig 8: Extracted Candidate Technical Skills Matrix"),
        ("09_resume_score_breakdown.png", "Fig 9: Resume ATS Quality Breakdown & Action Items"),
        ("10_company_registration.png", "Fig 10: ZetHub Employer Account Registration"),
        ("11_company_login.png", "Fig 11: ZetHub Company Sign In"),
        ("12_zethub_dashboard.png", "Fig 12: ZetHub Recruitment Dashboard"),
        ("13_create_job_form.png", "Fig 13: Job Creation Form with Target Skills & Attributes"),
        ("14_zethub_posted_jobs.png", "Fig 14: ZetHub Active Job Postings Management"),
        ("15_job_listings_with_ai_matches.png", "Fig 15: Student Job Board with Dynamic AI Match Percentages"),
        ("16_job_ai_match_details.png", "Fig 16: Explainable AI Job Compatibility Breakdown"),
        ("17_student_application_submitted.png", "Fig 17: Successful Student Job Application Submission"),
        ("18_student_applications_view.png", "Fig 18: Student Applied Jobs & Status Tracker"),
        ("19_company_applicants_view.png", "Fig 19: AI-Ranked Candidate List on ZetHub Portal"),
        ("20_applicant_shortlisted_by_company.png", "Fig 20: Candidate Shortlisting in Hiring Pipeline"),
        ("21_student_shortlisted_confirmed.png", "Fig 21: Updated Application Status Reflected to Student"),
        ("22_phpmyadmin_db_structure.png", "Fig 22: MySQL Database Structure in phpMyAdmin (ai_resume_matcher)"),
        ("23_phpmyadmin_users_table.png", "Fig 23: MySQL Users Table Data Records"),
        ("24_phpmyadmin_jobs_table.png", "Fig 24: MySQL Published Jobs Table Data"),
        ("25_phpmyadmin_applications_table.png", "Fig 25: MySQL Job Applications Table Records")
    ]

    for img_name, caption in screenshots_data:
        img_path = os.path.join(SCREENSHOTS_DIR, img_name)
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.paragraph_format.keep_with_next = True
            
            # Width scaled for standard A4 page width with margins (around 6.0 inches)
            p_img.add_run().add_picture(img_path, width=Inches(5.8))

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(1)
            p_cap.paragraph_format.space_after = Pt(14)
            r_cap = p_cap.add_run(caption)
            r_cap.bold = True
            r_cap.font.size = Pt(9.5)

    doc.add_page_break()

    # =========================================================================
    # RESULT & REFERENCES
    # =========================================================================
    p_res_t = doc.add_paragraph()
    p_res_t.paragraph_format.space_before = Pt(0)
    p_res_t.paragraph_format.space_after = Pt(6)
    r_res_h = p_res_t.add_run("RESULT:")
    r_res_h.bold = True
    r_res_h.underline = True
    r_res_h.font.size = Pt(11)

    p_res_intro = doc.add_paragraph()
    p_res_intro.paragraph_format.space_before = Pt(2)
    p_res_intro.paragraph_format.space_after = Pt(4)
    p_res_intro.add_run("The system successfully:")

    res_points = [
        "Provides secure multi-role registration and authentication for Students, Companies, and Administrators.",
        "Parses unstructured resumes in PDF, DOCX, and TXT formats and extracts candidate profiles.",
        "Identifies and categorizes technical skills dynamically using an NLP taxonomy engine.",
        "Calculates an ATS health score with actionable suggestions for resume optimization.",
        "Enables employers (ZetHub) to create, publish, and manage structured job vacancies.",
        "Executes a TF-IDF and Cosine Similarity matching pipeline to compute exact candidate-job compatibility.",
        "Allows seamless student application submissions and company hiring pipeline management (Shortlisting).",
        "Ensures ACID-compliant persistent relational storage using MySQL and XAMPP."
    ]

    for pt in res_points:
        p_pt = doc.add_paragraph()
        p_pt.paragraph_format.space_before = Pt(1)
        p_pt.paragraph_format.space_after = Pt(2)
        p_pt.paragraph_format.left_indent = Inches(0.25)
        p_pt.paragraph_format.line_spacing = 1.15
        r_pt = p_pt.add_run("• " + pt)
        r_pt.font.size = Pt(10.5)

    p_res_sum = doc.add_paragraph()
    p_res_sum.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_res_sum.paragraph_format.space_before = Pt(8)
    p_res_sum.paragraph_format.space_after = Pt(24)
    p_res_sum.paragraph_format.line_spacing = 1.2
    r_sum = p_res_sum.add_run(
        "Thus, the mini project effectively integrates Artificial Intelligence, Machine Learning, Natural Language "
        "Processing, and MySQL database technologies to automate recruitment, simplify candidate evaluation, and optimize "
        "student-job matching."
    )
    r_sum.font.size = Pt(10.5)

    # REFERENCES
    p_ref_t = doc.add_paragraph()
    p_ref_t.paragraph_format.space_before = Pt(6)
    p_ref_t.paragraph_format.space_after = Pt(6)
    r_ref_h = p_ref_t.add_run("REFERENCES:")
    r_ref_h.bold = True
    r_ref_h.underline = True
    r_ref_h.font.size = Pt(11)

    references = [
        "1. Scikit-learn Machine Learning Library Documentation – https://scikit-learn.org/stable/",
        "2. Python Official Documentation – https://docs.python.org/3/",
        "3. Flask Web Development Framework Documentation – https://flask.palletsprojects.com/",
        "4. Vue.js Progressive JavaScript Framework – https://vuejs.org/guide/",
        "5. MySQL 8.0 Reference Manual – https://dev.mysql.com/doc/",
        "6. PyPDF & python-docx Documentation – https://pypdf.readthedocs.io/",
        "7. W3Schools & MDN Web Docs (JavaScript, CSS, HTML5) – https://developer.mozilla.org/"
    ]

    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(3)
        p_ref.paragraph_format.left_indent = Inches(0.25)
        r_ref = p_ref.add_run(ref)
        r_ref.font.size = Pt(10)

    doc.save(DOCX_OUTPUT_PATH)
    print(f"[✓] Document successfully generated: {DOCX_OUTPUT_PATH}")

if __name__ == "__main__":
    create_report()
