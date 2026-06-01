from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


# ── AI 输出子结构（需求文档 4.5.4 定义）──

class MissingSkill(BaseModel):
    skill: str
    importance: str = "nice_to_have"
    reason: str = ""
    learning_suggestion: str = ""


class Strength(BaseModel):
    title: str
    evidence: str
    related_segment_id: str = ""


class WeaknessSeverity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Weakness(BaseModel):
    title: str
    reason: str
    severity: WeaknessSeverity = WeaknessSeverity.medium
    related_segment_id: str = ""


class SuggestionType(str, Enum):
    quantify_impact = "quantify_impact"
    keyword_optimization = "keyword_optimization"
    clarity = "clarity"
    project_relevance = "project_relevance"
    ats = "ats"


class SuggestionItem(BaseModel):
    target_segment_id: str = ""
    type: SuggestionType = SuggestionType.clarity
    before: str = ""
    after: str = ""
    reason: str = ""


class Difficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class InterviewQuestion(BaseModel):
    question: str
    difficulty: Difficulty = Difficulty.medium
    related_skill: str = ""
    reason: str = ""
    answer_hint: str = ""


# ── AI 分析结果（需求文档 4.5.4 完整结构）──

class AIAnalysisResult(BaseModel):
    """AI 返回的结构，Pydantic 校验用"""

    overall_score: int = Field(ge=0, le=100)
    summary: str = ""
    matched_skills: list[str] = []
    missing_skills: list[MissingSkill] = []
    strengths: list[Strength] = []
    weaknesses: list[Weakness] = []
    suggestions: list[SuggestionItem] = []
    interview_questions: list[InterviewQuestion] = []


# ── API 请求/响应 ──

class CreateAnalysisRequest(BaseModel):
    resume_id: str
    job_description: str


class AnalysisResponse(BaseModel):
    analysis_id: str
    resume_id: str
    job_id: str
    overall_score: int
    summary: str
    matched_skills: list[str] = []
    missing_skills: list[MissingSkill] = []
    strengths: list[Strength] = []
    weaknesses: list[Weakness] = []
    suggestions: list[SuggestionItem] = []
    interview_questions: list[InterviewQuestion] = []
    created_at: datetime


class AnalysisListItem(BaseModel):
    analysis_id: str
    resume_filename: str = ""
    job_title: str = ""
    overall_score: int
    created_at: datetime
