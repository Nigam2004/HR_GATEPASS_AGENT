
from typing import TypedDict, Optional, Any


class AgentState(TypedDict, total=False):

    # 1. Document upload
    thread_id: str
    documents: list[dict]
    document_count: int

    # 2. AI extraction
    extracted_details: list[dict]

    # 3. Document comparison
    comparisons: list[dict]
    mismatches: list[dict]
    worker_profile: dict

    # 4. HR correction
    corrections: dict
    correction_history: list[dict]
    corrections_applied: bool

    # 5. Profile validation
    validation_result: dict
    validation_errors: list[str]
    verified_corrections:list[str]
    is_valid: bool

    # 6. HR profile approval
    profile_confirmed: bool
    profile_approved_by: Optional[str]

    # 7. Portal field mapping
    mapped_data: dict

    # 8. Playwright automation
    captcha_images:list[dict]
    portal_status: str
    portal_filled: bool
    portal_screenshot: Optional[str]

    # 9. Final submission approval
    final_approval: bool
    final_approved_by: Optional[str]

    # 10. Final result
    submission_result: dict
    gatepass_reference: Optional[str]

    # Workflow tracking
    workflow_status: str
    current_step: str
    errors: list[str]
