from langchain.agents import AgentState, create_agent
from model import chat_Model
from langgraph.checkpoint.memory import InMemorySaver
from src.agent.tools.web_search import web_search

class ChatAgentConfig(AgentState):
    personality_name: str
    user_id: str

def create_chat_agent(prompt_template,personality_name,user_id):
    config = ChatAgentConfig(
        personality_name=personality_name,
        user_id=user_id,
    )
    return create_agent(
        model=chat_Model,
        tools=[web_search],
        state_schema=ChatAgentConfig,
        checkpoint=InMemorySaver(),
        system_prompt=prompt_template,
    )
