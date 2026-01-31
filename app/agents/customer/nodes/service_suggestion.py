from langchain.messages import SystemMessage
from langfuse import observe
from typing import List, Dict, Any

from app.services.service import recommend_service as service_recommendation
from app.database.dependencies import db_session
from app.agents.customer.states.customer import CustomerState
from app.agents.customer.utils.models import llm_call_with_tools
from app.agents.customer.prompts.service_suggestion import system_prompt

# LLM Tool
async def recommend_service(query: str) -> List[Dict[str, Any]]:
    """
    Recommends car services based on user query or symptoms.
    
    Args:
        query: User's query describing car issues, symptoms, or service needs
    """
    async with db_session() as db:
        return await service_recommendation(query, db)


@observe
async def service_suggestion(state: CustomerState):
    """Service suggestion node with tool binding"""
    
    tools = [recommend_service]
    messages = [SystemMessage(content=system_prompt), *state.messages]
    
    response = await llm_call_with_tools(messages, tools)
    
    return {"messages": [response]}
