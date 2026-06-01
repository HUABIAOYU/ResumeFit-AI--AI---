import os
import uuid

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from config import settings
from database import get_db
from api.deps import get_current_user
from models.user import User
from models.resume import Resume
from schemas.resume import ResumeUploadResponse, ResumeDetailResponse, ResumeListResponse
from schemas.common import MessageResponse
from services.pdf_parser import parse_pdf, is_likely_scanned
from services.sanitizer import sanitize
from services.segmenter import segment_resume_text
from models.resume_segment import ResumeSegment

router = APIRouter(prefix="/api/resumes", tags=["简历"])


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="仅支持 PDF 简历")

    file_bytes = await file.read()
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > settings.pdf_max_size_mb:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="文件过大")

    if len(file_bytes) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="文件内容为空")

    try:
        result = parse_pdf(file_bytes)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="简历解析失败")

    if is_likely_scanned(result.full_text, settings.resume_min_chars):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="简历文本过短，可能为扫描版 PDF，请上传文本版 PDF",
        )

    sanitized = sanitize(result.full_text)

    os.makedirs(settings.upload_dir, exist_ok=True)
    file_path = os.path.join(settings.upload_dir, f"{uuid.uuid4()}.pdf")
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    resume = Resume(
        user_id=current_user.id,
        filename=file.filename,
        file_url=file_path,
        raw_text=result.full_text,
        sanitized_text=sanitized,
    )
    db.add(resume)
    await db.flush()

    # 创建简历分段
    segments_data = segment_resume_text(result.full_text)
    for idx, seg in enumerate(segments_data):
        db.add(ResumeSegment(
            resume_id=resume.id,
            section=seg["section"],
            text=seg["text"],
            page=1,
            order_index=idx,
        ))
    await db.flush()
    await db.refresh(resume)

    preview = result.full_text[:200] + "..." if len(result.full_text) > 200 else result.full_text
    return ResumeUploadResponse(
        resume_id=resume.id,
        filename=resume.filename,
        text_preview=preview,
        text_length=len(result.full_text),
        created_at=resume.created_at,
    )


@router.get("", response_model=list[ResumeListResponse])
async def list_resumes(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Resume).where(Resume.user_id == current_user.id).order_by(Resume.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{resume_id}", response_model=ResumeDetailResponse)
async def get_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Resume).where(Resume.id == resume_id, Resume.user_id == current_user.id)
        .options(selectinload(Resume.segments))
    )
    resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="简历不存在")
    return resume


@router.delete("/{resume_id}", response_model=MessageResponse)
async def delete_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Resume).where(Resume.id == resume_id, Resume.user_id == current_user.id)
    )
    resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="简历不存在")
    await db.delete(resume)
    return MessageResponse(message="简历已删除")
