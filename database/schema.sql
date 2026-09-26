-- Database Schema for AI Resume Analyzer & Job Matcher
-- Target MySQL Database: ai_resume_matcher

CREATE DATABASE IF NOT EXISTS `ai_resume_matcher` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `ai_resume_matcher`;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(150) NOT NULL,
    `email` VARCHAR(191) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `role` ENUM('student', 'company', 'admin') NOT NULL,
    `status` ENUM('active', 'inactive', 'pending') DEFAULT 'active',
    `must_change_password` TINYINT(1) DEFAULT 0,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_users_email` (`email`),
    INDEX `idx_users_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Student Profiles Table
CREATE TABLE IF NOT EXISTS `student_profiles` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL UNIQUE,
    `phone` VARCHAR(30) NULL,
    `location` VARCHAR(150) NULL,
    `education` VARCHAR(150) NULL,
    `college` VARCHAR(200) NULL,
    `degree` VARCHAR(150) NULL,
    `graduation_year` INT NULL,
    `experience` VARCHAR(100) NULL,
    `bio` TEXT NULL,
    `linkedin_url` VARCHAR(255) NULL,
    `github_url` VARCHAR(255) NULL,
    `portfolio_url` VARCHAR(255) NULL,
    `profile_image` VARCHAR(255) NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_student_profile_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Company Profiles Table
CREATE TABLE IF NOT EXISTS `company_profiles` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL UNIQUE,
    `company_name` VARCHAR(200) NOT NULL,
    `company_email` VARCHAR(191) NULL,
    `phone` VARCHAR(30) NULL,
    `website` VARCHAR(255) NULL,
    `industry` VARCHAR(100) NULL,
    `location` VARCHAR(150) NULL,
    `description` TEXT NULL,
    `logo` VARCHAR(255) NULL,
    `verified` TINYINT(1) DEFAULT 0,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_company_profile_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Resumes Table
CREATE TABLE IF NOT EXISTS `resumes` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_id` INT NOT NULL,
    `file_name` VARCHAR(255) NOT NULL,
    `file_path` VARCHAR(500) NOT NULL,
    `file_type` VARCHAR(50) NOT NULL,
    `raw_text` LONGTEXT NULL,
    `parsed_sections` JSON NULL,
    `resume_score` INT DEFAULT 0,
    `strengths` JSON NULL,
    `weaknesses` JSON NULL,
    `recommendations` JSON NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_resumes_student` (`student_id`),
    CONSTRAINT `fk_resume_user` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Extracted Skills Table
CREATE TABLE IF NOT EXISTS `extracted_skills` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `resume_id` INT NOT NULL,
    `skill_name` VARCHAR(100) NOT NULL,
    `category` VARCHAR(100) DEFAULT 'General',
    `confidence` FLOAT DEFAULT 1.0,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_extracted_skills_resume` (`resume_id`),
    INDEX `idx_extracted_skills_name` (`skill_name`),
    CONSTRAINT `fk_skill_resume` FOREIGN KEY (`resume_id`) REFERENCES `resumes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Jobs Table
CREATE TABLE IF NOT EXISTS `jobs` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `company_id` INT NOT NULL,
    `title` VARCHAR(200) NOT NULL,
    `description` LONGTEXT NOT NULL,
    `requirements` TEXT NULL,
    `skills` TEXT NULL,
    `preferred_skills` TEXT NULL,
    `location` VARCHAR(150) NULL,
    `job_type` ENUM('Full Time', 'Part Time', 'Internship', 'Contract', 'Remote', 'Hybrid') DEFAULT 'Full Time',
    `experience_required` VARCHAR(100) NULL,
    `salary_min` DECIMAL(12, 2) NULL,
    `salary_max` DECIMAL(12, 2) NULL,
    `application_deadline` DATE NULL,
    `status` ENUM('active', 'closed', 'draft') DEFAULT 'active',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_jobs_company` (`company_id`),
    INDEX `idx_jobs_status` (`status`),
    CONSTRAINT `fk_job_company` FOREIGN KEY (`company_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Applications Table
CREATE TABLE IF NOT EXISTS `applications` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `job_id` INT NOT NULL,
    `student_id` INT NOT NULL,
    `resume_id` INT NOT NULL,
    `match_score` FLOAT DEFAULT 0,
    `status` ENUM('Applied', 'Under Review', 'Shortlisted', 'Interview', 'Selected', 'Rejected') DEFAULT 'Applied',
    `cover_note` TEXT NULL,
    `applied_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_apps_job` (`job_id`),
    INDEX `idx_apps_student` (`student_id`),
    INDEX `idx_apps_status` (`status`),
    CONSTRAINT `fk_app_job` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_app_student` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_app_resume` FOREIGN KEY (`resume_id`) REFERENCES `resumes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. Saved Jobs Table
CREATE TABLE IF NOT EXISTS `saved_jobs` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_id` INT NOT NULL,
    `job_id` INT NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY `unique_student_job` (`student_id`, `job_id`),
    CONSTRAINT `fk_saved_student` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_saved_job` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. AI Analysis Table
CREATE TABLE IF NOT EXISTS `ai_analysis` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_id` INT NOT NULL,
    `resume_id` INT NOT NULL,
    `job_id` INT NOT NULL,
    `match_score` FLOAT DEFAULT 0,
    `matched_skills` JSON NULL,
    `missing_skills` JSON NULL,
    `strengths` JSON NULL,
    `weaknesses` JSON NULL,
    `recommendations` JSON NULL,
    `score_breakdown` JSON NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_analysis_student` (`student_id`),
    INDEX `idx_analysis_job` (`job_id`),
    INDEX `idx_analysis_resume` (`resume_id`),
    CONSTRAINT `fk_analysis_student` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_analysis_resume` FOREIGN KEY (`resume_id`) REFERENCES `resumes` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_analysis_job` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
