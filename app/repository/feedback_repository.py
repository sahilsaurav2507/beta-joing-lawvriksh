# Import database (SQLite for development, MySQL for production)
try:
    from database import db
except ImportError:
    from database_sqlite import db
from app.models.feedback_models import FeedbackData
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class FeedbackRepository:
    
    @staticmethod
    def save_feedback(feedback_data: FeedbackData) -> bool:
        """Save feedback data to database"""
        try:
            # Start transaction (SQLite doesn't need explicit start)
            if hasattr(db.connection, 'start_transaction'):
                db.connection.start_transaction()
            
            # Insert into feedback_forms
            feedback_query = "INSERT INTO feedback_forms (user_email) VALUES (%s)"
            feedback_result = db.execute_query(feedback_query, (feedback_data.user_email,))
            
            if feedback_result <= 0:
                if hasattr(db.connection, 'rollback'):
                    db.connection.rollback()
                return False
            
            feedback_form_id = db.cursor.lastrowid
            
            # Insert UI ratings if provided
            if any([
                feedback_data.visual_design_rating,
                feedback_data.ease_of_navigation_rating,
                feedback_data.mobile_responsiveness_rating
            ]):
                ui_query = """
                    INSERT INTO ui_ratings (
                        feedback_form_id, visual_design_rating, visual_design_comments,
                        ease_of_navigation_rating, ease_of_navigation_comments,
                        mobile_responsiveness_rating, mobile_responsiveness_comments
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                ui_params = (
                    feedback_form_id,
                    feedback_data.visual_design_rating,
                    feedback_data.visual_design_comments,
                    feedback_data.ease_of_navigation_rating,
                    feedback_data.ease_of_navigation_comments,
                    feedback_data.mobile_responsiveness_rating,
                    feedback_data.mobile_responsiveness_comments
                )
                db.execute_query(ui_query, ui_params)
            
            # Insert UX ratings if provided
            if any([
                feedback_data.overall_satisfaction_rating,
                feedback_data.task_completion_rating,
                feedback_data.service_quality_rating
            ]):
                ux_query = """
                    INSERT INTO ux_ratings (
                        feedback_form_id, overall_satisfaction_rating, overall_satisfaction_comments,
                        task_completion_rating, task_completion_comments,
                        service_quality_rating, service_quality_comments
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                ux_params = (
                    feedback_form_id,
                    feedback_data.overall_satisfaction_rating,
                    feedback_data.overall_satisfaction_comments,
                    feedback_data.task_completion_rating,
                    feedback_data.task_completion_comments,
                    feedback_data.service_quality_rating,
                    feedback_data.service_quality_comments
                )
                db.execute_query(ux_query, ux_params)
            
            # Insert suggestions and needs if provided
            if any([
                feedback_data.liked_features,
                feedback_data.improvement_suggestions,
                feedback_data.desired_features,
                feedback_data.legal_challenges,
                feedback_data.additional_feedback,
                feedback_data.follow_up_consent,
                feedback_data.follow_up_email
            ]):
                suggestions_query = """
                    INSERT INTO suggestions_and_needs (
                        feedback_form_id, liked_features, improvement_suggestions,
                        desired_features, legal_challenges, additional_feedback,
                        follow_up_consent, follow_up_email
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                suggestions_params = (
                    feedback_form_id,
                    feedback_data.liked_features,
                    feedback_data.improvement_suggestions,
                    feedback_data.desired_features,
                    feedback_data.legal_challenges,
                    feedback_data.additional_feedback,
                    feedback_data.follow_up_consent,
                    feedback_data.follow_up_email
                )
                db.execute_query(suggestions_query, suggestions_params)
            
            # Commit transaction
            if hasattr(db.connection, 'commit'):
                db.connection.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error saving feedback: {e}")
            if hasattr(db.connection, 'rollback'):
                db.connection.rollback()
            return False
    
    @staticmethod
    def get_all_feedback() -> List[dict]:
        """Get all feedback data with related information"""
        try:
            query = """
                SELECT 
                    f.id, f.user_email, f.created_at,
                    ui.visual_design_rating, ui.visual_design_comments,
                    ui.ease_of_navigation_rating, ui.ease_of_navigation_comments,
                    ui.mobile_responsiveness_rating, ui.mobile_responsiveness_comments,
                    ux.overall_satisfaction_rating, ux.overall_satisfaction_comments,
                    ux.task_completion_rating, ux.task_completion_comments,
                    ux.service_quality_rating, ux.service_quality_comments,
                    sn.liked_features, sn.improvement_suggestions,
                    sn.desired_features, sn.legal_challenges, sn.additional_feedback,
                    sn.follow_up_consent, sn.follow_up_email
                FROM feedback_forms f
                LEFT JOIN ui_ratings ui ON f.id = ui.feedback_form_id
                LEFT JOIN ux_ratings ux ON f.id = ux.feedback_form_id
                LEFT JOIN suggestions_and_needs sn ON f.id = sn.feedback_form_id
                ORDER BY f.created_at DESC
            """
            return db.execute_query(query)
        except Exception as e:
            logger.error(f"Error fetching feedback: {e}")
            return []
    
    @staticmethod
    def get_feedback_analytics() -> dict:
        """Get feedback analytics and statistics"""
        try:
            # Get average ratings
            avg_ratings_query = """
                SELECT 
                    AVG(ui.visual_design_rating) as avg_visual_design,
                    AVG(ui.ease_of_navigation_rating) as avg_navigation,
                    AVG(ui.mobile_responsiveness_rating) as avg_mobile,
                    AVG(ux.overall_satisfaction_rating) as avg_satisfaction,
                    AVG(ux.task_completion_rating) as avg_task_completion,
                    AVG(ux.service_quality_rating) as avg_service_quality
                FROM feedback_forms f
                LEFT JOIN ui_ratings ui ON f.id = ui.feedback_form_id
                LEFT JOIN ux_ratings ux ON f.id = ux.feedback_form_id
            """
            avg_ratings = db.execute_query(avg_ratings_query)
            
            # Get total feedback count
            count_query = "SELECT COUNT(*) as total_feedback FROM feedback_forms"
            total_count = db.execute_query(count_query)
            
            # Get follow-up consent count
            consent_query = """
                SELECT 
                    follow_up_consent,
                    COUNT(*) as count
                FROM suggestions_and_needs 
                WHERE follow_up_consent IS NOT NULL
                GROUP BY follow_up_consent
            """
            consent_stats = db.execute_query(consent_query)
            
            return {
                'average_ratings': avg_ratings[0] if avg_ratings else {},
                'total_feedback': total_count[0]['total_feedback'] if total_count else 0,
                'consent_stats': consent_stats
            }
        except Exception as e:
            logger.error(f"Error fetching feedback analytics: {e}")
            return {} 