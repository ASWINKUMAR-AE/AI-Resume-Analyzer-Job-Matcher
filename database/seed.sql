-- AI Resume Analyzer & Job Matcher Demo Seed Data
USE `ai_resume_matcher`;

-- Default Admin (Password: Admin@123)
INSERT IGNORE INTO `users` (`id`, `name`, `email`, `password_hash`, `role`, `status`, `must_change_password`) VALUES
(1, 'System Administrator', 'admin@airesume.com', 'scrypt:32768:8:1$uH3WkW1qF5Yv6Z0G$615c4d6215eb375d86ca8e1b126305a2e58c89b88cf1459a0f074d0a8764feaa9a6bca26442655bf5d447fc1f24dbe309be6b75ebfa40a4306fe1d45da85fa32', 'admin', 'active', 0);

-- Demo Companies (Password: Company@123 for all demo companies)
INSERT IGNORE INTO `users` (`id`, `name`, `email`, `password_hash`, `role`, `status`, `must_change_password`) VALUES
(2, 'TechNova Solutions', 'hr@technova.com', 'scrypt:32768:8:1$kR7wF9vX8z1Q2L0M$d9284fae852ce79237699313db433fbc5ea62f3a61ba9aebcd19f7a77bda30fa8c893ba0ee56d0284e3d36bfaae6d8d6eb1006e8fb2cf5fc9ffecdfbc066e4d7', 'company', 'active', 0),
(3, 'ZetHub Technologies', 'careers@zethub.com', 'scrypt:32768:8:1$kR7wF9vX8z1Q2L0M$d9284fae852ce79237699313db433fbc5ea62f3a61ba9aebcd19f7a77bda30fa8c893ba0ee56d0284e3d36bfaae6d8d6eb1006e8fb2cf5fc9ffecdfbc066e4d7', 'company', 'active', 0),
(4, 'CloudCore Systems', 'jobs@cloudcore.com', 'scrypt:32768:8:1$kR7wF9vX8z1Q2L0M$d9284fae852ce79237699313db433fbc5ea62f3a61ba9aebcd19f7a77bda30fa8c893ba0ee56d0284e3d36bfaae6d8d6eb1006e8fb2cf5fc9ffecdfbc066e4d7', 'company', 'active', 0),
(5, 'DataSphere AI', 'talent@datasphere.ai', 'scrypt:32768:8:1$kR7wF9vX8z1Q2L0M$d9284fae852ce79237699313db433fbc5ea62f3a61ba9aebcd19f7a77bda30fa8c893ba0ee56d0284e3d36bfaae6d8d6eb1006e8fb2cf5fc9ffecdfbc066e4d7', 'company', 'active', 0);

-- Demo Student (Password: Student@123)
INSERT IGNORE INTO `users` (`id`, `name`, `email`, `password_hash`, `role`, `status`, `must_change_password`) VALUES
(6, 'Alex Rivera', 'alex.student@example.com', 'scrypt:32768:8:1$mN5vK2xP7y4Q9W1Z$4f884f18db269d0426fe41362e53eeeaae89d18db4314c1143a5ce39097e87da9ea03cf7b7fce29d10e52fcba4c1fb3a2f8f70fa0cbff9574cf97a47ef0e85ca', 'student', 'active', 0);

-- Company Profiles
INSERT IGNORE INTO `company_profiles` (`id`, `user_id`, `company_name`, `company_email`, `phone`, `website`, `industry`, `location`, `description`, `verified`) VALUES
(1, 2, 'TechNova Solutions', 'hr@technova.com', '+1-555-0192', 'https://technovasolutions.io', 'Software & Cloud Engineering', 'San Francisco, CA (Hybrid)', 'TechNova is a cutting-edge software engineering firm specializing in high-throughput enterprise SaaS, modern web applications, and cloud-native solutions.', 1),
(2, 3, 'ZetHub Technologies', 'careers@zethub.com', '+1-555-0144', 'https://zethub.tech', 'Artificial Intelligence & Fintech', 'New York, NY (Remote)', 'ZetHub builds next-generation financial intelligence platforms and automated workflow engines powered by machine learning and Python microservices.', 1),
(3, 4, 'CloudCore Systems', 'jobs@cloudcore.com', '+1-555-0188', 'https://cloudcore.dev', 'Cloud Infrastructure & DevOps', 'Austin, TX', 'CloudCore builds automated Kubernetes infrastructure, CI/CD orchestration, and scalable multi-region AWS cloud solutions for Fortune 500 enterprises.', 1),
(4, 5, 'DataSphere AI', 'talent@datasphere.ai', '+1-555-0177', 'https://datasphere.ai', 'Big Data & Machine Learning', 'Seattle, WA (Hybrid)', 'DataSphere is an AI research and applied analytics lab engineering predictive ML pipelines, deep learning models, and real-time data streaming engines.', 1);

-- Student Profile
INSERT IGNORE INTO `student_profiles` (`id`, `user_id`, `phone`, `location`, `education`, `college`, `degree`, `graduation_year`, `experience`, `bio`, `linkedin_url`, `github_url`, `portfolio_url`) VALUES
(1, 6, '+1-555-0123', 'San Francisco, CA', 'Bachelor of Science', 'Stanford University', 'Computer Science', 2025, '1-2 years', 'Passionate full-stack & AI software engineering student with experience building Python, Flask, Vue.js, and SQL web platforms. Enthusiastic about ML model deployment and clean code.', 'https://linkedin.com/in/alex-rivera-demo', 'https://github.com/alexrivera-demo', 'https://alexrivera.dev');

-- Demo Jobs
INSERT IGNORE INTO `jobs` (`id`, `company_id`, `title`, `description`, `requirements`, `skills`, `preferred_skills`, `location`, `job_type`, `experience_required`, `salary_min`, `salary_max`, `application_deadline`, `status`) VALUES
(1, 2, 'Full Stack Python & Vue Developer', 'We are looking for a versatile Full Stack Developer to build modern web applications. You will develop reactive user interfaces with Vue.js, create robust REST APIs with Python/Flask, and integrate MySQL databases.', 'Bachelor in CS or related experience. Strong proficiency in Vue.js, Python, Flask, REST APIs, and relational databases. Familiarity with Git and Docker.', 'Python, Flask, Vue.js, JavaScript, MySQL, REST API, Git, HTML, CSS', 'Docker, Tailwind CSS, Redis, TypeScript', 'San Francisco, CA (Hybrid)', 'Full Time', '1-3 years', 85000.00, 115000.00, DATE_ADD(CURRENT_DATE, INTERVAL 45 DAY), 'active'),

(2, 2, 'Frontend Engineer (Vue 3 / TypeScript)', 'Join our frontend engineering team to craft blazing-fast SaaS dashboards and intuitive AI web interfaces using Vue 3, Pinia, and modern CSS architecture.', 'Strong command of Vue.js, modern JavaScript/TypeScript, responsive UI design, component architecture, and state management.', 'Vue.js, JavaScript, TypeScript, HTML, CSS, REST API, Pinia, Git', 'Tailwind CSS, Vite, Jest, Figma', 'San Francisco, CA', 'Full Time', '2-4 years', 95000.00, 130000.00, DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), 'active'),

(3, 3, 'AI / Machine Learning Intern', 'Exciting opportunity for a motivated AI/ML intern to work on real-world natural language processing, TF-IDF vectorization, scikit-learn models, and recommendation algorithms.', 'Currently enrolled or recent graduate in CS/Data Science. Working knowledge of Python, NumPy, Pandas, scikit-learn, and basic NLP concepts.', 'Python, Machine Learning, NLP, scikit-learn, NumPy, SQL, Git', 'Deep Learning, PyTorch, TensorFlow, Flask', 'New York, NY (Remote)', 'Internship', '0-1 years', 45000.00, 65000.00, DATE_ADD(CURRENT_DATE, INTERVAL 60 DAY), 'active'),

(4, 3, 'Backend Python Engineer', 'Architect and scale backend microservices, real-time data pipelines, and secure RESTful endpoints using Python, Flask/FastAPI, and MySQL.', '2+ years developing backend services with Python, designing relational database schemas, handling authentication (JWT), and optimizing SQL queries.', 'Python, Flask, MySQL, REST API, JWT, SQL, Git, Linux', 'FastAPI, Docker, Redis, Celery', 'New York, NY', 'Full Time', '2-5 years', 105000.00, 140000.00, DATE_ADD(CURRENT_DATE, INTERVAL 40 DAY), 'active'),

(5, 4, 'Cloud Infrastructure & DevOps Engineer', 'Build and maintain automated cloud pipelines, Kubernetes clusters, Docker containerization, and secure CI/CD workflows on AWS.', 'Proficiency in AWS, Docker, Kubernetes, Linux, CI/CD, and infrastructure as code. Scripting in Python or Bash.', 'AWS, Docker, Kubernetes, Linux, CI/CD, Git, Python', 'Terraform, Ansible, Prometheus, Grafana', 'Austin, TX (Remote)', 'Full Time', '2-4 years', 110000.00, 145000.00, DATE_ADD(CURRENT_DATE, INTERVAL 35 DAY), 'active'),

(6, 5, 'Data Analyst & ML Specialist', 'Transform complex datasets into actionable business intelligence. Build predictive models, extract insights using SQL and Python, and create data visualization dashboards.', 'Strong analytical mindset, mastery of SQL, Python data manipulation (Pandas, NumPy), and machine learning pipelines.', 'SQL, Python, Data Analysis, Machine Learning, Pandas, NumPy, Data Visualization', 'Tableau, Power BI, Statistics, BigQuery', 'Seattle, WA (Hybrid)', 'Full Time', '1-3 years', 80000.00, 110000.00, DATE_ADD(CURRENT_DATE, INTERVAL 50 DAY), 'active');
