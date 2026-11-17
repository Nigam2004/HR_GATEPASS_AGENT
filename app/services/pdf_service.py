from pathlib import Path
from uuid import UUID
from app.schemas.worker import DOCUMENT_KEYWORDS
import fitz
from fastapi import UploadFile

from app.core.config import MAX_FILE_SIZE, UPLOAD_DIR


def detect_document_type(filename: str):

    # Get file name without extension
    filename = Path(filename).stem.lower()

    # Replace separators with spaces
    filename = filename.replace("-", " ").replace("_", " ")

    for document_type, keywords in DOCUMENT_KEYWORDS.items():

        for keyword in keywords:

            keyword = keyword.replace("_", " ")

            if keyword in filename:
                return document_type

    return None


async def save_pdf_and_extract_name(
    upload: UploadFile,
    thread_id: str,
) -> tuple[dict, str]:
    """Save one PDF and return its metadata plus extracted text."""
    print("PDF SAVED")
    filename = Path(upload.filename or "").name
    if not filename or not filename.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are accepted.")
    
    worker_folder = UPLOAD_DIR / str(UUID(thread_id))
    worker_folder.mkdir(parents=True, exist_ok=True)
    # Prefix the saved file to avoid collisions between duplicate filenames.
    saved_path = worker_folder / f"{len(list(worker_folder.iterdir())) + 1}_{filename}"

    try:
        content = await upload.read()
        if not content:
            raise ValueError("Uploaded PDF is empty.")
        
        if not content or len(content) > MAX_FILE_SIZE:
            raise ValueError(f"Invalid or oversized PDF: {filename}")
        
        saved_path.write_bytes(content)
        document_type = detect_document_type(filename)
        if not document_type:
            raise ValueError("Unable to identify document type from filename")
        print("PDF WRITE")
    
        # with fitz.open(stream=content, filetype="pdf") as pdf:
        #     text = "\n".join(page.get_text() for page in pdf)
        document = {
                "filename": filename,
                "path": str(saved_path),
                "document_type":document_type
            }
        return document
    except Exception:
        saved_path.unlink(missing_ok=True)
        raise

    # if not text.strip():
    #     saved_path.unlink(missing_ok=True)
    #     raise ValueError(
    #         f"{filename} has no extractable text. OCR support is required for scanned PDFs."
    #     )

    
