from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from app.services.user_service import UserService
from app.services.feedback_service import FeedbackService
from app.services.auth_service import AuthService
from app.schemas.response_schemas import BaseResponse, DataDownloadResponse
from typing import List, Dict, Any
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/data", tags=["Data Management"])
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

@router.post("/downloaddata", response_model=BaseResponse)
async def download_data(payload: dict = Depends(verify_admin_token)):
    """
    Download all data in JSON format (Admin only)
    """
    try:
        # Get all data
        users = UserService.get_all_users()
        creators = UserService.get_all_creators()
        not_interested = UserService.get_all_not_interested()
        feedback = FeedbackService.get_all_feedback()
        
        # Get analytics
        user_analytics = UserService.get_user_analytics()
        feedback_analytics = FeedbackService.get_feedback_analytics()
        
        # Prepare download data
        download_data = {
            "users": users,
            "creators": creators,
            "not_interested": not_interested,
            "feedback": feedback,
            "analytics": {
                "user_analytics": user_analytics,
                "feedback_analytics": feedback_analytics
            },
            "summary": {
                "total_users": len(users),
                "total_creators": len(creators),
                "total_not_interested": len(not_interested),
                "total_feedback": len(feedback)
            }
        }
        
        return BaseResponse(
            success=True,
            message="Data downloaded successfully",
            data=download_data
        )
    except Exception as e:
        logger.error(f"Error downloading data: {e}")
        return BaseResponse(
            success=False,
            message="Failed to download data"
        )

@router.get("/export/json", response_model=BaseResponse)
async def export_data_json(payload: dict = Depends(verify_admin_token)):
    """
    Export all data as JSON file (Admin only)
    """
    try:
        # Get all data
        users = UserService.get_all_users()
        creators = UserService.get_all_creators()
        not_interested = UserService.get_all_not_interested()
        feedback = FeedbackService.get_all_feedback()
        
        # Get analytics
        user_analytics = UserService.get_user_analytics()
        feedback_analytics = FeedbackService.get_feedback_analytics()
        
        # Prepare export data
        export_data = {
            "export_date": str(payload.get("exp", "")),
            "users": users,
            "creators": creators,
            "not_interested": not_interested,
            "feedback": feedback,
            "analytics": {
                "user_analytics": user_analytics,
                "feedback_analytics": feedback_analytics
            },
            "summary": {
                "total_users": len(users),
                "total_creators": len(creators),
                "total_not_interested": len(not_interested),
                "total_feedback": len(feedback)
            }
        }
        
        # Return as JSON response with file download headers
        return JSONResponse(
            content=export_data,
            headers={
                "Content-Disposition": "attachment; filename=lawviksh_data_export.json",
                "Content-Type": "application/json"
            }
        )
    except Exception as e:
        logger.error(f"Error exporting data: {e}")
        raise HTTPException(status_code=500, detail="Failed to export data")

@router.get("/stats", response_model=BaseResponse)
async def get_data_statistics(payload: dict = Depends(verify_admin_token)):
    """
    Get data statistics (Admin only)
    """
    try:
        # Get all data counts
        users = UserService.get_all_users()
        creators = UserService.get_all_creators()
        not_interested = UserService.get_all_not_interested()
        feedback = FeedbackService.get_all_feedback()
        
        # Get analytics
        user_analytics = UserService.get_user_analytics()
        feedback_analytics = FeedbackService.get_feedback_analytics()
        
        stats = {
            "total_users": len(users),
            "total_creators": len(creators),
            "total_not_interested": len(not_interested),
            "total_feedback": len(feedback),
            "user_analytics": user_analytics,
            "feedback_analytics": feedback_analytics
        }
        
        return BaseResponse(
            success=True,
            message="Statistics retrieved successfully",
            data=stats
        )
    except Exception as e:
        logger.error(f"Error fetching statistics: {e}")
        return BaseResponse(
            success=False,
            message="Failed to fetch statistics"
        ) 