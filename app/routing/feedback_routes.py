from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.feedback_models import FeedbackData
from app.services.feedback_service import FeedbackService
from app.services.auth_service import AuthService
from app.schemas.response_schemas import BaseResponse
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/feedback", tags=["Feedback"])
security = HTTPBearer()

def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify admin JWT token"""
    try:
        payload = AuthService.verify_token(credentials.credentials)
        if not payload or payload.get("role") != "admin":
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return payload
    except Exception as e:
        logger.error(f"Token verification error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/submit", response_model=BaseResponse)
async def submit_feedback(feedback_data: FeedbackData):
    """
    Submit feedback data
    
    - **user_email**: User's email (optional)
    - **visual_design_rating**: Rating for visual design (1-5, optional)
    - **visual_design_comments**: Comments for visual design (optional)
    - **ease_of_navigation_rating**: Rating for navigation (1-5, optional)
    - **ease_of_navigation_comments**: Comments for navigation (optional)
    - **mobile_responsiveness_rating**: Rating for mobile responsiveness (1-5, optional)
    - **mobile_responsiveness_comments**: Comments for mobile responsiveness (optional)
    - **overall_satisfaction_rating**: Overall satisfaction rating (1-5, optional)
    - **overall_satisfaction_comments**: Comments for overall satisfaction (optional)
    - **task_completion_rating**: Task completion rating (1-5, optional)
    - **task_completion_comments**: Comments for task completion (optional)
    - **service_quality_rating**: Service quality rating (1-5, optional)
    - **service_quality_comments**: Comments for service quality (optional)
    - **liked_features**: Features user liked (optional)
    - **improvement_suggestions**: Suggestions for improvement (optional)
    - **desired_features**: Desired features (optional)
    - **legal_challenges**: Legal challenges faced (optional)
    - **additional_feedback**: Additional feedback (optional)
    - **follow_up_consent**: Consent for follow-up (yes/no, optional)
    - **follow_up_email**: Email for follow-up (required if consent is yes)
    """
    try:
        result = FeedbackService.save_feedback(feedback_data)
        return result
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        return BaseResponse(
            success=False,
            message="Failed to submit feedback"
        )

@router.get("/all", response_model=BaseResponse)
async def get_all_feedback(payload: dict = Depends(verify_admin_token)):
    """
    Get all feedback data (Admin only)
    """
    try:
        feedback = FeedbackService.get_all_feedback()
        return BaseResponse(
            success=True,
            message="Feedback retrieved successfully",
            data=feedback
        )
    except Exception as e:
        logger.error(f"Error fetching feedback: {e}")
        return BaseResponse(
            success=False,
            message="Failed to fetch feedback"
        )

@router.get("/userfeedbackdata", response_model=BaseResponse)
async def get_user_feedback_data(payload: dict = Depends(verify_admin_token)):
    """
    Get all feedback data (Admin only, alternate endpoint)
    """
    try:
        feedback = FeedbackService.get_all_feedback()
        return BaseResponse(
            success=True,
            message="Feedback retrieved successfully",
            data=feedback
        )
    except Exception as e:
        logger.error(f"Error fetching feedback: {e}")
        return BaseResponse(
            success=False,
            message="Failed to fetch feedback"
        )

@router.get("/analytics", response_model=BaseResponse)
async def get_feedback_analytics(payload: dict = Depends(verify_admin_token)):
    """
    Get feedback analytics and statistics (Admin only)
    """
    try:
        analytics = FeedbackService.get_feedback_analytics()
        return BaseResponse(
            success=True,
            message="Analytics retrieved successfully",
            data=analytics
        )
    except Exception as e:
        logger.error(f"Error fetching feedback analytics: {e}")
        return BaseResponse(
            success=False,
            message="Failed to fetch analytics"
        )

@router.get("/summary", response_model=BaseResponse)
async def get_feedback_summary(payload: dict = Depends(verify_admin_token)):
    """
    Get feedback summary (Admin only)
    """
    try:
        summary = FeedbackService.get_feedback_summary()
        return BaseResponse(
            success=True,
            message="Summary retrieved successfully",
            data=summary
        )
    except Exception as e:
        logger.error(f"Error fetching feedback summary: {e}")
        return BaseResponse(
            success=False,
            message="Failed to fetch summary"
        ) 