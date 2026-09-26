import re

ACTION_VERBS = [
    "developed", "built", "engineered", "designed", "implemented", "architected",
    "optimized", "scaled", "created", "led", "managed", "deployed", "integrated",
    "improved", "accelerated", "reduced", "automated", "spearheaded", "orchestrated"
]

METRIC_PATTERNS = [
    r'\b\d+%\b',
    r'\$\s*\d+(?:,\d+)*(?:\.\d+)?(?:k|m|b)?\b',
    r'\b\d+\s*(?:ms|seconds|minutes|hours|days|x|users|clients|requests|transactions)\b',
    r'\bincreased by\b',
    r'\breduced by\b',
    r'\bimproved by\b'
]

class ResumeScorer:
    @staticmethod
    def score_resume(raw_text, sections, skills, contact_info=None):
        """
        Calculates a holistic 0-100 resume health score with detailed explainable feedback.
        """
        score = 0
        breakdown = {}
        strengths = []
        weaknesses = []
        recommendations = []
        warnings = []
        suggestions = []

        # 1. Section Completeness (Max 30 points)
        sec_points = 0
        required_secs = [
            ("summary", "Summary / Objective", 4),
            ("skills", "Technical Skills", 8),
            ("experience", "Work Experience / Internships", 8),
            ("education", "Education Background", 6),
            ("projects", "Projects", 4)
        ]
        
        missing_sections = []
        for key, name, pts in required_secs:
            content = sections.get(key, "").strip()
            if content and len(content) > 20:
                sec_points += pts
            else:
                missing_sections.append(name)
                
        # Bonus for certifications/achievements
        if sections.get("certifications", "").strip():
            sec_points = min(30, sec_points + 2)
        if sections.get("achievements", "").strip():
            sec_points = min(30, sec_points + 2)
            
        score += sec_points
        breakdown["section_completeness"] = {"score": sec_points, "max": 30}
        
        if not missing_sections:
            strengths.append("Comprehensive section structure covering Summary, Skills, Experience, Projects, and Education.")
        else:
            weaknesses.append(f"Missing or brief sections: {', '.join(missing_sections)}.")
            recommendations.append(f"Add dedicated sections for: {', '.join(missing_sections)} to ensure complete ATS parsing.")

        # 2. Skill Diversity and Quantity (Max 25 points)
        skill_count = len(skills)
        skill_categories = set(s.get("category", "") for s in skills)
        
        skill_score = 0
        if skill_count >= 12:
            skill_score += 15
        elif skill_count >= 7:
            skill_score += 10
        elif skill_count >= 3:
            skill_score += 6
        else:
            skill_score += 2

        if len(skill_categories) >= 4:
            skill_score += 10
        elif len(skill_categories) >= 2:
            skill_score += 6
        else:
            skill_score += 3
            
        score += skill_score
        breakdown["skills_depth"] = {"score": skill_score, "max": 25, "count": skill_count, "categories": len(skill_categories)}
        
        if skill_count >= 10 and len(skill_categories) >= 3:
            strengths.append(f"Strong technical repertoire with {skill_count} detected skills spanning {len(skill_categories)} technology domains.")
        else:
            weaknesses.append(f"Skill coverage is limited ({skill_count} skills detected).")
            recommendations.append("Expand your skills section with relevant frameworks, tools, database technologies, and cloud services.")

        # 3. Measurable Impact & Action Verbs (Max 20 points)
        text_lower = raw_text.lower()
        matched_verbs = [v for v in ACTION_VERBS if re.search(rf'\b{v}\b', text_lower)]
        
        metric_matches = 0
        for pat in METRIC_PATTERNS:
            if re.search(pat, text_lower):
                metric_matches += 1
                
        impact_score = 0
        if len(matched_verbs) >= 6:
            impact_score += 10
        elif len(matched_verbs) >= 3:
            impact_score += 6
        else:
            impact_score += 2
            
        if metric_matches >= 3:
            impact_score += 10
        elif metric_matches >= 1:
            impact_score += 6
        else:
            impact_score += 1
            
        score += impact_score
        breakdown["measurable_impact"] = {"score": impact_score, "max": 20, "action_verbs": len(matched_verbs), "metrics_detected": metric_matches}
        
        if metric_matches >= 2 and len(matched_verbs) >= 4:
            strengths.append("Effective use of strong action verbs and quantifiable outcome metrics in descriptions.")
        else:
            weaknesses.append("Descriptions lack sufficient quantifiable metrics (percentages, KPIs, performance boosts).")
            recommendations.append("Quantify your project and work achievements (e.g. 'Improved API response time by 35%' instead of 'Worked on API optimization').")
            suggestions.append({
                "category": "Quantifiable Impact",
                "before": "Created a web application with Python and Vue.",
                "suggestion": "Developed a full-stack Vue 3 + Flask web app supporting 500+ active users and reducing data retrieval latency by 40%."
            })

        # 4. Contact & Identity Information (Max 15 points)
        contact_score = 0
        if contact_info:
            if contact_info.get("email"):
                contact_score += 5
            if contact_info.get("phone"):
                contact_score += 4
            if contact_info.get("linkedin_url"):
                contact_score += 3
            if contact_info.get("github_url"):
                contact_score += 3
                
        score += contact_score
        breakdown["contact_information"] = {"score": contact_score, "max": 15}
        
        if contact_info and contact_info.get("linkedin_url") and contact_info.get("github_url"):
            strengths.append("Professional profile links (LinkedIn and GitHub/Portfolio) detected.")
        else:
            recommendations.append("Include your LinkedIn profile and GitHub repository link in the header for recruiter visibility.")

        # 5. Length & Formatting Clarity (Max 10 points)
        word_count = len(raw_text.split())
        format_score = 0
        if 250 <= word_count <= 950:
            format_score = 10
            strengths.append(f"Optimal resume length ({word_count} words), ideal for standard 1 to 2-page ATS scanning.")
        elif word_count < 250:
            format_score = 4
            warnings.append(f"Resume text seems very brief ({word_count} words). Consider adding more detailed bullet points under projects and experience.")
        else:
            format_score = 6
            warnings.append(f"Resume is on the longer side ({word_count} words). Try to keep content concise and focused.")
            
        score += format_score
        breakdown["formatting_clarity"] = {"score": format_score, "max": 10, "word_count": word_count}

        # Cap total score between 0 and 100
        final_score = max(10, min(100, int(score)))

        return {
            "resume_score": final_score,
            "breakdown": breakdown,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "warnings": warnings,
            "suggestions": suggestions
        }
