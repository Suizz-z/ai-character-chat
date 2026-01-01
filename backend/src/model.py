import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings

load_dotenv()

chat_Model = ChatTongyi(
    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY"),
    model_name="qwen-max",
    timeout=80,
    streaming = True,
    # model_kwargs={
    #     "enable_thinking": True
    # }
    
)

embedding_Model = DashScopeEmbeddings(
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="text-embedding-v4",
)