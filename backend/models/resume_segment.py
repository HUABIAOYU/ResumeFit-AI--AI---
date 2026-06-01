import uuid

from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class ResumeSegment(Base):
    __tablename__ = "resume_segments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    resume_id: Mapped[str] = mapped_column(String(36), ForeignKey("resumes.id"), nullable=False, index=True)
    section: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    page: Mapped[int] = mapped_column(Integer, default=1)
    order_index: Mapped[int] = mapped_column(Integer, default=0)

    resume = relationship("Resume", back_populates="segments")
    suggestions = relationship("Suggestion", back_populates="target_segment")
