import os
import time
import pymysql
from playwright.sync_api import sync_playwright

OUTPUT_DIR = r"d:\resume_ai\report_screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def setup_demo_accounts_in_db():
    print("[*] Ensuring student & company demo accounts are properly registered in MySQL...")
    conn = pymysql.connect(host='localhost', user='root', password='', database='ai_resume_matcher')
    cursor = conn.cursor()

    from werkzeug.security import generate_password_hash
    pwd_hash = generate_password_hash("aswin@2006WEB")

    # 1. Student: ASWIN KUMAR
    cursor.execute("SELECT id FROM users WHERE email='cseaswin@gmail.com'")
    row = cursor.fetchone()
    if not row:
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, role, status) VALUES (%s, %s, %s, %s, %s)",
            ("ASWIN KUMAR", "cseaswin@gmail.com", pwd_hash, "student", "active")
        )
        student_user_id = cursor.lastrowid
        cursor.execute(
            """INSERT INTO student_profiles 
               (user_id, phone, college, degree, graduation_year, experience, location, bio) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (student_user_id, "9361109518",
             "Velammal College of Engineering and Technology", "B.E. Computer Science and Engineering",
             2026, "Entry Level (0-1 yrs)", "Madurai, Tamil Nadu, India",
             "Full-Stack Web & App Developer with expertise in Vue.js, React, Node.js, Python, Flask, and MySQL.")
        )
    else:
        student_user_id = row[0]
        cursor.execute("UPDATE users SET password_hash=%s, status='active' WHERE id=%s", (pwd_hash, student_user_id))

    # 2. Company: ZetHub
    cursor.execute("SELECT id FROM users WHERE email='hr@zethub.in'")
    crow = cursor.fetchone()
    if not crow:
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, role, status) VALUES (%s, %s, %s, %s, %s)",
            ("ZetHub", "hr@zethub.in", pwd_hash, "company", "active")
        )
        company_user_id = cursor.lastrowid
        cursor.execute(
            """INSERT INTO company_profiles 
               (user_id, company_name, company_email, phone, website, industry, location, description, verified) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (company_user_id, "ZetHub IT Solutions", "hr@zethub.in", "+91 9361109518",
             "https://zethub.in", "Software & Cloud AI", "Madurai, Tamil Nadu, India",
             "Leading software and IT solutions provider specializing in full stack web platforms, AI applications, and cloud architecture.", 1)
        )
    else:
        company_user_id = crow[0]
        cursor.execute("UPDATE users SET password_hash=%s, status='active' WHERE id=%s", (pwd_hash, company_user_id))

    conn.commit()
    conn.close()
    print("[✓] Demo accounts ready.")

def execute_capture_sequence():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            device_scale_factor=1.25
        )
        page = context.new_page()

        print("\n--- STEP 1: Student Registration Screen ---")
        page.goto("http://localhost:5173/register", wait_until="networkidle")
        time.sleep(1)
        page.fill("input[placeholder*='Jane Doe']", "ASWIN KUMAR")
        page.fill("input[placeholder*='jane@example.com']", "cseaswin@gmail.com")
        pwds = page.locator("input[type='password']").all()
        if len(pwds) >= 2:
            pwds[0].fill("aswin@2006WEB")
            pwds[1].fill("aswin@2006WEB")
        col_in = page.locator("input[placeholder*='Stanford']").first
        if col_in.is_visible():
            col_in.fill("Velammal College of Engineering and Technology")
        time.sleep(0.5)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "01_student_registration.png"))
        print("✓ Captured 01_student_registration.png")

        print("\n--- STEP 2: Student Login Screen ---")
        page.goto("http://localhost:5173/login", wait_until="networkidle")
        time.sleep(1)
        page.locator("input[type='email']").first.fill("cseaswin@gmail.com")
        page.locator("input[type='password']").first.fill("aswin@2006WEB")
        time.sleep(0.5)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "02_student_login.png"))
        print("✓ Captured 02_student_login.png")

        # Perform Login
        page.locator("button[type='submit']").first.click()
        page.wait_for_url("**/student/dashboard", timeout=12000)
        time.sleep(2)

        print("\n--- STEP 3: Student Dashboard ---")
        page.screenshot(path=os.path.join(OUTPUT_DIR, "03_student_dashboard.png"))
        print("✓ Captured 03_student_dashboard.png")

        print("\n--- STEP 4: Student Profile ---")
        page.goto("http://localhost:5173/student/profile", wait_until="networkidle")
        time.sleep(1.5)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "04_student_profile.png"))
        print("✓ Captured 04_student_profile.png")

        print("\n--- STEP 5: Resume Upload Interface ---")
        page.goto("http://localhost:5173/student/resume", wait_until="networkidle")
        time.sleep(1.5)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "05_resume_upload_view.png"))
        print("✓ Captured 05_resume_upload_view.png")

        print("\n--- STEP 6: Uploading Real Student Resume (PDF) ---")
        resume_pdf_path = r"d:\resume_ai\Aswin_Kumar_Resume.pdf"
        # If upload modal or dropzone is active
        modal_btn = page.locator("button:has-text('Upload New Resume')").first
        if modal_btn.is_visible():
            modal_btn.click()
            time.sleep(0.5)
        
        file_input = page.locator("input[type='file']").first
        file_input.set_input_files(resume_pdf_path)
        time.sleep(3.5) # Allow NLP engine to parse and extract skills
        page.screenshot(path=os.path.join(OUTPUT_DIR, "06_resume_upload_processing.png"))
        print("✓ Captured 06_resume_upload_processing.png")

        time.sleep(2)
        page.goto("http://localhost:5173/student/resume", wait_until="networkidle")
        time.sleep(2)

        print("\n--- STEP 7: AI Resume Analysis Audit ---")
        page.screenshot(path=os.path.join(OUTPUT_DIR, "07_ai_resume_analysis.png"))
        print("✓ Captured 07_ai_resume_analysis.png")

        print("\n--- STEP 8: Extracted Skills Matrix ---")
        page.goto("http://localhost:5173/student/skills", wait_until="networkidle")
        time.sleep(2)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "08_extracted_skills_matrix.png"))
        print("✓ Captured 08_extracted_skills_matrix.png")

        print("\n--- STEP 9: Detailed ATS Score & Breakdown ---")
        page.goto("http://localhost:5173/student/resume", wait_until="networkidle")
        time.sleep(1.5)
        page.evaluate("window.scrollTo(0, 420)")
        time.sleep(1)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "09_resume_score_breakdown.png"))
        page.evaluate("window.scrollTo(0, 0)")
        print("✓ Captured 09_resume_score_breakdown.png")

        # Clear session for Company
        context.clear_cookies()
        page.evaluate("() => localStorage.clear()")

        print("\n--- STEP 10: Company Registration Form ---")
        page.goto("http://localhost:5173/register", wait_until="networkidle")
        time.sleep(1)
        company_tab = page.locator("button:has-text('Employer'), button:has-text('Company')").first
        if company_tab.is_visible():
            company_tab.click()
            time.sleep(0.5)
        page.fill("input[placeholder*='Acme Technologies']", "ZetHub IT Solutions")
        page.fill("input[placeholder*='careers@acme.com']", "hr@zethub.in")
        cpwds = page.locator("input[type='password']").all()
        if len(cpwds) >= 2:
            cpwds[0].fill("aswin@2006WEB")
            cpwds[1].fill("aswin@2006WEB")
        time.sleep(0.5)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "10_company_registration.png"))
        print("✓ Captured 10_company_registration.png")

        print("\n--- STEP 11: Company Login Screen ---")
        page.goto("http://localhost:5173/login", wait_until="networkidle")
        time.sleep(1)
        page.locator("input[type='email']").first.fill("hr@zethub.in")
        page.locator("input[type='password']").first.fill("aswin@2006WEB")
        time.sleep(0.5)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "11_company_login.png"))
        print("✓ Captured 11_company_login.png")

        # Perform Company Login
        page.locator("button[type='submit']").first.click()
        page.wait_for_url("**/company/dashboard", timeout=12000)
        time.sleep(2)

        print("\n--- STEP 12: ZetHub Company Dashboard ---")
        page.screenshot(path=os.path.join(OUTPUT_DIR, "12_zethub_dashboard.png"))
        print("✓ Captured 12_zethub_dashboard.png")

        print("\n--- STEP 13: Create Job Form ---")
        page.goto("http://localhost:5173/company/jobs/create", wait_until="networkidle")
        time.sleep(1.5)
        page.fill("input[placeholder*='Senior Python']", "Full Stack Developer / AI-ML Developer Intern")
        page.fill("input[placeholder*='San Francisco']", "Madurai, Tamil Nadu (Hybrid / On-site)")
        page.fill("input[placeholder*='2-4 years']", "0-1 years")
        page.fill("input[placeholder*='Python, Flask, Vue.js']", "React.js, Vue.js, Node.js, Python, Flask, MySQL, JavaScript, HTML, CSS, REST API, Git")
        page.fill("input[placeholder*='Docker, AWS']", "NLP, Scikit-learn, Electron.js, Firebase")
        
        salary_inputs = page.locator("input[type='number']").all()
        if len(salary_inputs) >= 2:
            salary_inputs[0].fill("400000")
            salary_inputs[1].fill("750000")
            
        desc_area = page.locator("textarea[placeholder*='overview']").first
        if desc_area.is_visible():
            desc_area.fill("ZetHub IT Solutions is seeking a talented Full Stack & AI-ML Developer Intern. You will build cutting-edge web applications using Vue.js, React, Node.js, Python Flask, and MySQL, with integration to machine learning recommendation models.")
        
        req_area = page.locator("textarea[placeholder*='requirements']").first
        if req_area.is_visible():
            req_area.fill("• Hands-on experience with Vue.js, React.js, and Modern JavaScript\n• Server-side API development with Python (Flask) or Node.js\n• Relational database skills in MySQL\n• Familiarity with Git, REST APIs, and NLP fundamentals")

        time.sleep(0.5)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "13_create_job_form.png"))
        print("✓ Captured 13_create_job_form.png")

        # Submit Job Form
        post_btn = page.locator("button[type='submit']").first
        if post_btn.is_visible():
            post_btn.click()
            time.sleep(2)

        print("\n--- STEP 14: ZetHub Manage Jobs List ---")
        page.goto("http://localhost:5173/company/jobs", wait_until="networkidle")
        time.sleep(2)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "14_zethub_posted_jobs.png"))
        print("✓ Captured 14_zethub_posted_jobs.png")

        # Clear session for Student
        context.clear_cookies()
        page.evaluate("() => localStorage.clear()")

        print("\n--- STEP 15: Student Login & Job Matching ---")
        page.goto("http://localhost:5173/login", wait_until="networkidle")
        time.sleep(1)
        page.locator("input[type='email']").first.fill("cseaswin@gmail.com")
        page.locator("input[type='password']").first.fill("aswin@2006WEB")
        page.locator("button[type='submit']").first.click()
        page.wait_for_url("**/student/dashboard", timeout=12000)
        time.sleep(1.5)

        print("\n--- STEP 16: Job Listings with AI Match Badges ---")
        page.goto("http://localhost:5173/jobs", wait_until="networkidle")
        time.sleep(2.5)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "15_job_listings_with_ai_matches.png"))
        print("✓ Captured 15_job_listings_with_ai_matches.png")

        print("\n--- STEP 17: ZetHub Job Detail & AI Match Breakdown ---")
        zethub_job_link = page.locator("text=Full Stack Developer / AI-ML Developer Intern").first
        if zethub_job_link.is_visible():
            zethub_job_link.click()
            time.sleep(2)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "16_job_ai_match_details.png"))
        print("✓ Captured 16_job_ai_match_details.png")

        print("\n--- STEP 18: Applying for ZetHub Job ---")
        apply_btn = page.locator("button:has-text('Apply for this Role')").first
        if apply_btn.is_visible() and not apply_btn.is_disabled():
            apply_btn.click()
            time.sleep(1)
            submit_modal_btn = page.locator("button:has-text('Submit Application')").first
            if submit_modal_btn.is_visible():
                submit_modal_btn.click()
                time.sleep(2)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "17_student_application_submitted.png"))
        print("✓ Captured 17_student_application_submitted.png")

        print("\n--- STEP 19: Student Applications Dashboard ---")
        page.goto("http://localhost:5173/student/applications", wait_until="networkidle")
        time.sleep(2)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "18_student_applications_view.png"))
        print("✓ Captured 18_student_applications_view.png")

        # Clear session for Company
        context.clear_cookies()
        page.evaluate("() => localStorage.clear()")

        print("\n--- STEP 20: Company Applicants View (ZetHub) ---")
        page.goto("http://localhost:5173/login", wait_until="networkidle")
        time.sleep(1)
        page.locator("input[type='email']").first.fill("hr@zethub.in")
        page.locator("input[type='password']").first.fill("aswin@2006WEB")
        page.locator("button[type='submit']").first.click()
        page.wait_for_url("**/company/dashboard", timeout=12000)
        time.sleep(1.5)

        page.goto("http://localhost:5173/company/applicants", wait_until="networkidle")
        time.sleep(2.5)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "19_company_applicants_view.png"))
        print("✓ Captured 19_company_applicants_view.png")

        print("\n--- STEP 21: Shortlisting Candidate ---")
        status_dropdown = page.locator("select.badge-select").first
        if status_dropdown.is_visible():
            status_dropdown.select_option("Shortlisted")
            time.sleep(2)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "20_applicant_shortlisted_by_company.png"))
        print("✓ Captured 20_applicant_shortlisted_by_company.png")

        # Clear session for Student verification
        context.clear_cookies()
        page.evaluate("() => localStorage.clear()")

        print("\n--- STEP 22: Verified Shortlisted Status on Student Account ---")
        page.goto("http://localhost:5173/login", wait_until="networkidle")
        time.sleep(1)
        page.locator("input[type='email']").first.fill("cseaswin@gmail.com")
        page.locator("input[type='password']").first.fill("aswin@2006WEB")
        page.locator("button[type='submit']").first.click()
        page.wait_for_url("**/student/dashboard", timeout=12000)
        time.sleep(1.5)
        page.goto("http://localhost:5173/student/applications", wait_until="networkidle")
        time.sleep(2)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "21_student_shortlisted_confirmed.png"))
        print("✓ Captured 21_student_shortlisted_confirmed.png")

        print("\n--- STEP 23: phpMyAdmin Database & Tables ---")
        try:
            page.goto("http://localhost/phpmyadmin/index.php?route=/database/structure&db=ai_resume_matcher", timeout=8000)
            time.sleep(2.5)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "22_phpmyadmin_db_structure.png"))
            print("✓ Captured 22_phpmyadmin_db_structure.png")

            page.goto("http://localhost/phpmyadmin/index.php?route=/sql&db=ai_resume_matcher&table=users&pos=0", timeout=8000)
            time.sleep(2)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "23_phpmyadmin_users_table.png"))
            print("✓ Captured 23_phpmyadmin_users_table.png")

            page.goto("http://localhost/phpmyadmin/index.php?route=/sql&db=ai_resume_matcher&table=jobs&pos=0", timeout=8000)
            time.sleep(2)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "24_phpmyadmin_jobs_table.png"))
            print("✓ Captured 24_phpmyadmin_jobs_table.png")

            page.goto("http://localhost/phpmyadmin/index.php?route=/sql&db=ai_resume_matcher&table=applications&pos=0", timeout=8000)
            time.sleep(2)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "25_phpmyadmin_applications_table.png"))
            print("✓ Captured 25_phpmyadmin_applications_table.png")
        except Exception as e:
            print(f"phpMyAdmin notice: {e}")

        browser.close()
        print("\n==========================================")
        print("[✓] ALL 25 SCREENSHOTS CAPTURED SUCCESSFULLY!")
        print("==========================================")

if __name__ == "__main__":
    setup_demo_accounts_in_db()
    execute_capture_sequence()
