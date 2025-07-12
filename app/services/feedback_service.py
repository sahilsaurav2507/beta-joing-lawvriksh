from app.repository.feedback_repository import FeedbackRepository
from app.models.feedback_models import FeedbackData
from app.schemas.response_schemas import BaseResponse
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class FeedbackService:
    
    @staticmethod
    def save_feedback(feedback_data: FeedbackData) -> BaseResponse:
        """Save feedback data"""
        try:
            if FeedbackRepository.save_feedback(feedback_data):
                return BaseResponse(
                    success=True,
                    message="Feedback submitted successfully"
                )
            else:
                return BaseResponse(
                    success=False,
                    message="Failed to submit feedback"
                )
        except Exception as e:
            logger.error(f"Error in save_feedback: {e}")
            return BaseResponse(
                success=False,
                message="Internal server error"
            )
    
    @staticmethod
    def get_all_feedback() -> List[Dict[str, Any]]:
        """Get all feedback data"""
        try:
            return FeedbackRepository.get_all_feedback()
        except Exception as e:
            logger.error(f"Error in get_all_feedback: {e}")
            return []
    
    @staticmethod
    def get_feedback_analytics() -> Dict[str, Any]:
        """Get feedback analytics and statistics"""
        try:
            return FeedbackRepository.get_feedback_analytics()
        except Exception as e:
            logger.error(f"Error in get_feedback_analytics: {e}")
            return {}
    
    @staticmethod
    def get_feedback_summary() -> Dict[str, Any]:
        """Get a summary of feedback data"""
        try:
            feedback_list = FeedbackRepository.get_all_feedback()
            analytics = FeedbackRepository.get_feedback_analytics()
            
            # Calculate summary statistics
            total_feedback = len(feedback_list)
            
            # Rating summaries
            rating_summaries = {}
            if analytics.get('average_ratings'):
                avg_ratings = analytics['average_ratings']
                rating_summaries = {
                    'visual_design': round(avg_ratings.get('avg_visual_design', 0), 2),
                    'navigation': round(avg_ratings.get('avg_navigation', 0), 2),
                    'mobile_responsiveness': round(avg_ratings.get('avg_mobile', 0), 2),
                    'overall_satisfaction': round(avg_ratings.get('avg_satisfaction', 0), 2),
                    'task_completion': round(avg_ratings.get('avg_task_completion', 0), 2),
                    'service_quality': round(avg_ratings.get('avg_service_quality', 0), 2)
                }
            
            # Follow-up consent summary
            consent_summary = {}
            if analytics.get('consent_stats'):
                for stat in analytics['consent_stats']:
                    consent_summary[stat['follow_up_consent']] = stat['count']
            
            # Recent feedback (last 10)
            recent_feedback = feedback_list[:10] if feedback_list else []
            
            return {
                'total_feedback': total_feedback,
                'average_ratings': rating_summaries,
                'consent_summary': consent_summary,
                'recent_feedback': recent_feedback
            }
        except Exception as e:
            logger.error(f"Error in get_feedback_summary: {e}")
            return {} 