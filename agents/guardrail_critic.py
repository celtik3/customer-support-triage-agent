from core.llm import llm


def guardrail_critic_agent(state: dict) -> dict:
    """
    Final safety and policy review agent.
    """

    classification = state.get("classification", "")
    triage_summary = state.get("triage_summary", "")
    injection_detected = state.get("injection_detected", False)

    if injection_detected:
        return {
            **state,
            "safety_review": "Blocked: prompt injection attempt detected.",
            "final_response": (
                "Your request could not be processed because it triggered "
                "security protections."
            ),
        }

    prompt = f"""
You are a security and policy guardrail reviewer.

Review the following generated support content.

Classification:
{classification}

Generated Content:
{triage_summary}

Check for ALL of the following:
- medical advice
- legal advice
- invented company policies
- unsafe commitments
- prompt leakage
- unprofessional tone
- risky escalation

Return EXACTLY in this format:

Decision: APPROVED or BLOCKED
Risk Level: LOW, MEDIUM, or HIGH
Issues Found:
Safe Final Response:

Rules:
- If content is acceptable, approve it
- If issues exist, rewrite a safer final response
- Keep tone professional
"""

    response = llm.invoke(prompt)
    content = response.content

    return {
        **state,
        "safety_review": content,
        "final_response": content,
    }