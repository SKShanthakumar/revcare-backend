from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode

from app.agents.customer.nodes.intent_classification import classify_intent
from app.agents.customer.nodes.general_chat import general_chat
from app.agents.customer.nodes.service_suggestion import service_suggestion, recommend_service
from app.agents.customer.states.customer import CustomerState


def build_customer_graph(checkpointer=None):
    """Build the car service recommedation graph"""
    
    builder = StateGraph(CustomerState)
    
    builder.add_node("general_chat", general_chat)
    builder.add_node("service_suggestion", service_suggestion)
    builder.add_node("tools", ToolNode([recommend_service]))
    
    builder.add_conditional_edges(START, classify_intent, ["general_chat", "service_suggestion"])
    
    # Add edges from nodes to END
    builder.add_edge("general_chat", END)
    builder.add_conditional_edges("service_suggestion", tools_condition)
    builder.add_edge("tools", "service_suggestion")
    builder.add_edge("tools", END)

    
    return builder.compile(checkpointer=checkpointer)


CustomerGraph = build_customer_graph()
