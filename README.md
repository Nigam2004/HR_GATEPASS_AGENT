# HR Gate Pass Agent

A FastAPI + Gemini + LangGraph starter project for extracting worker details from PDF documents, comparing values across documents, and pausing for human review before any portal automation.

## Project structure

```text
hr_gatepass_agent/
├── main.py
├── pyproject.toml
├── .env
├── .env.example
├── .gitignore
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── api/
│   │   ├── router.py
│   │   └── routes.py
│   ├── schemas/
│   │   ├── worker.py
│   │   └── requests.py
│   ├── services/
│   │   ├── pdf_service.py
│   │   ├── ai_extractor.py
│   │   └── comparison_service.py
│   └── graph/
│       ├── state.py
│       ├── nodes.py
│       └── workflow.py
├── uploads/
└── checkpoints.sqlite  # created automatically when the app starts
```

## 1. Configure the project

Open PowerShell in this folder:

```powershell
uv sync
```

Open `.env` and replace the placeholder with your Gemini API key:

```env
GOOGLE_API_KEY=your_actual_google_api_key
GEMINI_MODEL=gemini-2.5-flash
```

Keep `.env` private. It is excluded by `.gitignore`.

## 2. Run the API

```powershell
uv run uvicorn main:app --reload
```

Open the interactive API documentation:

- http://127.0.0.1:8000/docs

## 3. Workflow endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Health check |
| POST | `/validate-documents` | Upload exactly five text-based PDF files and start extraction |
| POST | `/resolve-mismatches/{thread_id}` | Submit corrections for fields that disagree |
| POST | `/confirm-profile/{thread_id}` | Approve or reject the complete worker profile |
| GET | `/status/{thread_id}` | Inspect saved workflow state |

### Upload

In Swagger UI, open `POST /validate-documents`, choose exactly five PDF files, and execute.

The response includes a `thread_id`. Save it for the remaining requests.

### Resolve mismatches

Only call this endpoint when the workflow response is paused with `type: mismatch_review`.

Example request body:

```json
{
  "corrections": {
    "name": "Correct worker name"
  }
}
```

Use only the field names listed in the mismatch response.

### Confirm profile

When the workflow is paused with `type: profile_confirmation`, review every field and then send:

```json
{
  "approved": true
}
```

To reject the profile, send `false`.

## 4. Important current limitations

- The upload endpoint currently requires exactly five PDF files.
- PDFs must contain selectable/extractable text. Scanned PDFs need OCR, which is not included yet.
- The identity-number field stores only the last four digits, as requested in the extraction prompt.
- The first value found is only a draft. Conflicting values are sent for human review.
- SQLite stores LangGraph checkpoints locally.
- Playwright / Mantra portal integration is not implemented. Even after approval, this starter project does not log in, fill fields, upload documents, or submit anything.
- Do not use real worker documents until you have reviewed access controls, retention, encryption, audit logging, and applicable privacy requirements.

## 5. Main responsibilities

- `core/config.py`: environment variables and project paths.
- `core/database.py`: SQLite LangGraph checkpoint storage.
- `schemas/worker.py`: extracted worker data schema and comparable fields.
- `schemas/requests.py`: API request bodies.
- `services/pdf_service.py`: PDF validation, saving, and text extraction.
- `services/ai_extractor.py`: Gemini structured extraction.
- `services/comparison_service.py`: compare extracted values and identify mismatches.
- `graph/state.py`: shared LangGraph state.
- `graph/nodes.py`: workflow node logic and human-review interrupts.
- `graph/workflow.py`: connect and compile the LangGraph workflow.
- `api/routes.py`: HTTP endpoints.
- `api/router.py`: API route registration.
- `main.py`: create the FastAPI application.
