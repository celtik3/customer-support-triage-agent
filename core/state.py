from typing import TypedDict, Optional, List


class AgentState(TypedDict):
    raw_request: str
    sanitized_request: Optional[str]
    classification: Optional[str]
    triage_summary: Optional[str]
    draft_response: Optional[str]
    safety_review: Optional[str]
    final_response: Optional[str]
    injection_detected: Optional[bool]
    escalation_required: Optional[bool]
    recommended_team: Optional[str]
    escalation_reason: Optional[str]
    confidence_score: Optional[float]
    agent_trace: Optional[List[str]]
    error: Optional[str]