from datetime import datetime

from pydantic import BaseModel


class ResumeUploadResponse(BaseModel):
    resume_id: str
    filename: str
    text_preview: str
    text_length: int
    created_at: datetime


class ResumeSegmentResponse(BaseModel):
    id: str
    section: str
    text: str
    page: int
    order_index: int

    model_config = {"from_attributes": True}


class ResumeDetailResponse(BaseModel):
    id: str
    filename: str
    raw_text: str
    created_at: datetime
    segments: list[ResumeSegmentResponse] = []

    model_config = {"from_attributes": True}


class ResumeListResponse(BaseModel):
    id: str
    filename: str
    created_at: datetime

    model_config = {"from_attributes": True}
