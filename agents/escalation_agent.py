from core.llm import llm


def escalation_agent(state: dict) -> dict:
    """
    Determines whether the support request should be escalated
    to a human team before final handling.
    """

    classification = state.get("classification", "")
    triage_summary = state.get("triage_summary", "")
    injection_detected = state.get("injection_detected", False)

    if injection_detected:
        return {
            **state,
            "escalation_required": True,
            "recommended_team": "Security Review",
            "escalation_reason": "Prompt injection or unsafe instruction detected.",
        }

    prompt = f"""
You are an escalation decision agent for a customer support triage workflow.

Review the classification and triage summary.

Classification:
{classification}

Triage Summary:
{triage_summary}

Decide whether this case requires human escalation.

Return EXACTLY this format:

Escalation Required: Yes or No
Recommended Team:
Reason:

Rules:
- Escalate health/safety risks to Safety Team
- Escalate accessibility or mobility needs to Accessibility Support Team
- Escalate unclear or high-risk requests to Human Review
- Routine general support can remain unescalated
- Do not provide medical or legal advice
"""

    response = llm.invoke(prompt)
    content = response.content

    escalation_required = "Escalation Required: Yes" in content

    recommended_team = "General Support"
    escalation_reason = content

    for line in content.splitlines():
        if line.startswith("Recommended Team:"):
            recommended_team = line.replace("Recommended Team:", "").strip()
        if line.startswith("Reason:"):
            escalation_reason = line.replace("Reason:", "").strip()

    trace = state.get("agent_trace") or []
    trace.append(
        f"Escalation Agent: escalation_required={escalation_required}, recommended_team='{recommended_team}'"
    )
    
    return {
        **state,
        "escalation_required": escalation_required,
        "recommended_team": recommended_team,
        "escalation_reason": escalation_reason,
        "agent_trace": trace,
    }