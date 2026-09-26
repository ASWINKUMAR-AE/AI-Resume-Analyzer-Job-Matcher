import re
from ai.skills_taxonomy import SKILL_TAXONOMY, SKILL_ALIASES, get_canonical_skill, get_skill_category

# Single letter/short keywords that need strict boundary checks
SHORT_SKILLS = {"c", "r", "go", "js", "ts", "py", "ml", "dl", "cv", "ai", "sql"}

class SkillExtractor:
    @staticmethod
    def extract_skills(raw_text, sections=None):
        """
        Extracts skills from text with taxonomy matching, alias resolution,
        category assignment, and confidence scoring.
        """
        if not raw_text:
            return []

        skills_section_text = (sections.get("skills", "") if sections else "").lower()
        projects_section_text = (sections.get("projects", "") if sections else "").lower()
        experience_section_text = (sections.get("experience", "") if sections else "").lower()
        full_text_lower = raw_text.lower()
        
        extracted = {}  # {canonical_name: {"skill_name": str, "category": str, "confidence": float}}
        
        # 1. Match from taxonomy list
        for category, skill_list in SKILL_TAXONOMY.items():
            for skill in skill_list:
                s_lower = skill.lower()
                pattern = SkillExtractor._build_pattern(s_lower)
                
                if pattern.search(full_text_lower):
                    canonical = get_canonical_skill(skill)
                    conf = SkillExtractor._calculate_confidence(
                        pattern, s_lower, skills_section_text, projects_section_text, experience_section_text
                    )
                    
                    if canonical not in extracted or conf > extracted[canonical]["confidence"]:
                        extracted[canonical] = {
                            "skill_name": canonical,
                            "category": category,
                            "confidence": conf
                        }
        
        # 2. Match from aliases
        for alias, canonical_name in SKILL_ALIASES.items():
            pattern = SkillExtractor._build_pattern(alias)
            if pattern.search(full_text_lower):
                canonical = get_canonical_skill(canonical_name)
                cat = get_skill_category(canonical)
                conf = SkillExtractor._calculate_confidence(
                    pattern, alias, skills_section_text, projects_section_text, experience_section_text
                )
                if canonical not in extracted or conf > extracted[canonical]["confidence"]:
                    extracted[canonical] = {
                        "skill_name": canonical,
                        "category": cat,
                        "confidence": conf
                    }

        # Return sorted list of extracted skills
        result = list(extracted.values())
        result.sort(key=lambda x: (x["category"], x["skill_name"]))
        return result

    @staticmethod
    def extract_skill_names(text):
        """
        Quick helper to extract canonical skill strings as a set or list.
        """
        extracted = SkillExtractor.extract_skills(text)
        return [s["skill_name"] for s in extracted]

    @staticmethod
    def _build_pattern(term):
        """
        Constructs regex pattern safe for special symbols like C++, C#, .NET, Node.js
        """
        escaped = re.escape(term)
        # Handle trailing symbols like ++, #, .js
        if term in SHORT_SKILLS:
            return re.compile(rf'(?<![a-zA-Z0-9]){escaped}(?![a-zA-Z0-9])', re.IGNORECASE)
        elif term.endswith('++') or term.endswith('#'):
            return re.compile(rf'(?<![a-zA-Z0-9]){escaped}', re.IGNORECASE)
        else:
            return re.compile(rf'\b{escaped}\b', re.IGNORECASE)

    @staticmethod
    def _calculate_confidence(pattern, term, skills_sec, proj_sec, exp_sec):
        """
        Assigns confidence score depending on where the skill occurs.
        """
        if pattern.search(skills_sec):
            return 1.0
        elif pattern.search(proj_sec):
            return 0.95
        elif pattern.search(exp_sec):
            return 0.90
        return 0.85
