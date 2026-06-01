import uuid

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Suggestion(Base):
    __tablename__ = "suggestions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    analysis_id: Mapped[str] = mapped_column(String(36), ForeignKey("analyses.id"), nullable=False, index=True)
    target_segment_id: Mapped[str] = mapped_column(String(36), ForeignKey("resume_segments.id"), nullable=True)
    type: Mapped[str] = mapped_column(String(50), default="clarity")
    before_text: Mapped[str] = mapped_column(Text, default="")
    after_text: Mapped[str] = mapped_column(Text, default="")
    reason: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(20), default="pending")

    analysis = relationship("Analysis", back_populates="suggestions")
    target_segment = relationship("ResumeSegment", back_populates="suggestions")
