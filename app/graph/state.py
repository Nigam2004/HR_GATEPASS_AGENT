from typing import TypedDict


class AgentState(TypedDict):
    documents: list[dict]
    extracted_details: list[dict]
    mismatches: list[dict]
    worker_profile: dict
    corrections: dict
    profile_confirmed: bool
    workflow_status: str
    portal_status: str
