import os
import sys
from langchain_chroma import Chroma
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.model import embedding_Model
from dotenv import load_dotenv

load_dotenv()

_chroma_db = None

def get_chroma_db():
    global _chroma_db
    if _chroma_db is None:
        embeddings = embedding_Model
        kb_path = os.path.join(os.path.dirname(__file__), "../knowledge_base/chroma_db")
        _chroma_db = Chroma(
            persist_directory=kb_path,
            embedding_function=embeddings
        )
    return _chroma_db

def retrieve_personality(personality_name: str, top_k: int = 1):
    """
    从知识库检索指定人格模板
    :param personality_name: 人格名称（如“李白”“甄嬛”）
    :param top_k: 检索结果数量（默认1，精准匹配）
    :return: 格式化的人格模板字典，无结果返回None
    """
    db = get_chroma_db()
    
    retriever = db.as_retriever(
        search_kwargs={
            "k": top_k,
            "filter": {"personality_name": {"$eq": personality_name}}
        }
    )
    
    docs = retriever.invoke(personality_name)
    if not docs:
        return None
    
    doc_content = docs[0].page_content
    personality = {}
    
    name_line = [line for line in doc_content.split('\n') if "人格名称：" in line][0]
    personality["name"] = name_line.replace("人格名称：", "").strip()
    
    background_line = [line for line in doc_content.split('\n') if "背景：" in line][0]
    personality["background"] = background_line.replace("背景：", "").strip()
    
    traits_line = [line for line in doc_content.split('\n') if "性格特征：" in line][0]
    personality["personality_traits"] = traits_line.replace("性格特征：", "").strip().split(',')
    
    style_line = [line for line in doc_content.split('\n') if "语言风格：" in line][0]
    personality["dialogue_style"] = style_line.replace("语言风格：", "").strip()
    
    template_line = [line for line in doc_content.split('\n') if "提示词模板：" in line][0]
    template_start_index = doc_content.index("提示词模板：") + len("提示词模板：")
    personality["prompt_template"] = doc_content[template_start_index:].strip()
    
    return personality

def get_personality_prompt(personality_name: str):
    """
    从知识库获取人格模板，并格式化Prompt
    :param personality_name: 人格名称
    :param user_input: 用户输入
    :param history: 历史对话（可选，默认为空）
    :return: 格式化后的Prompt文本，无结果返回None
    """
    personality = retrieve_personality(personality_name)
    if not personality:
        return None
    
    prompt_template = personality["prompt_template"]
    formatted_prompt = prompt_template.format(
        background=personality["background"],
        personality_traits=','.join(personality["personality_traits"]),
        dialogue_style=personality["dialogue_style"],
    )
    return formatted_prompt

if __name__ == "__main__":
    print(get_personality_prompt("李白（字太白，号青莲居士）","你好"))