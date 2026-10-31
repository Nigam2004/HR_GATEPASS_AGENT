from pydantic import BaseModel, Field


class WorkerDetails(BaseModel):
    document_type: str = Field(description="Type of document")
    name: str | None = None
    father_name: str | None = None
    date_of_birth: str | None = None
    uan: str | None = None
    esic_number: str | None = None
    bank_account_number: str | None = None
    ifsc: str | None = None
    identity_number_last4: str | None = None
    driving_licence_number: str | None = None


WORKER_FIELDS = [
    "name",
    "father_name",
    "date_of_birth",
    "uan",
    "esic_number",
    "bank_account_number",
    "ifsc",
    "identity_number_last4",
    "driving_licence_number",
]
