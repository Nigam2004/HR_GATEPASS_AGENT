from pathlib import Path
from uuid import UUID

import fitz
from fastapi import UploadFile

from app.core.config import MAX_FILE_SIZE, UPLOAD_DIR


async def save_pdf_and_extract_text(
    upload: UploadFile,
    thread_id: str,
) -> tuple[dict, str]:
    """Save one PDF and return its metadata plus extracted text."""
    filename = Path(upload.filename or "").name

    if not filename or not filename.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are accepted.")

    content = await upload.read()

    if not content or len(content) > MAX_FILE_SIZE:
        raise ValueError(f"Invalid or oversized PDF: {filename}")

    worker_folder = UPLOAD_DIR / str(UUID(thread_id))
    worker_folder.mkdir(parents=True, exist_ok=True)

    # Prefix the saved file to avoid collisions between duplicate filenames.
    saved_path = worker_folder / f"{len(list(worker_folder.iterdir())) + 1}_{filename}"
    saved_path.write_bytes(content)

    try:
        with fitz.open(stream=content, filetype="pdf") as pdf:
            text = "\n".join(page.get_text() for page in pdf)
    except Exception as exc:
        saved_path.unlink(missing_ok=True)
        raise ValueError(f"Could not read {filename} as a valid PDF.") from exc

    if not text.strip():
        saved_path.unlink(missing_ok=True)
        raise ValueError(
            f"{filename} has no extractable text. OCR support is required for scanned PDFs."
        )

    document = {
        "filename": filename,
        "path": str(saved_path),
    }
    return document, text
