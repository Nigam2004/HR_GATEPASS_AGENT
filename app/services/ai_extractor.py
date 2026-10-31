from functools import lru_cache

from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import GOOGLE_API_KEY, GEMINI_MODEL
from app.schemas.worker import WorkerDetails


@lru_cache(maxsize=1)
def _get_structured_extractor():
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your_google_api_key_here":
        raise RuntimeError(
            "Set a valid GOOGLE_API_KEY in the project .env file before uploading PDFs."
        )

    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        api_key=GOOGLE_API_KEY,
        temperature=0,
    )
    return llm.with_structured_output(WorkerDetails)


def extract_worker_details(filename: str, document_text: str) -> dict:
    prompt = f"""
Extract the worker details from this document.

Filename: {filename}

Instructions:
- Preserve names and identifiers exactly as printed also remove if there is any Mr. .
- Do not guess missing values or correct spellings.
- Return null for missing information.
- For identity numbers, extract only the last four digits if the number is present.
-keep all the date in DD-MM-YYYY

Document text:
{document_text}
"""
    result = _get_structured_extractor().invoke(prompt)
    return result.model_dump()
