import re
import os
from pypdf import PdfReader
from docx import Document

SECTION_HEADERS = {
    "summary": [
        "summary", "professional summary", "career summary", "profile", "about me",
        "objective", "career objective", "personal statement"
    ],
    "skills": [
        "skills", "technical skills", "core competencies", "skills & competencies",
        "technologies", "tech stack", "tools & technologies", "key skills", "proficiencies"
    ],
    "experience": [
        "experience", "work experience", "professional experience", "employment history",
        "work history", "internships", "relevant experience"
    ],
    "education": [
        "education", "academic background", "academic history", "qualifications",
        "degrees", "educational background"
    ],
    "projects": [
        "projects", "academic projects", "key projects", "personal projects",
        "software projects", "portfolio projects"
    ],
    "certifications": [
        "certifications", "certificates", "licenses", "courses", "credentials",
        "online certifications"
    ],
    "achievements": [
        "achievements", "awards", "honors", "accomplishments", "extracurricular"
    ],
    "languages": [
        "languages", "spoken languages", "language proficiencies"
    ]
}

EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
PHONE_REGEX = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
LINKEDIN_REGEX = r'(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/[a-zA-Z0-9-_]+'
GITHUB_REGEX = r'(?:https?:\/\/)?(?:www\.)?github\.com\/[a-zA-Z0-9-_]+'

class ResumeParser:
    @staticmethod
    def extract_text(file_path, file_type=None):
        """
        Extracts raw text from PDF, DOCX, or TXT file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at: {file_path}")
        
        ext = (file_type or os.path.splitext(file_path)[1].replace(".", "")).lower()
        
        if ext == "pdf":
            return ResumeParser._extract_pdf(file_path)
        elif ext in ["docx", "doc"]:
            return ResumeParser._extract_docx(file_path)
        elif ext in ["txt", "text"]:
            return ResumeParser._extract_txt(file_path)
        else:
            raise ValueError(f"Unsupported resume file type: {ext}. Allowed types: pdf, docx, txt")

    @staticmethod
    def _extract_pdf(path):
        text = []
        try:
            reader = PdfReader(path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        except Exception as e:
            raise RuntimeError(f"Error reading PDF file: {str(e)}")
        return "\n".join(text)

    @staticmethod
    def _extract_docx(path):
        try:
            doc = Document(path)
            full_text = []
            for para in doc.paragraphs:
                if para.text.strip():
                    full_text.append(para.text)
            for table in doc.tables:
                for row in table.rows:
                    row_data = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    if row_data:
                        full_text.append(" | ".join(row_data))
            return "\n".join(full_text)
        except Exception as e:
            raise RuntimeError(f"Error reading DOCX file: {str(e)}")

    @staticmethod
    def _extract_txt(path):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            raise RuntimeError(f"Error reading TXT file: {str(e)}")

    @staticmethod
    def clean_text(text):
        """
        Cleans extra whitespace, strange control characters, and normalizes line breaks.
        """
        if not text:
            return ""
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        # Replace non-breaking spaces
        text = text.replace('\xa0', ' ')
        # Reduce multiple spaces to single
        text = re.sub(r'[ \t]+', ' ', text)
        # Reduce multiple newlines to double newline
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()

    @staticmethod
    def detect_sections(raw_text):
        """
        Detects standard sections in resume using header recognition.
        """
        cleaned = ResumeParser.clean_text(raw_text)
        lines = cleaned.split('\n')
        
        sections = {
            "contact": "",
            "summary": "",
            "skills": "",
            "experience": "",
            "education": "",
            "projects": "",
            "certifications": "",
            "achievements": "",
            "languages": "",
            "other": ""
        }
        
        current_section = "contact"
        current_content = []
        
        for line in lines:
            trimmed = line.strip()
            if not trimmed:
                continue
            
            # Check if line is a section header (short line, match keywords)
            norm_header = re.sub(r'[^a-zA-Z\s]', '', trimmed.lower()).strip()
            found_section = None
            
            if len(trimmed) < 45 and not trimmed.endswith('.'):
                for sec_key, keywords in SECTION_HEADERS.items():
                    if norm_header in keywords or any(norm_header.startswith(kw) for kw in keywords):
                        found_section = sec_key
                        break
            
            if found_section:
                # Save previous section
                if current_content:
                    sections[current_section] = (sections[current_section] + "\n" + "\n".join(current_content)).strip()
                    current_content = []
                current_section = found_section
            else:
                current_content.append(trimmed)
                
        if current_content:
            sections[current_section] = (sections[current_section] + "\n" + "\n".join(current_content)).strip()
            
        return sections

    @staticmethod
    def extract_contact_info(text):
        """
        Extracts email, phone, links, and profile identifiers.
        """
        emails = re.findall(EMAIL_REGEX, text)
        phones = re.findall(PHONE_REGEX, text)
        linkedin = re.findall(LINKEDIN_REGEX, text)
        github = re.findall(GITHUB_REGEX, text)
        
        # Clean extracted phones
        valid_phones = [p.strip() for p in phones if len(re.sub(r'\D', '', p)) >= 10]
        
        return {
            "email": emails[0] if emails else None,
            "phone": valid_phones[0] if valid_phones else None,
            "linkedin_url": linkedin[0] if linkedin else None,
            "github_url": github[0] if github else None
        }

    @staticmethod
    def extract_education_details(education_text, raw_text=""):
        """
        Infers degrees, institutions, and graduation years.
        """
        combined = (education_text + " " + raw_text).lower()
        
        degree_patterns = [
            (r'bachelor|b\.?s\.?|b\.?tech|b\.?e\.?|undergraduate', 'Bachelor of Science / Engineering'),
            (r'master|m\.?s\.?|m\.?tech|m\.?b\.?a\.?|graduate', 'Master of Science / Postgraduate'),
            (r'ph\.?d\.?|doctorate', 'Doctorate (Ph.D.)'),
            (r'associate|diploma', 'Associate Degree / Diploma')
        ]
        
        detected_degree = "Bachelor's / Undergrad"
        for pattern, label in degree_patterns:
            if re.search(pattern, combined):
                detected_degree = label
                break
                
        # Graduation Year Detection (4 digit years between 2000 and 2035)
        years = re.findall(r'\b(20[0-3][0-9])\b', education_text)
        grad_year = int(years[-1]) if years else None
        
        return {
            "degree": detected_degree,
            "graduation_year": grad_year
        }

    @staticmethod
    def extract_experience_years(experience_text, raw_text=""):
        """
        Estimates years of experience from dates and keywords.
        """
        text = (experience_text + " " + raw_text).lower()
        
        # Look for explicit statements like "3+ years", "2 years of experience"
        explicit = re.findall(r'(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+experience', text)
        if explicit:
            return float(explicit[0])
            
        # Count date ranges e.g. "2021 - 2024", "2022 to Present"
        date_ranges = re.findall(r'\b(20[0-2][0-9])\s*(?:-|–|to)\s*(20[0-2][0-9]|present|current)\b', text)
        total_months = 0
        current_year = 2026
        
        for start_yr, end_yr in date_ranges:
            try:
                s_yr = int(start_yr)
                e_yr = current_year if end_yr in ["present", "current"] else int(end_yr)
                diff = max(0, e_yr - s_yr)
                total_months += diff * 12
            except Exception:
                pass
                
        if total_months > 0:
            return round(total_months / 12.0, 1)
            
        if "intern" in text or "entry level" in text or "fresh graduate" in text:
            return 0.5
            
        return 1.0
