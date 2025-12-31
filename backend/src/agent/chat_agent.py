from langchain.agents import create_agent
from model import chat_Model
from langgraph.checkpoint.memory import InMemorySaver
from src.agent.tools.web_search import web_search


chat_agent = create_agent(
    model=chat_Model,
    tools=[web_search],
)

chat_agent.system_prompt = """
你是一个专业的占卜师，你的任务是根据用户的问题，提供专业的占卜结果。
"""