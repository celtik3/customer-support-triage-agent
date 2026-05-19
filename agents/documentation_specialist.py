from core.llm import llm


def documentation_specialist_agent(state: dict) -> dict:
    """
    Converts the customer request into structured triage documentation
    and drafts a professional support response.
    """

    sanitized_request = state.get("sanitized_request", "")
    classification = state.get("classification", "general_support")

    if classification == "security_risk":
        return {
            **state,
            "triage_summary": "Request flagged as potential security risk.",
            "draft_response": "Request blocked pending security review."
        }

    prompt = f"""
You are a documentation specialist in a customer support triage system.

Your job is to transform an unstructured customer support request into a structured internal triage record.

Customer request:
{sanitized_request}

Classification:
{classification}

Create the response in EXACTLY this structure:

Category:
Urgency Level:
Dietary Needs:
Health/Safety Risks:
Behavioral Considerations:
Mobility/Accessibility Needs:
Communication Needs:
Recommended Next Step:
Draft Customer Response:

Rules:
- For Urgency Level, choose exactly one: Low, Medium, High
- If a section does not apply, write "None"
- Keep professional tone
- Do NOT provide medical advice
- Do NOT invent policies
- Draft Customer Response should be short and professional
"""

    response = llm.invoke(prompt)
    content = response.content

    return {
        **state,
        "triage_summary": content,
        "draft_response": "Draft included inside triage summary."
    }