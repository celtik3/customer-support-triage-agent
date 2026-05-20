import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.graph import graph


def test_full_pipeline_enterprise_case():
    state = {
        "raw_request": "We want an AI assistant that reads Zendesk tickets and creates Jira tasks.",
        "sanitized_request": None,
        "classification": None,
        "triage_summary": None,
        "draft_response": None,
        "safety_review": None,
        "final_response": None,
        "injection_detected": None,
        "escalation_required": None,
        "recommended_team": None,
        "escalation_reason": None,
        "confidence_score": None,
        "agent_trace": [],
        "error": None,
    }

    result = graph.invoke(state)

    assert result["classification"] in [
        "workflow_automation",
        "data_integration",
        "ai_llm_use_case"
    ]