"""
Skill Taxonomy & Aliases for AI Resume Analyzer & Job Matcher.
Configurable, hierarchical dictionary with category classifications and aliases.
"""

SKILL_TAXONOMY = {
    # 1. Programming Languages
    "Languages": [
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "C", "Go", "Golang",
        "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R", "Dart", "MATLAB",
        "SQL", "HTML", "CSS", "Bash", "Shell", "PowerShell", "Perl"
    ],
    
    # 2. Web & Frontend Frameworks
    "Frontend": [
        "Vue.js", "Vue", "React", "React.js", "Angular", "Next.js", "Nuxt.js", "Svelte",
        "Tailwind CSS", "Bootstrap", "Sass", "SCSS", "jQuery", "Redux", "Pinia", "Vuex",
        "Webpack", "Vite", "Responsive Design", "WebSockets", "GraphQL", "REST API"
    ],
    
    # 3. Backend & APIs
    "Backend": [
        "Flask", "Django", "FastAPI", "Node.js", "Express.js", "NestJS", "Spring Boot",
        "ASP.NET", "Ruby on Rails", "Laravel", "Microservices", "RESTful API", "gRPC",
        "Celery", "JWT", "OAuth", "GraphQL API"
    ],
    
    # 4. Databases & Caching
    "Databases": [
        "MySQL", "PostgreSQL", "SQLite", "MongoDB", "Redis", "Elasticsearch",
        "Oracle", "Microsoft SQL Server", "Cassandra", "DynamoDB", "Firebase",
        "Supabase", "Prisma", "SQLAlchemy", "Hibernate"
    ],
    
    # 5. Cloud, DevOps & Infrastructure
    "DevOps & Cloud": [
        "AWS", "Amazon Web Services", "Microsoft Azure", "Google Cloud", "GCP",
        "Docker", "Kubernetes", "CI/CD", "GitHub Actions", "GitLab CI", "Jenkins",
        "Terraform", "Ansible", "Linux", "Nginx", "Apache", "Prometheus", "Grafana"
    ],
    
    # 6. AI, Machine Learning & Data Science
    "AI & Data Science": [
        "Machine Learning", "Deep Learning", "Natural Language Processing", "NLP",
        "Computer Vision", "TensorFlow", "PyTorch", "scikit-learn", "Keras",
        "NumPy", "Pandas", "SciPy", "Matplotlib", "Seaborn", "Data Analysis",
        "Data Visualization", "Big Data", "Spark", "Hadoop", "LLM", "Prompt Engineering",
        "Vector Embeddings", "Transformers", "Hugging Face", "OpenAI API", "LangChain"
    ],
    
    # 7. Tools, Methodologies & Version Control
    "Tools & Practices": [
        "Git", "GitHub", "GitLab", "Bitbucket", "Jira", "Agile", "Scrum",
        "Unit Testing", "Test Driven Development", "TDD", "Postman", "Swagger",
        "Linux CLI", "Figma", "Object-Oriented Programming", "OOP", "Design Patterns"
    ],
    
    # 8. Professional & Soft Skills
    "Soft Skills": [
        "Problem Solving", "Team Leadership", "Communication", "Collaboration",
        "Project Management", "Critical Thinking", "Adaptability", "Time Management",
        "Mentorship", "Technical Writing"
    ]
}

# Alias / Synonym Normalization Dictionary
SKILL_ALIASES = {
    "vue": "Vue.js",
    "vuejs": "Vue.js",
    "vue.js": "Vue.js",
    "vue 3": "Vue.js",
    "vue2": "Vue.js",
    "react": "React",
    "reactjs": "React",
    "react.js": "React",
    "react native": "React Native",
    "angular": "Angular",
    "angularjs": "Angular",
    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "express": "Express.js",
    "expressjs": "Express.js",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "ts": "TypeScript",
    "typescript": "TypeScript",
    "py": "Python",
    "python": "Python",
    "python3": "Python",
    "golang": "Go",
    "go": "Go",
    "c++": "C++",
    "cpp": "C++",
    "c#": "C#",
    "csharp": "C#",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "mongo": "MongoDB",
    "mongodb": "MongoDB",
    "k8s": "Kubernetes",
    "kubernetes": "Kubernetes",
    "aws": "AWS",
    "amazon web services": "AWS",
    "gcp": "Google Cloud",
    "google cloud platform": "Google Cloud",
    "azure": "Microsoft Azure",
    "ml": "Machine Learning",
    "machine learning": "Machine Learning",
    "dl": "Deep Learning",
    "deep learning": "Deep Learning",
    "nlp": "Natural Language Processing",
    "natural language processing": "Natural Language Processing",
    "cv": "Computer Vision",
    "computer vision": "Computer Vision",
    "sklearn": "scikit-learn",
    "scikit-learn": "scikit-learn",
    "tf": "TensorFlow",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "rest": "REST API",
    "rest api": "REST API",
    "restful": "REST API",
    "restful api": "REST API",
    "ci/cd": "CI/CD",
    "cicd": "CI/CD",
    "gh actions": "GitHub Actions",
    "github actions": "GitHub Actions",
    "tailwind": "Tailwind CSS",
    "tailwindcss": "Tailwind CSS",
    "tailwind css": "Tailwind CSS",
    "oop": "Object-Oriented Programming"
}

def get_canonical_skill(skill_str):
    """
    Returns normalized canonical skill name.
    """
    clean = skill_str.strip()
    lower = clean.lower()
    if lower in SKILL_ALIASES:
        return SKILL_ALIASES[lower]
    
    for category, skills in SKILL_TAXONOMY.items():
        for s in skills:
            if s.lower() == lower:
                return s
    return clean

def get_skill_category(canonical_skill):
    """
    Finds category for a canonical skill name.
    """
    for category, skills in SKILL_TAXONOMY.items():
        if canonical_skill in skills:
            return category
    return "Other Technical"
