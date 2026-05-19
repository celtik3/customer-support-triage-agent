from typing import TypedDict, Optional


class AgentState(TypedDict):
    raw_request: str
    sanitized_request: Optional[str]
    classification: Optional[str]
    triage_summary: Optional[str]
    draft_response: Optional[str]
    safety_review: Optional[str]
    final_response: Optional[str]
    injection_detected: Optional[bool]
    error: Optional[str]