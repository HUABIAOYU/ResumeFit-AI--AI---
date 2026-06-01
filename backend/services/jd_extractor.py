import json

from schemas.analysis import AIAnalysisResult
from services.deepseek_client import chat_json
from prompts.jd_extraction import JD_EXTRACTION_PROMPT
from prompts.system_prompt import SYSTEM_PROMPT


async def extract_jd(job_description: str) -> dict:
    """从 JD 文本中提取结构化信息"""
    user_message = f"请分析以下岗位 JD:\n\n{job_description}"
    result = await chat_json(
        system_prompt=JD_EXTRACTION_PROMPT,
        user_message=user_message,
        max_tokens=1024,
        temperature=0.2,
    )
    return result


async def run_ai_analysis(
    resume_text: str,
    job_description: str,
    jd_extracted: dict | None = None,
) -> AIAnalysisResult:
    """调用 AI 对简历和 JD 进行语义匹配分析"""
    jd_context = ""
    if jd_extracted:
        jd_context = f"\n\nJD 结构化提取结果:\n{json.dumps(jd_extracted, ensure_ascii=False, indent=2)}"

    user_message = f"""请分析以下简历与岗位的匹配度。

## 简历内容:
{resume_text}

## 岗位 JD:
{job_description}{jd_context}

请根据简历和 JD 生成完整匹配分析报告，只输出合法 JSON。"""

    result = await chat_json(
        system_prompt=SYSTEM_PROMPT,
        user_message=user_message,
        max_tokens=4096,
        temperature=0.3,
    )
    return AIAnalysisResult(**result)
