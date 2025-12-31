import streamlit as st
import requests
import json
import uuid

user_id = str(uuid.uuid4())

BACKEND_URL = "http://localhost:5000"

if "history" not in st.session_state:
    st.session_state.history = []
if "selected_personality" not in st.session_state:
    st.session_state.selected_personality = ""
if "user_id" not in st.session_state:
    st.session_state.user_id = user_id

st.title("🎭 人格穿越聊天")

@st.cache_data
def get_personality_list():
    try:
        res = requests.get(f"{BACKEND_URL}/api/personalities")
        return res.json()["data"]
    except Exception as e:
        st.error(f"获取人格列表失败：{e}")
        return []

personalities = get_personality_list()
if personalities:
    st.session_state.selected_personality = st.selectbox(
        "选择聊天人格",
        personalities,
        index=0 if st.session_state.selected_personality == "" else personalities.index(st.session_state.selected_personality)
    )
is_ready = False

if not is_ready:
    st.button("准备开始", on_click=lambda: setattr(st.session_state, "is_ready", True))

st.subheader("💬 聊天窗口")

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

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
                    "personality_name": st.session_state.selected_personality,
                    "user_input": user_input,
                    "history": json.dumps(st.session_state.history[:-1])  # 传递历史对话
                }
            )
            if res.json()["code"] == 200:
                reply = res.json()["data"]["reply"]
                # 添加AI回复到历史
                st.session_state.history.append({"role": "assistant", "content": reply})
                with st.chat_message("assistant"):
                    st.markdown(reply)
            else:
                st.error(res.json()["msg"])
        except Exception as e:
            st.error(f"聊天失败：{e}")