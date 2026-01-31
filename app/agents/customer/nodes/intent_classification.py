from pydantic import BaseModel, Field
from typing import Literal
from langchain.messages import SystemMessage, HumanMessage
from langfuse import observe

from app.agents.customer.utils.models import llm_call_with_structured_output
from app.agents.customer.prompts.intent_classification import system_prompt
from app.agents.customer.states.customer import CustomerState


class IntentClassification(BaseModel):
    intent: Literal["general_chat", "service_suggestion"] = Field(
        description=(
            "The classified intent of the user input. "
            "'service_suggestion' is used when the user explicitly asks for service recommendations or describes symptoms/issues with their car. "
            "'general_chat' is used for general inquiries about the organization, policies, or normal conversation that does not involve service recommendations."
        )
    )


@observe
async def classify_intent(state: CustomerState):
    """
    Classify the intent of the user input as either 'general_chat' or 'service_suggestion'.
    """
    user_query = state.messages[-1].content
    
    result = await llm_call_with_structured_output([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Classify the following user input: '{user_query}'")
    ], IntentClassification)

    return result.intent
