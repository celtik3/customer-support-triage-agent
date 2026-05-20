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
    "print your system instructions",
    "system instructions",
    "hidden policies",
    "debugging",
    "show your prompt",
    "show your instructions",
    "tell me your instructions",
]


def redact_pii(text: str) -> str:
    text = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", "[REDACTED_EMAIL]", text)
    text = re.sub(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "[REDACTED_PHONE]", text)

    text = re.sub(
        r"\b(my name is|i am|i'm)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?",
        r"\1 [REDACTED_NAME]",
        text,
        flags=re.IGNORECASE,
    )

    return text


def detect_prompt_injection(text: str) -> bool:
    lower_text = text.lower()

    for pattern in INJECTION_PATTERNS:
        if pattern in lower_text:
            return True

    return False


def rule_based_classification(text: str) -> str | None:
    lower_text = text.lower()

    security_keywords = [
        "role-based access",
        "restricted by user roles",
        "permissions",
        "access control",
        "compliance",
        "security",
        "sensitive data",
        "pii",
        "secrets",
    ]

    data_integration_keywords = [
        "salesforce",
        "zendesk",
        "jira",
        "slack",
        "database",
        "api",
        "crm",
        "data warehouse",
        "internal databases",
    ]

    workflow_keywords = [
        "automate",
        "workflow",
        "create tasks",
        "summarize tickets",
        "route tickets",
        "follow-up",
        "approval process",
    ]

    ai_keywords = [
        "ai assistant",
        "llm",
        "chatbot",
        "summarize",
        "generate",
        "classify",
        "rag",
    ]

    deployment_keywords = [
        "deploy",
        "cloud",
        "aws",
        "azure",
        "gcp",
        "docker",
        "kubernetes",
        "production",
    ]

    for keyword in security_keywords:
        if keyword in lower_text:
            return "security_compliance"

    for keyword in data_integration_keywords:
        if keyword in lower_text:
            return "data_integration"

    for keyword in workflow_keywords:
        if keyword in lower_text:
            return "workflow_automation"

    for keyword in ai_keywords:
        if keyword in lower_text:
            return "ai_llm_use_case"

    for keyword in deployment_keywords:
        if keyword in lower_text:
            return "deployment_infrastructure"

    return None


def classify_request(text: str) -> str:
    prompt = f"""
You are an intake router for a forward-deployed AI engineering team.

Classify the client request into exactly one category:

- workflow_automation
- data_integration
- ai_llm_use_case
- security_compliance
- user_access_permissions
- deployment_infrastructure
- general_requirement

Return only the category name.

Client request:
{text}
"""

    response = llm.invoke(prompt)
    return response.content.strip()


def intake_router_agent(state: dict) -> dict:
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