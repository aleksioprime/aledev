from src.services.feedback import FeedbackService
from src.core.config import settings


def get_feedback_service() -> FeedbackService:
    return FeedbackService(settings.email)