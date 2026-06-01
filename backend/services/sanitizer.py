import re

# 脱敏规则：需求文档 4.9.3
PATTERNS = [
    (re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"), "[EMAIL]"),
    # 注意: replacement 不能为 None，Python 3.13 的 re.sub 会报错
    (re.compile(r"1[3-9]\d\s?-?\d{4}\s?-?\d{4}"), "[PHONE]"),
    (re.compile(r"https?://github\.com/\S+"), "[URL]"),
    (re.compile(r"https?://[^\s)]+"), "[URL]"),
]


def sanitize(text: str) -> str:
    """对简历文本进行隐私脱敏"""
    for pattern, replacement in PATTERNS:
        text = pattern.sub(replacement, text)
    return text
