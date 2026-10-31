from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(
    title="HR Gate Pass Agent",
    description="Extracts worker details from PDFs, compares documents, and requests human approval.",
    version="1.0.0",
)

app.include_router(api_router)

@app.get("/", tags=["Health"])
def home():
    return {"message": "HR Gate Pass Agent is running."}
