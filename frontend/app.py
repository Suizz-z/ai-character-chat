import streamlit as st
import requests
import json
import uuid
import random

user_id = str(uuid.uuid4())

BACKEND_URL = "http://localhost:5000"

if "history" not in st.session_state:
    st.session_state.history = []
if "selected_personality" not in st.session_state:
    st.session_state.selected_personality = ""
if "user_id" not in st.session_state:
    st.session_state.user_id = user_id
if "agent_created" not in st.session_state:
    st.session_state.agent_created = False
if "last_personality" not in st.session_state:
    st.session_state.last_personality = ""
if "show_personality_detail" not in st.session_state:
    st.session_state.show_personality_detail = False
if "personality_detail_data" not in st.session_state:
    st.session_state.personality_detail_data = None
if "conversation_round" not in st.session_state:
    st.session_state.conversation_round = 0
if "next_image_round" not in st.session_state:
    st.session_state.next_image_round = random.randint(3, 10)

st.title("🎭 人格穿越聊天")

st.sidebar.title("⚙️ 设置")

@st.cache_data
def get_personality_list():
    try:
        res = requests.get(f"{BACKEND_URL}/api/personalities")
        return res.json()["data"]
    except Exception as e:
        st.error(f"获取人格列表失败：{e}")
        return []

def create_agent(personality_name):
    try:
        res = requests.post(
            f"{BACKEND_URL}/api/createagent",
            json={"personality_name": personality_name}
        )
        return res.json()
    except Exception as e:
        st.error(f"创建 Agent 失败：{e}")
        return {"code": 500, "msg": str(e)}

def get_personality_detail(personality_name):
    try:
        res = requests.get(
            f"{BACKEND_URL}/api/personality-detail",
            params={"name": personality_name}
        )
        return res.json()
    except Exception as e:
        st.error(f"获取人格详情失败：{e}")
        return {"code": 500, "msg": str(e)}

def generate_image(personality_name, query):
    try:
        res = requests.post(
            f"{BACKEND_URL}/api/image",
            json={"personality_name": personality_name, "query": query}
        )
        return res.json()
    except Exception as e:
        st.error(f"生成图片失败：{e}")
        return {"code": 500, "msg": str(e)}

def format_personality_detail(personality):
    markdown = f"""
# 📖 {personality.get('name', '未知人格')}

## 🎭 背景
{personality.get('background', '暂无背景信息')}

## ✨ 性格特征
"""
    traits = personality.get('personality_traits', [])
    if traits:
        for trait in traits:
            markdown += f"- {trait}\n"
    else:
        markdown += "暂无性格特征\n"
    
    dialogue_style = personality.get('dialogue_style', '')
    if dialogue_style:
        markdown += "\n## 💬 对话风格\n"
        markdown += dialogue_style
    else:
        markdown += "\n## 💬 对话风格\n暂无对话风格信息"
    
    return markdown

def on_personality_change():
    if st.session_state.last_personality != "" and st.session_state.last_personality != st.session_state.selected_personality:
        st.session_state.agent_created = False
        st.session_state.history = []
        st.session_state.conversation_round = 0
        st.session_state.next_image_round = random.randint(3, 10)

personalities = get_personality_list()
if personalities:
    st.sidebar.selectbox(
        "选择聊天人格",
        personalities,
        index=0 if st.session_state.selected_personality == "" else personalities.index(st.session_state.selected_personality),
        key="selected_personality",
        on_change=on_personality_change
    )

if st.sidebar.button("🚀 创建 Agent"):
    if st.session_state.selected_personality:
        result = create_agent(st.session_state.selected_personality)
        if result["code"] == 200:
            st.session_state.agent_created = True
            st.session_state.last_personality = st.session_state.selected_personality
            st.sidebar.success("✅ Agent 创建成功！")
        else:
            st.sidebar.error(f"❌ {result['msg']}")
    else:
        st.sidebar.warning("⚠️ 请先选择一个人格")

if st.sidebar.button("📖 查看人格详情"):
    if st.session_state.selected_personality:
        result = get_personality_detail(st.session_state.selected_personality)
        if result["code"] == 200:
            st.session_state.show_personality_detail = True
            st.session_state.personality_detail_data = result["data"]
            st.sidebar.success("✅ 获取成功！")
        else:
            st.sidebar.error(f"❌ {result['msg']}")
    else:
        st.sidebar.warning("⚠️ 请先选择一个人格")

if "show_personality_detail" in st.session_state and st.session_state.show_personality_detail:
    with st.expander("📖 人格详情", expanded=True):
        markdown_content = format_personality_detail(st.session_state.personality_detail_data)
        st.markdown(markdown_content)
        
        with st.expander("🔍 调试信息（查看原始数据）"):
            st.json(st.session_state.personality_detail_data)
        
        if st.button("关闭"):
            st.session_state.show_personality_detail = False
            st.rerun()

st.markdown("---")

if not st.session_state.agent_created:
    st.warning("⚠️ 请先在左侧创建 Agent 才能开始聊天")
else:
    st.subheader("💬 聊天窗口")

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "image" in msg and msg["image"]:
                st.image(msg["image"], caption=f"{st.session_state.selected_personality}的动作", use_column_width=True)

    user_input = st.chat_input("输入你想聊的内容...")

    if user_input and st.session_state.selected_personality:
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.spinner("AI正在思考..."):
            try:
                res = requests.post(
                    f"{BACKEND_URL}/api/chat",
                    json={
                        "query": user_input,
                        "personality_name": st.session_state.selected_personality,
                        "user_id": st.session_state.user_id
                    }
                )
                if res.json()["code"] == 200:
                    reply = res.json()["data"]
                    st.session_state.conversation_round += 1
                    
                    msg_data = {"role": "assistant", "content": reply}
                    
                    if st.session_state.conversation_round >= st.session_state.next_image_round:
                        with st.spinner("正在生成人物动作图片..."):
                            image_result = generate_image(st.session_state.selected_personality, reply)
                            
                            if image_result["code"] == 200:
                                image_data = image_result["data"]
                                if isinstance(image_data, dict) and "image" in image_data:
                                    msg_data["image"] = image_data["image"]
                                elif isinstance(image_data, str):
                                    msg_data["image"] = image_data
                                
                                st.session_state.next_image_round = st.session_state.conversation_round + random.randint(3, 10)
                    
                    st.session_state.history.append(msg_data)
                    
                    with st.chat_message("assistant"):
                        st.markdown(reply)
                        if "image" in msg_data and msg_data["image"]:
                            st.image(msg_data["image"], caption=f"{st.session_state.selected_personality}的动作", width="auto")
                else:
                    st.error(res.json()["msg"])
            except Exception as e:
                st.error(f"聊天失败：{e}")