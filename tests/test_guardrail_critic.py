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
