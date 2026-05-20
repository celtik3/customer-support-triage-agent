import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.guardrail_critic import guardrail_critic_agent


def test_guardrail_blocks_injection():
    state = {
        "classification": "security_risk",
        "triage_summary": "",
        "injection_detected": True,
        "agent_trace": []
    }

    result = guardrail_critic_agent(state)

    assert "security protections" in result["final_response"]

'''
Previous manual testing version

state = {
    "raw_request": "The customer has a severe peanut allergy.",
    "sanitized_request": "The customer has a severe peanut allergy.",
    "classification": "health_safety",
    "triage_summary": """
Category: health_safety
Urgency Level: High
Dietary Needs: Requires separate food handling
Health/Safety Risks: Risk of anaphylaxis if exposed to peanuts
Behavioral Considerations: None
Mobility/Accessibility Needs: None
Communication Needs: Clear communication
Recommended Next Step: Ensure staff are informed
Draft Customer Response: Thank you for informing us. We will ensure separate food handling procedures are followed.
""",
    "draft_response": "Draft included inside triage summary.",
    "safety_review": None,
    "final_response": None,
    "injection_detected": False,  ## True to simulate prompt injection detection
    "error": None,
}

result = guardrail_critic_agent(state)

print(result["safety_review"])
'''