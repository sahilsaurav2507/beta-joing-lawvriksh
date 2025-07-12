from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from enum import Enum

class FollowUpConsent(str, Enum):
    YES = "yes"
    NO = "no"

class FeedbackData(BaseModel):
    user_email: Optional[EmailStr] = None
    
    # UI Ratings
    visual_design_rating: Optional[int] = None
    visual_design_comments: Optional[str] = None
    ease_of_navigation_rating: Optional[int] = None
    ease_of_navigation_comments: Optional[str] = None
    mobile_responsiveness_rating: Optional[int] = None
    mobile_responsiveness_comments: Optional[str] = None
    
    # UX Ratings
    overall_satisfaction_rating: Optional[int] = None
    overall_satisfaction_comments: Optional[str] = None
    task_completion_rating: Optional[int] = None
    task_completion_comments: Optional[str] = None
    service_quality_rating: Optional[int] = None
    service_quality_comments: Optional[str] = None
    
    # Suggestions and Needs
    liked_features: Optional[str] = None
    improvement_suggestions: Optional[str] = None
    desired_features: Optional[str] = None
    legal_challenges: Optional[str] = None
    additional_feedback: Optional[str] = None
    
    # Follow-up
    follow_up_consent: Optional[FollowUpConsent] = FollowUpConsent.NO
    follow_up_email: Optional[EmailStr] = None
    
    @validator('visual_design_rating', 'ease_of_navigation_rating', 'mobile_responsiveness_rating',
               'overall_satisfaction_rating', 'task_completion_rating', 'service_quality_rating')
    def validate_rating(cls, v):
        if v is not None and (v < 1 or v > 5):
            raise ValueError('Rating must be between 1 and 5')
        return v
    
    @validator('follow_up_email')
    def validate_follow_up_email(cls, v, values):
        if values.get('follow_up_consent') == FollowUpConsent.YES and not v:
            raise ValueError('Follow-up email is required when consent is given')
        return v 