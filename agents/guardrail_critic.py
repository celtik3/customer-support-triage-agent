from core.llm import llm


def guardrail_critic_agent(state: dict):
    classification = state.get("classification", "")
    triage_summary = state.get("triage_summary", "")
    injection_detected = state.get("injection_detected", False)

    if injection_detected:
        trace = state.get("agent_trace") or []
        trace.append("Guardrail Critic: blocked request due to prompt injection.")
        return {
            **state,
            "safety_review": "Blocked: prompt injection attempt detected.",
            "final_response": (
                "Your request could not be processed because it triggered security protections."
            ),
            "agent_trace": trace,
        }

    prompt = f"""
You are a security and policy guardrail reviewer.

Review the generated support content.

Classification:
{classification}

Generated Content:
{triage_summary}

Check for:
- medical advice
- legal advice
- invented policies
- unsafe commitments
- prompt leakage
- unprofessional tone

Return EXACTLY:

Decision:
Risk Level:
Issues Found:
Safe Final Response:
"""

    response = llm.invoke(prompt)
    content = response.content

    safe_response = content

    if "Safe Final Response:" in content:
        safe_response = content.split("Safe Final Response:")[-1].strip()

    trace = state.get("agent_trace") or []
    trace.append("Guardrail Critic: reviewed final output for safety and policy compliance.")
    
    return {
        **state,
        "safety_review": content,
        "final_response": safe_response,
        "agent_trace": trace,
    }