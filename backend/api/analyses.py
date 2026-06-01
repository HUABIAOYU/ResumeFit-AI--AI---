import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_db
from api.deps import get_current_user
from models.user import User
from models.resume import Resume
from models.job import Job
from models.analysis import Analysis
from models.suggestion import Suggestion
from schemas.analysis import (
    CreateAnalysisRequest,
    AnalysisResponse,
    AnalysisListItem,
    AIAnalysisResult,
)
from schemas.common import MessageResponse
from services.jd_extractor import extract_jd, run_ai_analysis
from services.analysis_engine import compute_rule_score, merge_rule_and_ai

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/analyses", tags=["分析"])


@router.post("", response_model=AnalysisResponse)
async def create_analysis(
    req: CreateAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not req.job_description or len(req.job_description.strip()) < 10:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="岗位 JD 内容过短")

    # 获取简历
    result = await db.execute(
        select(Resume).where(Resume.id == req.resume_id, Resume.user_id == current_user.id)
    )
    resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="简历不存在")

    # 保存 JD
    job = Job(
        user_id=current_user.id,
        description=req.job_description.strip(),
    )
    db.add(job)
    await db.flush()

    try:
        # JD 结构化提取
        jd_extracted = await extract_jd(req.job_description.strip())
        job.title = jd_extracted.get("title", "")
        job.extracted_json = jd_extracted
    except Exception as e:
        logger.warning(f"JD 提取失败，继续分析: {e}")

    # 规则评分
    rule_result = compute_rule_score(resume.sanitized_text, job.description)

    # AI 语义分析
    ai_result = None
    try:
        ai_result = await run_ai_analysis(
            resume_text=resume.sanitized_text,
            job_description=job.description,
            jd_extracted=jd_extracted if job.extracted_json else None,
        )
    except Exception as e:
        logger.error(f"AI 分析失败: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="AI 分析失败，请重试")

    # 合并评分
    final_score = merge_rule_and_ai(rule_result, ai_result)

    # 保存分析结果
    analysis = Analysis(
        user_id=current_user.id,
        resume_id=resume.id,
        job_id=job.id,
        overall_score=final_score,
        summary=ai_result.summary,
        result_json=ai_result.model_dump(),
    )
    db.add(analysis)
    await db.flush()

    # 保存建议
    for suggestion in ai_result.suggestions:
        s = Suggestion(
            analysis_id=analysis.id,
            target_segment_id=None,  # AI 返回的标签并非 DB 中的真实 segment UUID
            type=suggestion.type.value if hasattr(suggestion.type, 'value') else suggestion.type,
            before_text=suggestion.before,
            after_text=suggestion.after,
            reason=suggestion.reason,
        )
        db.add(s)

    return AnalysisResponse(
        analysis_id=analysis.id,
        resume_id=resume.id,
        job_id=job.id,
        overall_score=final_score,
        summary=ai_result.summary,
        matched_skills=ai_result.matched_skills,
        missing_skills=ai_result.missing_skills,
        strengths=ai_result.strengths,
        weaknesses=ai_result.weaknesses,
        suggestions=ai_result.suggestions,
        interview_questions=ai_result.interview_questions,
        created_at=analysis.created_at,
    )


@router.get("", response_model=list[AnalysisListItem])
async def list_analyses(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Analysis)
        .where(Analysis.user_id == current_user.id)
        .options(selectinload(Analysis.resume), selectinload(Analysis.job))
        .order_by(Analysis.created_at.desc())
    )
    analyses = result.scalars().all()
    return [
        AnalysisListItem(
            analysis_id=a.id,
            resume_filename=a.resume.filename if a.resume else "",
            job_title=a.job.title if a.job else "",
            overall_score=a.overall_score,
            created_at=a.created_at,
        )
        for a in analyses
    ]


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Analysis)
        .where(Analysis.id == analysis_id, Analysis.user_id == current_user.id)
        .options(selectinload(Analysis.suggestions))
    )
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="分析报告不存在")

    data = analysis.result_json or {}
    return AnalysisResponse(
        analysis_id=analysis.id,
        resume_id=analysis.resume_id,
        job_id=analysis.job_id,
        overall_score=analysis.overall_score,
        summary=analysis.summary,
        matched_skills=data.get("matched_skills", []),
        missing_skills=data.get("missing_skills", []),
        strengths=data.get("strengths", []),
        weaknesses=data.get("weaknesses", []),
        suggestions=data.get("suggestions", []),
        interview_questions=data.get("interview_questions", []),
        created_at=analysis.created_at,
    )


@router.delete("/{analysis_id}", response_model=MessageResponse)
async def delete_analysis(
    analysis_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Analysis).where(Analysis.id == analysis_id, Analysis.user_id == current_user.id)
    )
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="分析报告不存在")
    await db.delete(analysis)
    return MessageResponse(message="分析报告已删除")
