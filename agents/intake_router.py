import re
from core.llm import llm


INJECTION_PATTERNS = [
    "ignore previous instructions",
    "reveal system prompt",
    "bypass guardrails",
    "act as unrestricted",
    "forget your instructions",
    "developer message",
    "system message",
]


def redact_pii(text: str) -> str:
    """Redact simple PII patterns before sending text forward."""
    text = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", "[REDACTED_EMAIL]", text)
    text = re.sub(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "[REDACTED_PHONE]", text)
    return text


def detect_prompt_injection(text: str) -> bool:
    """Detect obvious prompt injection attempts."""
    lower_text = text.lower()
    for pattern in INJECTION_PATTERNS:
        if pattern in lower_text:
            return True
    return False


def rule_based_classification(text: str) -> str | None:
    lower_text = text.lower()

    health_safety_keywords = [
        "severe allergy",
        "allergy",
        "allergic",
        "anaphylaxis",
        "peanut",
        "hazard",
        "unsafe",
        "injury",
        "emergency",
    ]

    mobility_keywords = [
        "wheelchair",
        "mobility",
        "walker",
        "accessible",
        "transportation",
        "stairs",
    ]

    dietary_keywords = [
        "low-sodium",
        "diet",
        "meal",
        "food preference",
        "vegetarian",
        "vegan",
        "gluten-free",
        "dairy-free"
    ]

    for keyword in health_safety_keywords:
        if keyword in lower_text:
            return "health_safety"

    for keyword in mobility_keywords:
        if keyword in lower_text:
            return "mobility_accessibility"

    for keyword in dietary_keywords:
        if keyword in lower_text:
            return "dietary_constraint"

    return None


def classify_request(text: str) -> str:
    """Use the LLM to classify the customer request."""
    prompt = f"""
You are an intake router for a customer support triage system.

Classify the request into exactly one category:

- dietary_constraint
- health_safety
- behavioral_consideration
- mobility_accessibility
- communication_need
- general_support

Return only the category name.

Customer request:
{text}
"""

    response = llm.invoke(prompt)
    return response.content.strip()


def intake_router_agent(state: dict) -> dict:
    """Main Intake Router agent node."""

    raw_request = state.get("raw_request", "")

    sanitized_request = redact_pii(raw_request)
    injection_detected = detect_prompt_injection(raw_request)

    rule_classification = None

    if injection_detected:
        classification = "security_risk"
    else:
        rule_classification = rule_based_classification(sanitized_request)

        if rule_classification:
            classification = rule_classification
        else:
            classification = classify_request(sanitized_request)

    if injection_detected:
        confidence_score = 0.99
    elif rule_classification:
        confidence_score = 0.95
    else:
        confidence_score = 0.80

    trace = state.get("agent_trace") or []
    trace.append(
        f"Intake Router: classified request as '{classification}', injection_detected={injection_detected}"
    )
    
    return {
        **state,
        "sanitized_request": sanitized_request,
        "classification": classification,
        "injection_detected": injection_detected,
        "confidence_score": confidence_score,
        "agent_trace": trace,
    }