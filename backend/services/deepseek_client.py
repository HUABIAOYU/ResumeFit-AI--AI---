import json
import logging

from openai import AsyncOpenAI

from config import settings

logger = logging.getLogger(__name__)

_client: AsyncOpenAI | None = None


def get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
        )
    return _client


async def chat_json(
    system_prompt: str,
    user_message: str,
    max_tokens: int = 4096,
    temperature: float = 0.3,
) -> dict:
    """调用 DeepSeek 并要求返回 JSON，解析失败自动重试一次"""
    client = get_client()

    for attempt in range(2):
        try:
            response = await client.chat.completions.create(
                model=settings.deepseek_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                response_format={"type": "json_object"},
            )
            raw = response.choices[0].message.content
            return json.loads(raw)
        except (json.JSONDecodeError, Exception) as e:
            logger.warning(f"DeepSeek 调用失败 (attempt {attempt + 1}): {e}")
            if attempt == 1:
                raise
    return {}
