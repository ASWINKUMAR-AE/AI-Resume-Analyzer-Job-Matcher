import os
import time
import pymysql
from playwright.sync_api import sync_playwright

OUTPUT_DIR = r"d:\resume_ai\report_screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_workflow_and_capture():
    # Database check and cleanup/setup for demo users
    conn = pymysql.connect(host='localhost', user='root', password='', database='ai_resume_matcher')
    cursor = conn.cursor()
    
    # Check if student exists; if so, we can test login or fresh register
    cursor.execute("SELECT id FROM users WHERE email='cseaswin@gmail.com'")
    existing_student = cursor.fetchone()
    print(f"Existing student in DB: {existing_student}")

    cursor.execute("SELECT id FROM users WHERE email='hr@zethub.in'")
    existing_company = cursor.fetchone()
    print(f"Existing company in DB: {existing_company}")

    conn.close()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Create a browser context with high DPI and 1400x900 viewport
        context = browser.new_context(
            viewport={'width': 1366, 'height': 820},
            device_scale_factor=1.5
        )
        page = context.new_page()

        print("[1] Navigating to Home...")
        page.goto("http://localhost:5173", wait_until="networkidle")
        time.sleep(1)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "01_homepage.png"))

        print("[2] Navigating to Student Registration...")
        page.goto("http://localhost:5173/register", wait_until="networkidle")
        time.sleep(1)
        # Fill registration form
        page.fill("input#full_name", "Aswin Kumar")
        page.fill("input#username", "aswinkumar")
        page.fill("input#email", "cseaswin@gmail.com")
        page.fill("input#password", "aswin@2006WEB")
        page.fill("input#confirm_password", "aswin@2006WEB")
        time.sleep(1)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "02_student_registration.png"))

        # If user already registered, we can proceed to login, else submit
        print("[3] Navigating to Login...")
        page.goto("http://localhost:5173/login", wait_until="networkidle")
        page.fill("input#username", "cseaswin@gmail.com")
        page.fill("input#password", "aswin@2006WEB")
        time.sleep(1)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "03_student_login.png"))

        # Click login
        page.click("button[type='submit']")
        page.wait_for_url("**/student/dashboard", timeout=8000)
        time.sleep(2)
        print("[4] Student Dashboard...")
        page.screenshot(path=os.path.join(OUTPUT_DIR, "04_student_dashboard.png"))

        print("[5] Navigating to Resume Upload...")
        page.goto("http://localhost:5173/student/resume", wait_until="networkidle")
        time.sleep(1)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "05_resume_upload_page.png"))

        # Upload the resume PDF
        resume_pdf_path = r"d:\resume_ai\Aswin_Kumar_Resume.pdf"
        file_input = page.locator("input[type='file']")
        file_input.set_input_files(resume_pdf_path)
        time.sleep(2)
        print("[6] Resume Selected / Uploading...")
        page.screenshot(path=os.path.join(OUTPUT_DIR, "06_resume_selected.png"))

        # Click Analyze / Upload button
        upload_btn = page.locator("button:has-text('Analyze')").first
        if upload_btn.is_visible():
            upload_btn.click()
            time.sleep(4)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "07_resume_analysis_result.png"))

        print("[8] Navigating to Extracted Skills Matrix...")
        page.goto("http://localhost:5173/student/skills", wait_until="networkidle")
        time.sleep(2)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "08_extracted_skills.png"))

        print("[9] Navigating to Student Profile...")
        page.goto("http://localhost:5173/student/profile", wait_until="networkidle")
        time.sleep(2)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "09_student_profile.png"))

        # Logout Student
        page.goto("http://localhost:5173/login", wait_until="networkidle")
        # Clear storage
        context.clear_cookies()
        page.evaluate("() => localStorage.clear()")

        print("[10] Company Registration / Login (ZetHub)...")
        page.goto("http://localhost:5173/register", wait_until="networkidle")
        # Select Employer role if available
        role_btn = page.locator("button:has-text('Employer'), button:has-text('Company')").first
        if role_btn.is_visible():
            role_btn.click()
            time.sleep(0.5)
        page.fill("input#full_name", "ZetHub IT Solutions")
        page.fill("input#username", "zethub")
        page.fill("input#email", "hr@zethub.in")
        page.fill("input#password", "aswin@2006WEB")
        page.fill("input#confirm_password", "aswin@2006WEB")
        page.screenshot(path=os.path.join(OUTPUT_DIR, "10_company_registration.png"))

        print("[11] Company Login...")
        page.goto("http://localhost:5173/login", wait_until="networkidle")
        page.fill("input#username", "hr@zethub.in")
        page.fill("input#password", "aswin@2006WEB")
        page.screenshot(path=os.path.join(OUTPUT_DIR, "11_company_login.png"))
        page.click("button[type='submit']")
        page.wait_for_url("**/company/dashboard", timeout=8000)
        time.sleep(2)
        print("[12] Company Dashboard...")
        page.screenshot(path=os.path.join(OUTPUT_DIR, "12_company_dashboard.png"))

        print("[13] Create Job Page...")
        page.goto("http://localhost:5173/company/jobs/create", wait_until="networkidle")
        time.sleep(1)
        # Fill Job Form
        title_input = page.locator("input[placeholder*='Title'], input#title").first
        if title_input.is_visible():
            title_input.fill("Full Stack Developer / AI-ML Developer Intern")
        
        desc_input = page.locator("textarea[placeholder*='description'], textarea#description").first
        if desc_input.is_visible():
            desc_input.fill("We are seeking an energetic Full Stack / AI-ML Developer Intern proficient in Vue.js, React, Python Flask, MySQL, and NLP-based matching systems. You will develop modern web applications, design REST APIs, and integrate intelligent algorithms.")
        
        # Skills input
        skills_input = page.locator("input[placeholder*='skills'], input#required_skills").first
        if skills_input.is_visible():
            skills_input.fill("Python, Flask, Vue.js, React.js, MySQL, JavaScript, REST API, NLP")
        
        page.screenshot(path=os.path.join(OUTPUT_DIR, "13_create_job_form.png"))
        
        # Submit job
        submit_job_btn = page.locator("button[type='submit']:has-text('Post'), button[type='submit']:has-text('Create'), button:has-text('Publish')").first
        if submit_job_btn.is_visible():
            submit_job_btn.click()
            time.sleep(2)

        print("[14] Company Jobs Management...")
        page.goto("http://localhost:5173/company/jobs", wait_until="networkidle")
        time.sleep(2)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "14_company_jobs_list.png"))

        # Logout Company
        context.clear_cookies()
        page.evaluate("() => localStorage.clear()")

        print("[15] Login as Student to Browse & AI Match ZetHub Job...")
        page.goto("http://localhost:5173/login", wait_until="networkidle")
        page.fill("input#username", "cseaswin@gmail.com")
        page.fill("input#password", "aswin@2006WEB")
        page.click("button[type='submit']")
        page.wait_for_url("**/student/dashboard", timeout=8000)
        time.sleep(1)

        print("[16] Jobs & AI Matches Page...")
        page.goto("http://localhost:5173/jobs", wait_until="networkidle")
        time.sleep(2)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "15_job_listings_and_matches.png"))

        # Click on the ZetHub job details
        zethub_job_link = page.locator("text=Full Stack Developer").first
        if zethub_job_link.is_visible():
            zethub_job_link.click()
            time.sleep(2)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "16_job_ai_match_detail.png"))

        # Apply for the job
        apply_btn = page.locator("button:has-text('Apply Now'), button:has-text('Submit Application')").first
        if apply_btn.is_visible() and not apply_btn.is_disabled():
            apply_btn.click()
            time.sleep(2)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "17_job_applied_success.png"))

        print("[18] Student Applications Page...")
        page.goto("http://localhost:5173/student/applications", wait_until="networkidle")
        time.sleep(2)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "18_student_applications.png"))

        # Logout Student
        context.clear_cookies()
        page.evaluate("() => localStorage.clear()")

        print("[19] Company Login to Shortlist Aswin Kumar...")
        page.goto("http://localhost:5173/login", wait_until="networkidle")
        page.fill("input#username", "hr@zethub.in")
        page.fill("input#password", "aswin@2006WEB")
        page.click("button[type='submit']")
        page.wait_for_url("**/company/dashboard", timeout=8000)
        time.sleep(1)

        print("[20] Company Applicants View...")
        page.goto("http://localhost:5173/company/applicants", wait_until="networkidle")
        time.sleep(2)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "19_company_applicants_view.png"))

        # Shortlist button
        shortlist_btn = page.locator("button:has-text('Shortlist'), select:has-text('Status')").first
        if shortlist_btn.is_visible():
            shortlist_btn.click()
            time.sleep(2)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "20_applicant_shortlisted.png"))

        # Student side verified shortlisted status
        context.clear_cookies()
        page.evaluate("() => localStorage.clear()")
        page.goto("http://localhost:5173/login", wait_until="networkidle")
        page.fill("input#username", "cseaswin@gmail.com")
        page.fill("input#password", "aswin@2006WEB")
        page.click("button[type='submit']")
        page.wait_for_url("**/student/dashboard", timeout=8000)
        time.sleep(1)
        page.goto("http://localhost:5173/student/applications", wait_until="networkidle")
        time.sleep(2)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "21_student_shortlisted_status.png"))

        # Also capture phpMyAdmin / MySQL Database
        print("[22] phpMyAdmin Database Structure...")
        try:
            page.goto("http://localhost/phpmyadmin/index.php?route=/database/structure&db=ai_resume_matcher", timeout=6000)
            time.sleep(2)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "22_phpmyadmin_db_structure.png"))
            
            # phpMyAdmin users table
            page.goto("http://localhost/phpmyadmin/index.php?route=/sql&db=ai_resume_matcher&table=users&pos=0", timeout=6000)
            time.sleep(2)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "23_phpmyadmin_users_table.png"))
            
            # phpMyAdmin applications / jobs table
            page.goto("http://localhost/phpmyadmin/index.php?route=/sql&db=ai_resume_matcher&table=jobs&pos=0", timeout=6000)
            time.sleep(2)
            page.screenshot(path=os.path.join(OUTPUT_DIR, "24_phpmyadmin_jobs_table.png"))
        except Exception as e:
            print(f"phpMyAdmin capture note: {e}")

        browser.close()
        print("Workflow and screenshot captures completed successfully!")

if __name__ == "__main__":
    run_workflow_and_capture()
