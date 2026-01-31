from langchain.messages import SystemMessage
from langfuse import observe

from app.agents.customer.states.customer import CustomerState
from app.agents.customer.utils.models import llm_call
from app.agents.customer.prompts.general_chat import system_prompt


@observe
async def general_chat(state: CustomerState):
    """General chat node with RAG retrieval for context"""
    
    # RAG retrieval will be implemented here
    
    
    response = await llm_call([SystemMessage(content=system_prompt), *state.messages])
    
    return {"messages": [response]}
