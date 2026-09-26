# AI Methodology & Matching Algorithm

## 1. Overview

The **AI Resume Analyzer & Job Matcher** utilizes an explainable, multi-factor AI/NLP engine designed to eliminate recruitment black boxes. It computes candidate compatibility based on mathematical similarity, skill taxonomy alignment, career level, and prerequisite qualifications.

---

## 2. Core Modules

### 1. Multi-Format Resume Parser (`backend/ai/parser.py`)
- **PDF Extraction**: Extracted page by page via `pypdf`.
- **DOCX Extraction**: Extracted paragraph by paragraph and table by table via `python-docx`.
- **TXT Extraction**: UTF-8 and Latin-1 multi-encoding fallback.
- **Section Detection**: Header matching against 8 primary sections:
  1. Summary / Objective
  2. Technical Skills
  3. Work Experience / Internships
  4. Academic Education
  5. Projects
  6. Certifications
  7. Achievements & Awards
  8. Languages

### 2. Skill Taxonomy & Alias Resolution (`backend/ai/skill_extractor.py`)
- Standardizes diverse keyword representations into canonical skills.
  - *Example*: `vue.js`, `vuejs`, `vue 3` $\rightarrow$ `Vue.js`
  - *Example*: `postgres`, `postgresql` $\rightarrow$ `PostgreSQL`
  - *Example*: `sklearn`, `scikit-learn` $\rightarrow$ `scikit-learn`
- **Context Confidence Scoring**:
  - Found in dedicated **Skills** section: `1.0 (100%)`
  - Found in **Projects** section: `0.95 (95%)`
  - Found in **Work Experience** section: `0.90 (90%)`
  - Found in general text: `0.85 (85%)`

### 3. ATS Resume Health Scorer (`backend/ai/resume_scorer.py`)
The resume health score is computed on a 0–100 scale according to 5 weighted criteria:
1. **Section Completeness (30 pts)**: Presence of Summary, Skills, Experience, Education, Projects, and Certifications.
2. **Skill Diversity & Quantity (25 pts)**: Total skills count and coverage across multiple technological domains (Languages, Frontend, Backend, Databases, Cloud, AI/ML).
3. **Measurable Impact & Action Verbs (20 pts)**: Frequency of strong action verbs (*Engineered, Architected, Deployed, Optimized*) and quantifiable outcome metrics (*e.g., %, $, latency reductions*).
4. **Contact Details & Professional URLs (15 pts)**: Phone, email, LinkedIn, and GitHub links.
5. **Formatting & Length Balance (10 pts)**: Ideal 250–950 word density for ATS scanning.

---

## 4. Multi-Factor Match Scoring Formula (`backend/ai/matcher.py`)

$$\text{Final Match Score} = (0.45 \times \text{Skill Match}) + (0.30 \times \text{TF-IDF Similarity}) + (0.15 \times \text{Experience Match}) + (0.10 \times \text{Education Match})$$

### Components:
- **Skill Match (45% Weight)**:
  $$\text{Skill Match} = \frac{|\text{Target Job Skills} \cap \text{Candidate Skills}|}{\max(1, |\text{Target Job Skills}|)} \times 100$$
- **TF-IDF & Cosine Similarity (30% Weight)**:
  $$\text{Cosine Similarity} = \frac{\mathbf{v}_{\text{resume}} \cdot \mathbf{v}_{\text{job}}}{\|\mathbf{v}_{\text{resume}}\| \|\mathbf{v}_{\text{job}}\|}$$
- **Experience Match (15% Weight)**: Evaluates whether candidate experience meets or exceeds role seniority.
- **Education Match (10% Weight)**: Verifies degree level (Bachelor, Master, PhD) and field alignment.

---

## 5. Offline Resilience & Privacy Guarantee

The entire NLP and ML pipeline executes locally on the Python Flask backend with zero required external API dependencies. Optional OpenAI or Google Gemini API keys can be configured in `.env` to enhance narrative conversational coaching without altering the deterministic, explainable mathematical match scores.
