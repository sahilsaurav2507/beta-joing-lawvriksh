-- =====================================================
-- LAWVIKSH JOINING LIST DATABASE SCHEMA (UPDATED)
-- MySQL Workbench compatible
-- =====================================================

-- Create database
CREATE DATABASE IF NOT EXISTS lawviksh_db;
USE lawviksh_db;

-- =====================================================
-- 1. USERS TABLE (for "Join as USER" and "Join as CREATOR" forms)
-- =====================================================

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(20) NOT NULL,
    gender ENUM('Male', 'Female', 'Other', 'Prefer not to say') NULL,
    profession ENUM('Student', 'Lawyer', 'Other') NULL,
    interest_reason TEXT NULL,
    user_type ENUM('user', 'creator') NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
);
GRANT ALL PRIVILEGES ON lawviksh_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;

-- =====================================================
-- 2. NOT INTERESTED TABLE (for "Not Interested" form)
-- =====================================================

CREATE TABLE not_interested_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    gender ENUM('Male', 'Female', 'Other', 'Prefer not to say') NULL,
    profession ENUM('Student', 'Lawyer', 'Other') NULL,
    not_interested_reason ENUM('Too complex', 'Not relevant', 'Other') NULL,
    improvement_suggestions TEXT NULL,
    interest_reason TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_reason (not_interested_reason),
    INDEX idx_created_at (created_at)
);

-- =====================================================
-- 3. FEEDBACK FORMS TABLE (for all feedback data)
-- =====================================================

CREATE TABLE feedback_forms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(255) NULL, -- Optional, for follow-up consent
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_email (user_email),
    INDEX idx_created_at (created_at)
);

-- =====================================================
-- 4. USER INTERFACE RATINGS TABLE
-- =====================================================

CREATE TABLE ui_ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    feedback_form_id INT NOT NULL,
    visual_design_rating INT CHECK (visual_design_rating BETWEEN 1 AND 5),
    visual_design_comments TEXT NULL,
    ease_of_navigation_rating INT CHECK (ease_of_navigation_rating BETWEEN 1 AND 5),
    ease_of_navigation_comments TEXT NULL,
    mobile_responsiveness_rating INT CHECK (mobile_responsiveness_rating BETWEEN 1 AND 5),
    mobile_responsiveness_comments TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (feedback_form_id) REFERENCES feedback_forms(id) ON DELETE CASCADE,
    INDEX idx_feedback_form (feedback_form_id),
    INDEX idx_ratings (visual_design_rating, ease_of_navigation_rating, mobile_responsiveness_rating)
);

-- =====================================================
-- 5. USER EXPERIENCE RATINGS TABLE
-- =====================================================

CREATE TABLE ux_ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    feedback_form_id INT NOT NULL,
    overall_satisfaction_rating INT CHECK (overall_satisfaction_rating BETWEEN 1 AND 5),
    overall_satisfaction_comments TEXT NULL,
    task_completion_rating INT CHECK (task_completion_rating BETWEEN 1 AND 5),
    task_completion_comments TEXT NULL,
    service_quality_rating INT CHECK (service_quality_rating BETWEEN 1 AND 5),
    service_quality_comments TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (feedback_form_id) REFERENCES feedback_forms(id) ON DELETE CASCADE,
    INDEX idx_feedback_form (feedback_form_id),
    INDEX idx_ratings (overall_satisfaction_rating, task_completion_rating, service_quality_rating)
);

-- =====================================================
-- 6. SUGGESTIONS AND LEGAL NEEDS TABLE
-- =====================================================

CREATE TABLE suggestions_and_needs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    feedback_form_id INT NOT NULL,
    liked_features TEXT NULL,
    improvement_suggestions TEXT NULL,
    desired_features TEXT NULL,
    legal_challenges TEXT NULL,
    additional_feedback TEXT NULL,
    follow_up_consent ENUM('yes', 'no') DEFAULT 'no',
    follow_up_email VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (feedback_form_id) REFERENCES feedback_forms(id) ON DELETE CASCADE,
    INDEX idx_feedback_form (feedback_form_id),
    INDEX idx_follow_up_consent (follow_up_consent)
);

-- =====================================================
-- 7. FORM SUBMISSIONS LOG TABLE (for tracking all submissions)
-- =====================================================

CREATE TABLE form_submissions_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    form_type ENUM('join_as_user', 'not_interested', 'feedback') NOT NULL,
    user_ip VARCHAR(45) NULL, -- IPv6 compatible
    user_agent TEXT NULL,
    submission_data JSON NULL, -- Store complete JSON for backup/audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_form_type (form_type),
    INDEX idx_created_at (created_at),
    INDEX idx_user_ip (user_ip)
);

-- =====================================================
-- 8. ANALYTICS VIEWS (for easy reporting)
-- =====================================================

-- View for user/creator registration analytics
CREATE OR REPLACE VIEW user_registration_analytics AS
SELECT 
    DATE(created_at) as registration_date,
    COUNT(*) as total_registrations,
    COUNT(CASE WHEN user_type = 'user' THEN 1 END) as user_count,
    COUNT(CASE WHEN user_type = 'creator' THEN 1 END) as creator_count,
    COUNT(CASE WHEN gender = 'Male' THEN 1 END) as male_count,
    COUNT(CASE WHEN gender = 'Female' THEN 1 END) as female_count,
    COUNT(CASE WHEN gender = 'Other' THEN 1 END) as other_count,
    COUNT(CASE WHEN gender = 'Prefer not to say' THEN 1 END) as prefer_not_to_say_count,
    COUNT(CASE WHEN profession = 'Student' THEN 1 END) as student_count,
    COUNT(CASE WHEN profession = 'Lawyer' THEN 1 END) as lawyer_count,
    COUNT(CASE WHEN profession = 'Other' THEN 1 END) as other_profession_count
FROM users 
GROUP BY DATE(created_at)
ORDER BY registration_date DESC;

-- View for feedback analytics
CREATE OR REPLACE VIEW feedback_analytics AS
SELECT 
    f.id as feedback_id,
    f.user_email,
    f.created_at,
    -- UI Ratings
    ui.visual_design_rating,
    ui.ease_of_navigation_rating,
    ui.mobile_responsiveness_rating,
    -- UX Ratings
    ux.overall_satisfaction_rating,
    ux.task_completion_rating,
    ux.service_quality_rating,
    -- Average ratings
    ROUND((ui.visual_design_rating + ui.ease_of_navigation_rating + ui.mobile_responsiveness_rating) / 3, 2) as avg_ui_rating,
    ROUND((ux.overall_satisfaction_rating + ux.task_completion_rating + ux.service_quality_rating) / 3, 2) as avg_ux_rating,
    -- Follow-up consent
    sn.follow_up_consent
FROM feedback_forms f
LEFT JOIN ui_ratings ui ON f.id = ui.feedback_form_id
LEFT JOIN ux_ratings ux ON f.id = ux.feedback_form_id
LEFT JOIN suggestions_and_needs sn ON f.id = sn.feedback_form_id
ORDER BY f.created_at DESC;

-- =====================================================
-- 9. SAMPLE DATA INSERTION (for testing)
-- =====================================================

-- Sample user registrations
INSERT INTO users (name, email, phone_number, gender, profession, interest_reason, user_type) VALUES
('John Doe', 'john.doe@example.com', '+1234567890', 'Male', 'Student', 'Interested in learning about legal processes', 'user'),
('Jane Smith', 'jane.smith@example.com', '+1234567891', 'Female', 'Lawyer', 'Looking for legal resources', 'creator'),
('Alex Johnson', 'alex.johnson@example.com', '+1234567892', 'Other', 'Other', 'General interest in law', 'user');

-- Sample not interested users
INSERT INTO not_interested_users (name, email, phone_number, gender, profession, not_interested_reason, improvement_suggestions, interest_reason) VALUES
('Bob Wilson', 'bob.wilson@example.com', '+1234567893', 'Male', 'Other', 'Too complex', 'Please simplify the interface', 'Not interested in legal resources'),
('Sarah Brown', 'sarah.brown@example.com', '+1234567894', 'Female', 'Lawyer', 'Not relevant', 'Not applicable to my needs', 'No interest');

-- Sample feedback form
INSERT INTO feedback_forms (user_email) VALUES
('feedback.user@example.com');

-- Sample UI ratings
INSERT INTO ui_ratings (feedback_form_id, visual_design_rating, ease_of_navigation_rating, mobile_responsiveness_rating) VALUES
(1, 4, 5, 4);

-- Sample UX ratings
INSERT INTO ux_ratings (feedback_form_id, overall_satisfaction_rating, task_completion_rating, service_quality_rating) VALUES
(1, 4, 4, 5);

-- Sample suggestions and needs
INSERT INTO suggestions_and_needs (feedback_form_id, liked_features, improvement_suggestions, desired_features, legal_challenges, follow_up_consent, follow_up_email) VALUES
(1, 'Clean interface and easy navigation', 'Add more legal resources', 'Document templates', 'Finding relevant legal information', 'yes', 'feedback.user@example.com');

-- =====================================================
-- 10. USEFUL QUERIES FOR ANALYSIS
-- =====================================================

-- Query to get total registrations by month
-- SELECT 
--     DATE_FORMAT(created_at, '%Y-%m') as month,
--     COUNT(*) as registrations
-- FROM users 
-- GROUP BY DATE_FORMAT(created_at, '%Y-%m')
-- ORDER BY month DESC;

-- Query to get average feedback ratings
-- SELECT 
--     AVG(visual_design_rating) as avg_visual_design,
--     AVG(ease_of_navigation_rating) as avg_navigation,
--     AVG(mobile_responsiveness_rating) as avg_mobile,
--     AVG(overall_satisfaction_rating) as avg_satisfaction,
--     AVG(task_completion_rating) as avg_task_completion,
--     AVG(service_quality_rating) as avg_service_quality
-- FROM ui_ratings ui
-- JOIN ux_ratings ux ON ui.feedback_form_id = ux.feedback_form_id;

-- Query to get most common improvement suggestions
-- SELECT 
--     improvement_suggestions,
--     COUNT(*) as frequency
-- FROM suggestions_and_needs 
-- WHERE improvement_suggestions IS NOT NULL 
-- GROUP BY improvement_suggestions 
-- ORDER BY frequency DESC 
-- LIMIT 10;

-- =====================================================
-- END OF SCHEMA
-- =====================================================
