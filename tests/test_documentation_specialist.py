import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.documentation_specialist import documentation_specialist_agent


state = {
    "raw_request": "The customer has a severe peanut allergy and requires separate food handling.", 
    "sanitized_request": "The customer has a severe peanut allergy and requires separate food handling.",
    "classification": "health_safety",
    "triage_summary": None,
    "draft_response": None,
    "safety_review": None,
    "final_response": None,
    "injection_detected": False,
    "error": None,
}

result = documentation_specialist_agent(state)

print(result["triage_summary"])