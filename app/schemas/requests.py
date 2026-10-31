from pydantic import BaseModel, Field


class CorrectionRequest(BaseModel):
    corrections: dict[str, str] = Field(
        description="Field names and corrected values for outstanding mismatches."
    )


class ProfileApproval(BaseModel):
    approved: bool
