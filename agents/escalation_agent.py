from core.llm import llm


def escalation_agent(state: dict) -> dict:
    """
    Determines whether an enterprise client request should be escalated
    to a specialized technical or security team.
    """

    classification = state.get("classification", "")
    triage_summary = state.get("triage_summary", "")
    injection_detected = state.get("injection_detected", False)

    if injection_detected:
        trace = state.get("agent_trace") or []
        trace.append("Escalation Agent: routed request to Security Review due to prompt injection.")

        return {
            **state,
            "escalation_required": True,
            "recommended_team": "Security Review",
            "escalation_reason": "Prompt injection or unsafe instruction detected.",
            "agent_trace": trace,
        }

    prompt = f"""
You are an escalation decision agent for a forward-deployed AI implementation workflow.

Review the classification and requirements summary.

Classification:
{classification}

Requirements Summary:
{triage_summary}

Decide whether this case requires human escalation.

Return EXACTLY this format:

Escalation Required: Yes or No
Recommended Team:
Reason:

Rules:
- Escalate security/compliance or access-control concerns to Security Review
- Escalate data integration, databases, APIs, CRMs, or multi-source data work to Data Engineering
- Escalate multi-system architecture requests to Solution Architect
- Escalate deployment, infrastructure, or production rollout concerns to Platform/DevOps Team
- Routine workflow automation can go to Implementation Team
- If unclear or high-risk, escalate to Human Review
- Do not invent company policies or technical guarantees
"""

    response = llm.invoke(prompt)
    content = response.content

    escalation_required = "Escalation Required: Yes" in content

    recommended_team = "Implementation Team"
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