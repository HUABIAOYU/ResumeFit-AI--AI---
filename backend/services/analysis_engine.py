"""
混合评分引擎：规则评分 + AI 语义分析
需求文档 4.5.3 定义的评分公式:
    最终匹配分 = 技能匹配分*40% + 项目相关性分*25% + 经历匹配分*20% + 表达质量分*10% + AI综合判断分*5%
"""

import re

from config import settings
from schemas.analysis import AIAnalysisResult, MissingSkill, Strength, Weakness, SuggestionItem, InterviewQuestion


def _extract_skills_from_text(text: str) -> set[str]:
    """简单规则提取技能关键词"""
    skill_patterns = [
        "vue3?", "vue\\.?js", "react", "angular", "typescript", "type script",
        "javascript", "js", "html5?", "css3?", "tailwind", "scss", "sass", "less",
        "node\\.?js", "node", "express", "koa", "next\\.?js", "nuxt",
        "webpack", "vite", "rollup", "esbuild", "babel",
        "git", "github", "gitlab",
        "pinia", "vuex", "redux", "zustand",
        "axios", "fetch",
        "jest", "vitest", "cypress", "playwright",
        "docker", "nginx", "ci/cd", "ci",
        "性能优化", "seo", "无障碍", "a11y",
        "vite", "uniapp", "taro",
        "webpack", "vite",
    ]
    found = set()
    text_lower = text.lower()
    for pattern in skill_patterns:
        if re.search(pattern, text_lower):
            found.add(pattern.replace(r"\\.", ".").replace(r"\\-", "-"))
    return found


def _skill_match_score(resume_skills: set[str], jd_skills: set[str]) -> float:
    """技能匹配分 0-100"""
    if not jd_skills:
        return 50
    matched = resume_skills & jd_skills
    return min(100, len(matched) / len(jd_skills) * 100)


def _project_relevance_score(resume_text: str, jd_text: str) -> float:
    """项目相关性分 0-100，基于关键词共现"""
    keywords = ["组件", "页面", "项目", "开发", "优化", "接口", "联调", "工程化", "打包", "部署"]
    resume_hits = sum(1 for kw in keywords if kw in resume_text)
    jd_hits = sum(1 for kw in keywords if kw in jd_text)
    if jd_hits == 0:
        return 50
    return min(100, resume_hits / max(jd_hits, 1) * 100)


def _experience_match_score(resume_text: str, jd_text: str) -> float:
    """经历匹配分 0-100"""
    signals = ["实习", "工作经验", "项目经验", "在校", "毕业", "年经验"]
    resume_hits = sum(1 for s in signals if s in resume_text)
    return min(100, resume_hits / max(len(signals), 1) * 100)


def _expression_quality_score(resume_text: str) -> float:
    """表达质量分 0-100"""
    score = 50
    if len(resume_text) > 300:
        score += 10
    if "负责" in resume_text or "参与" in resume_text:
        score += 10
    if re.search(r"\d+%|\d+倍|提升|减少|优化至", resume_text):
        score += 15
    if len(resume_text) > 600:
        score += 10
    return min(100, score)


def compute_rule_score(resume_text: str, jd_text: str) -> dict:
    """纯规则评分，返回各维度分数和加权总分"""
    resume_skills = _extract_skills_from_text(resume_text)
    jd_skills = _extract_skills_from_text(jd_text)

    skill_score = _skill_match_score(resume_skills, jd_skills)
    project_score = _project_relevance_score(resume_text, jd_text)
    experience_score = _experience_match_score(resume_text, jd_text)
    expression_score = _expression_quality_score(resume_text)

    # 没有 AI 综合判断分时，规则分数占 95%，按比例缩放
    rule_total = (
        skill_score * 0.40
        + project_score * 0.25
        + experience_score * 0.20
        + expression_score * 0.10
    ) / 0.95

    return {
        "rule_total": round(rule_total),
        "skill_score": round(skill_score),
        "project_score": round(project_score),
        "experience_score": round(experience_score),
        "expression_score": round(expression_score),
        "resume_skills": list(resume_skills),
        "jd_skills": list(jd_skills),
        "matched_skills": list(resume_skills & jd_skills),
    }


def merge_rule_and_ai(rule_result: dict, ai_result: AIAnalysisResult) -> int:
    """合并规则评分和 AI 评分"""
    if ai_result.overall_score > 0:
        return round(rule_result["rule_total"] * 0.95 + ai_result.overall_score * 0.05)
    return rule_result["rule_total"]
