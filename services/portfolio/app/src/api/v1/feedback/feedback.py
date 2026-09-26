from fastapi import APIRouter, BackgroundTasks, Depends, status, HTTPException, Request
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
    request: Request,
    background_tasks: BackgroundTasks,
    service: FeedbackService = Depends(get_feedback_service)
):
    remote_ip = request.client.host if request.client else None
    is_human = await service.verify_feedback_request(
        captcha_token=body.captcha_token,
        honeypot=body.website,
        form_started_at=body.form_started_at,
        remote_ip=remote_ip,
    )
    if not is_human:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Spam protection validation failed",
        )

    background_tasks.add_task(
        service.send_feedback, body.name, body.email, body.message
    )
    return {"message": "Обратная связь отправлена!"}
