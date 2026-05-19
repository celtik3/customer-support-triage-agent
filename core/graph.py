from langgraph.graph import StateGraph, END
from core.state import AgentState

from agents.intake_router import intake_router_agent
from agents.documentation_specialist import documentation_specialist_agent
from agents.guardrail_critic import guardrail_critic_agent


def route_after_intake(state: dict):
    """
    Decide next node after intake routing.
    """
    if state.get("injection_detected"):
        return "guardrail_critic"

    return "documentation_specialist"


builder = StateGraph(AgentState)

## Nodes
builder.add_node("intake_router", intake_router_agent)
builder.add_node("documentation_specialist", documentation_specialist_agent)
builder.add_node("guardrail_critic", guardrail_critic_agent)

## Entry
builder.set_entry_point("intake_router")

## Conditional routing
builder.add_conditional_edges(
    "intake_router",
    route_after_intake,
    {
        "documentation_specialist": "documentation_specialist",
        "guardrail_critic": "guardrail_critic",
    },
)

## Normal flow
builder.add_edge("documentation_specialist", "guardrail_critic")

## End
builder.add_edge("guardrail_critic", END)

graph = builder.compile()