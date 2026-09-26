from pydantic import BaseModel, EmailStr, Field


class FeedbackCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    message: str = Field(..., min_length=10, max_length=2000)
    captcha_token: str = Field(..., min_length=10, max_length=4096)
    website: str = Field("", max_length=0)
    form_started_at: int = Field(..., gt=0)
