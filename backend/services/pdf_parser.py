import io

import pdfplumber


class PDFParseResult:
    def __init__(self, full_text: str, pages: list[dict]):
        self.full_text = full_text
        self.pages = pages  # [{"page": 1, "text": "..."}, ...]

    @property
    def text_length(self) -> int:
        return len(self.full_text)


def parse_pdf(file_bytes: bytes) -> PDFParseResult:
    pages = []
    full_text_parts = []

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            pages.append({"page": i, "text": text})
            full_text_parts.append(text)

    full_text = "\n".join(full_text_parts)
    return PDFParseResult(full_text=full_text, pages=pages)


def is_likely_scanned(text: str, min_chars: int = 100) -> bool:
    """Returns True if text is too short, likely a scanned/image PDF."""
    return len(text.strip()) < min_chars
