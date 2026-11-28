import uuid
from pathlib import Path
from fastapi import APIRouter, File, HTTPException, UploadFile
from langgraph.types import Command
from pydantic import BaseModel
from app.core.config import EXPECTED_PDF_COUNT
from app.graph.workflow import agent
from app.schemas.requests import CorrectionRequest,ProfileApproval,ValidationRequest,CaptchaRequest
from app.services.ai_extractor import extract_worker_details
from app.services.pdf_service import save_pdf_and_extract_name
from app.services.sarvam_extracter import extract_worker_document
from datetime import datetime

import traceback

router = APIRouter()


def _thread_config(thread_id: str) -> dict:
    return {"configurable": {"thread_id": thread_id}}


def _format_result(result: dict) -> dict:
    pending = result.get("__interrupt__", [])
    if pending:
        return {
            "paused": True,
            "request": [item.value for item in pending],
        }

    return {
        "paused": False,
        "workflow_status": result.get("workflow_status"),
        "worker_profile": result.get("worker_profile"),
        "portal_status": result.get("portal_status"),
    }

#list[UploadFile]

##upload documents- Router
@router.post("/validate-documents")
async def validate_documents(files:list[UploadFile] = File(...)):
    print("api called=",datetime.now())
    if len(files) != EXPECTED_PDF_COUNT:
        raise HTTPException(
            status_code=400,
            detail=f"Upload exactly {EXPECTED_PDF_COUNT} PDF files.",
        )
    thread_id = str(uuid.uuid4())
    documents = []
    records = []

    try:
        for upload in files:
            document = await save_pdf_and_extract_name(upload, thread_id)
            print("pdf saved",datetime.now())
            details =await extract_worker_document(document["path"],document["document_type"])
            print("ai doc extracted",datetime.now())

            record = {
                **details,
                "filename": document["filename"],
            }
            records.append(record)
            documents.append(document)
        print("loop ended ",datetime.now())
        print("ALL DOCUMENTS EXTRACTED")

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=(
                "AI extraction failed. Check the Gemini API key, model "
                "configuration, network connection, and API quota."
            ),
        ) from exc
    finally:
        for upload in files:
            await upload.close()

    initial_state = {
        "documents": documents,
        "extracted_details": records,
        "mismatches": [],
        "worker_profile": {},
        "corrections": {},
        "profile_confirmed": False,
        "workflow_status": "started",
        "portal_status": "not_started",
        "comparisons":[]
    }

    result = agent.invoke(initial_state, config=_thread_config(thread_id))
    # print("rse",result)
    print("comparing the details",datetime.now())
    # {"thread_id": thread_id, **_format_result(result)}
    return {"thread_id": thread_id, **_format_result(result),**result}
# print("result",datetime.now())

# ##resolve mismatches-router
@router.post("/resolve-mismatches/{thread_id}")
def submit_corrections(thread_id: str, request: CorrectionRequest):
    try:
        result = agent.invoke(
            Command(resume=request.corrections),
            config=_thread_config(thread_id),
        )

    except Exception as exc:
        print("ERROR:", repr(exc))
        traceback.print_exc()
        raise HTTPException(
            status_code=400,
            detail=(
                "Could not apply corrections. Check the thread ID and "
                "outstanding mismatch fields."
            ),
        ) from exc

    return {"thread_id": thread_id, **_format_result(result),**result}

#validatio review
@router.post("/validation-review/{thread_id}")
def approve_profile(thread_id: str, request: ValidationRequest):
    print(request.verified_fields)
    print(type(request.verified_fields))
    try:
        result = agent.invoke(
            Command(resume=request.verified_fields),
            config=_thread_config(thread_id),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=(
                "Could not process validation review."
            ),
        ) from exc

    return {"thread_id": thread_id, **_format_result(result),**result}

##confirm router
@router.post("/confirm-profile/{thread_id}")
async def approve_profile(thread_id: str, request: ProfileApproval):
    print(request)
    try:
        result =agent.invoke(
            Command(resume={"approved": request.approved}),
            config=_thread_config(thread_id),
        )
    except Exception as exc:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=400,
            detail=(
                "Could not confirm profile. Check the thread ID and"
                "pending workflow stage."
            ),
        ) from exc

    return {"thread_id": thread_id, **_format_result(result),**result}

@router.post("/mantra/{thread_id}/captcha")
def approve_profile(thread_id: str, request: CaptchaRequest):
    print(request.captcha_text)
    print(type(request.captcha_text))
    try:
        result = agent.ainvoke(
            Command(resume=request.captcha_text),
            config=_thread_config(thread_id),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=(
                "Could not process validation review."
            ),
        ) from exc

    return {"message": "CAPTCHA submitted successfully", 
            **_format_result(result),**result}


# ## get result router
@router.get("/status/{thread_id}")
def workflow_status(thread_id: str):
    snapshot = agent.get_state(_thread_config(thread_id))
    if not snapshot.values and not snapshot.next:
        raise HTTPException(status_code=404, detail="Workflow thread not found.")

    return {
        "thread_id": thread_id,
        "values": snapshot.values,
        "next_steps": list(snapshot.next),
    }
