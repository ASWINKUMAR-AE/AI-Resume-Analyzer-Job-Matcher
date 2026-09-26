import re
import math
from collections import Counter
from ai.skill_extractor import SkillExtractor
from ai.skills_taxonomy import get_canonical_skill

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except Exception:
    SKLEARN_AVAILABLE = False

class JobMatcher:
    @staticmethod
    def calculate_text_similarity(doc1, doc2):
        """
        Computes TF-IDF and Cosine Similarity between resume text and job description.
        Uses scikit-learn when available, with pure Python fallback.
        """
        if not doc1 or not doc2:
            return 0.0
            
        if SKLEARN_AVAILABLE:
            try:
                vectorizer = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 2))
                tfidf_matrix = vectorizer.fit_transform([doc1, doc2])
                sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                return float(max(0.0, min(1.0, sim)))
            except Exception:
                pass
                
        # Pure Python fallback TF-IDF & Cosine Similarity
        return JobMatcher._pure_python_cosine_similarity(doc1, doc2)

    @staticmethod
    def _pure_python_cosine_similarity(text1, text2):
        def tokenize(text):
            words = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
            stop_words = {
                'the', 'and', 'is', 'in', 'at', 'of', 'on', 'for', 'with', 'a', 'an',
                'to', 'as', 'by', 'that', 'this', 'are', 'from', 'or', 'be', 'will', 'you', 'your'
            }
            return [w for w in words if w not in stop_words]

        tokens1 = tokenize(text1)
        tokens2 = tokenize(text2)
        if not tokens1 or not tokens2:
            return 0.0

        all_words = list(set(tokens1 + tokens2))
        c1 = Counter(tokens1)
        c2 = Counter(tokens2)

        v1 = [c1.get(w, 0) for w in all_words]
        v2 = [c2.get(w, 0) for w in all_words]

        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))

        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(dot / (norm1 * norm2))

    @staticmethod
    def evaluate_match(resume_text, resume_skills, job_dict, candidate_profile=None):
        """
        Calculates end-to-end explainable match score between a candidate resume and a job listing.
        """
        # 1. Skill Extraction for Job
        job_title = job_dict.get("title", "")
        job_desc = job_dict.get("description", "")
        job_req = job_dict.get("requirements", "")
        job_skills_raw = job_dict.get("skills", "")
        job_pref_raw = job_dict.get("preferred_skills", "")
        
        # Combine explicit skills field + extracted skills from description
        explicit_job_skills = [
            get_canonical_skill(s.strip()) for s in job_skills_raw.split(",") if s.strip()
        ]
        extracted_from_desc = SkillExtractor.extract_skill_names(f"{job_title} {job_desc} {job_req}")
        
        # Unique list of required/target job skills
        target_skills_set = set(explicit_job_skills + extracted_from_desc)
        if not target_skills_set:
            target_skills_set = {"Communication", "Problem Solving"}

        # Candidate skills set
        if isinstance(resume_skills, list):
            if resume_skills and isinstance(resume_skills[0], dict):
                cand_skills_set = set(s.get("skill_name") for s in resume_skills if s.get("skill_name"))
            else:
                cand_skills_set = set(get_canonical_skill(str(s)) for s in resume_skills)
        else:
            cand_skills_set = set(SkillExtractor.extract_skill_names(resume_text))

        # Skill Overlap
        matched_skills = sorted(list(target_skills_set.intersection(cand_skills_set)))
        missing_skills = sorted(list(target_skills_set.difference(cand_skills_set)))
        
        skill_match_ratio = len(matched_skills) / max(1, len(target_skills_set))
        skill_score = min(100.0, round(skill_match_ratio * 100.0, 1))

        # 2. Text Similarity (TF-IDF + Cosine)
        full_job_text = f"{job_title} {job_desc} {job_req} {job_skills_raw} {job_pref_raw}"
        text_sim = JobMatcher.calculate_text_similarity(resume_text, full_job_text)
        text_sim_score = min(100.0, round(text_sim * 100.0, 1))

        # 3. Experience Match
        exp_score = 80.0  # default fair baseline
        job_exp_str = (job_dict.get("experience_required") or "").lower()
        
        # Parse required years from job
        req_exp_match = re.search(r'(\d+)', job_exp_str)
        req_years = float(req_exp_match.group(1)) if req_exp_match else 1.0
        
        # Get candidate experience years
        cand_years = 1.0
        if candidate_profile and candidate_profile.get("experience"):
            exp_cand_str = str(candidate_profile.get("experience")).lower()
            c_match = re.search(r'(\d+)', exp_cand_str)
            if c_match:
                cand_years = float(c_match.group(1))
        
        if cand_years >= req_years:
            exp_score = 100.0
        elif cand_years >= (req_years * 0.5):
            exp_score = 75.0
        else:
            exp_score = 55.0

        # 4. Education Match
        edu_score = 90.0
        job_req_lower = (job_req + " " + job_desc).lower()
        if "master" in job_req_lower or "phd" in job_req_lower:
            if candidate_profile and ("master" in str(candidate_profile.get("degree", "")).lower() or "phd" in str(candidate_profile.get("degree", "")).lower()):
                edu_score = 100.0
            else:
                edu_score = 75.0
        else:
            edu_score = 95.0

        # 5. Composite Match Score Formula
        # Overall = 45% Skill Match + 30% Text Similarity + 15% Experience Match + 10% Education Match
        overall = (
            (0.45 * skill_score) +
            (0.30 * text_sim_score) +
            (0.15 * exp_score) +
            (0.10 * edu_score)
        )
        final_match_score = round(max(15.0, min(99.0, overall)), 1)

        # 6. Generate Explainability Insights
        strengths = []
        weaknesses = []
        recommendations = []
        
        if matched_skills:
            strengths.append(f"Matching technical skills: {', '.join(matched_skills[:6])}.")
        if skill_score >= 70:
            strengths.append(f"Strong skill alignment with {len(matched_skills)} of {len(target_skills_set)} target competencies matched.")
        if text_sim_score >= 40:
            strengths.append("High contextual overlap with the role description and responsibilities.")
            
        if missing_skills:
            weaknesses.append(f"Skills gap in: {', '.join(missing_skills[:5])}.")
            recommendations.append(f"Gain familiarity or complete projects utilizing: {', '.join(missing_skills[:4])}.")
            
        if exp_score < 80:
            weaknesses.append(f"Role prefers {job_dict.get('experience_required', 'more')} experience.")
            recommendations.append("Highlight production projects or relevant internships to offset formal years of experience.")

        why_matched = (
            f"Matches {len(matched_skills)} of {len(target_skills_set)} core requirements ({', '.join(matched_skills[:4])}) "
            f"with {int(text_sim_score)}% contextual similarity."
        )

        return {
            "match_score": final_match_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "score_breakdown": {
                "skill_match": skill_score,
                "text_similarity": text_sim_score,
                "experience_match": exp_score,
                "education_match": edu_score,
                "formula": "45% Skill + 30% Text TF-IDF + 15% Experience + 10% Education"
            },
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "why_matched_summary": why_matched
        }
