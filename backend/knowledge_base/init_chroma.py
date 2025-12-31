import json
import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv



load_dotenv()

embeddings = DashScopeEmbeddings(
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="text-embedding-v4",
)

def load_personality_json():
    json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "personalities.json")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

# 将人格模板转化为Document
def convert_to_documents(personalities):
    documents = []
    for p in personalities:
        # Document内容：整合所有模板字段，便于检索
        content = f"""
        人格名称：{p['name']}
        背景：{p['background']}
        性格特征：{','.join(p['personality_traits'])}
        语言风格：{p['dialogue_style']}
        提示词模板：{p['prompt_template']}
        """
        # 元数据：便于精准过滤（比如按名称检索）
        metadata = {
            "personality_name": p['name'],
            "core_traits": ','.join(p['personality_traits'])
        }
        documents.append(Document(page_content=content, metadata=metadata))
    return documents

# 初始化并保存向量库
def init_chroma_kb():
    # 加载JSON并转化为Document
    personalities = load_personality_json()
    docs = convert_to_documents(personalities)
    
    # 创建Chroma向量库（存储到本地backend/knowledge_base/chroma_db目录）
    kb_path = os.path.join(os.path.dirname(__file__), "chroma_db")
    db = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=kb_path
    )
    db.persist()  # 持久化向量库
    print(f"✅ 人格模板知识库初始化完成，共导入{len(docs)}个人格，存储路径：{kb_path}")

if __name__ == "__main__":
    init_chroma_kb()