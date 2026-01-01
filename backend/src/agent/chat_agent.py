import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from langchain.agents import AgentState, create_agent
from model import chat_Model
from langgraph.checkpoint.memory import InMemorySaver
from agent.tools.web_search import web_search

class ChatAgentConfig(AgentState):
    personality_name: str
    user_id: str

def create_chat_agent(prompt_template):

    return create_agent(
        model=chat_Model,
        tools=[web_search],
        state_schema=ChatAgentConfig,
        checkpointer=InMemorySaver(),
        system_prompt=prompt_template,
    )

def invoke_chat_agent(agent, query: str, personality_name: str, user_id: str):

    

    return agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ],
            "personality_name": personality_name,
            "user_id": user_id,
        },
        {"configurable": {"thread_id": user_id}},
    )

if __name__ == "__main__":

    agent = create_chat_agent(
        prompt_template="你现在是《甄嬛传》中的钮祜禄·甄嬛（太后），必须完全模仿他的人格与语言风格：\n1. 背景：{background}\n2. 性格：{personality_traits}\n3. 说话风格：{dialogue_style}\n4. 强制规则：\n- 回复必须带至少1个核心口头禅，自称优先用“本宫/哀家”（根据语境选）；\n- 语气沉稳，用“想来”“终究”“未必”等词，避免直白/冲动表达；\n- 聊到权谋/人情/选择时，必须点透人心，但不把话说绝，留有余地；\n- 句式以陈述句为主，少感叹，体现太后的冷静与城府。",
    )
    # res = agent.invoke(
    #     {
    #         "message":[{
    #             "role":"user",
    #             "content":"你好"
    #         }],
    #         "personality_name":"甄嬛",
    #         "user_id":"123",
    #     },
    #     {"configurable": {"thread_id": "1"}},
    # )
    # print(res)
    res = invoke_chat_agent(
        agent,
        query="你好",
        personality_name="甄嬛",
        user_id="123",
    )
    print(res)