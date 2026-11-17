from datetime import date, datetime, time
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class UserSummary(ORMModel):
    user_id: UUID
    employee_id: str
    display_name: str
    email: str
    job_title: str | None = None
    department: str | None = None
    location: str | None = None
    bio: str | None = None
    profile_image_url: str | None = None
    cover_image_url: str | None = None
    skills: list[dict] = []

class PostCreate(BaseModel):
    user_id: UUID
    content: str = Field(min_length=1, max_length=5000)
    post_type: str = "TEXT"
    media_url: str | None = None

class CommentCreate(BaseModel):
    user_id: UUID
    comment_text: str = Field(min_length=1, max_length=2000)

class RecognitionCreate(BaseModel):
    sender_id: UUID
    receiver_id: UUID
    recognition_type: str
    message: str = Field(min_length=1, max_length=2000)

class SaveCreate(BaseModel):
    user_id: UUID
    content_type: str
    content_id: UUID

class JoinRequest(BaseModel):
    user_id: UUID
