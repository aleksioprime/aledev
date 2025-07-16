from fastapi import APIRouter, BackgroundTasks, Depends, status, HTTPException
from src.schemas.feedback import FeedbackCreateSchema
from src.dependencies.feedback import get_feedback_service
from src.services.feedback import FeedbackService

router = APIRouter()


@router.post(
    "/",
    summary="Отправить обратную связь",
    status_code=status.HTTP_202_ACCEPTED,
)
async def send_feedback(
    body: FeedbackCreateSchema,
    background_tasks: BackgroundTasks,
    service: FeedbackService = Depends(get_feedback_service)
):
    try:
        background_tasks.add_task(
            service.send_feedback, body.name, body.email, body.message
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка отправки: {e}")
    return {"message": "Обратная связь отправлена!"}
