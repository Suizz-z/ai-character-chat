import streamlit as st
import requests
import json
import uuid
import random

# 页面基础配置
st.set_page_config(
    page_title="AI人格穿越聊天 - 多人格智能对话",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 全局样式定义（重点新增图片卡片样式）
st.markdown("""
<style>
    /* 全局基础样式 */
    .main {
        padding-top: 2rem;
    }
    
    /* 标题样式 */
    h1 {
        color: #1f2937;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* 侧边栏渐变背景 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    /* 侧边栏详情容器样式 */
    .sidebar-detail-container {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        max-height: 400px;
        overflow-y: auto;
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .sidebar-detail-content {
        color: white;
        font-size: 0.85rem;
        line-height: 1.4;
    }
    
    /* 侧边栏滚动条美化 */
    .sidebar-detail-container::-webkit-scrollbar {
        width: 4px;
    }
    .sidebar-detail-container::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 2px;
    }
    .sidebar-detail-container::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.3);
        border-radius: 2px;
    }
    .sidebar-detail-container::-webkit-scrollbar-thumb:hover {
        background: rgba(255,255,255,0.5);
    }
    
    /* 侧边栏所有文字强制白色 */
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* 侧边栏标题样式 */
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 {
        color: #ffffff !important;
        font-weight: 600;
    }
    
    /* 侧边栏下拉选择框样式修复 */
    [data-testid="stSidebar"] .stSelectbox {
        margin: 1rem 0;
    }
    [data-testid="stSidebar"] .stSelectbox > div:first-child {
        background-color: #1a252f !important;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 0.75rem;
        padding: 0.5rem;
        transition: all 0.3s ease;
    }
    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"],
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1a252f !important;
        color: #ffffff !important;
        width: 100%;
    }
    [data-testid="stSidebar"] .stSelectbox input,
    [data-testid="stSidebar"] .stSelectbox span {
        background-color: transparent !important;
        color: #ffffff !important;
        font-weight: 600;
        font-size: 1rem;
    }
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] svg {
        fill: #ffffff !important;
    }
    
    /* 侧边栏下拉选项列表样式 */
    [data-testid="stSidebar"] div[role="listbox"] {
        background-color: #1a252f !important;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 0.75rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        max-height: 300px;
        overflow-y: auto;
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] div[role="listbox"] div[role="option"] {
        background-color: transparent !important;
        color: #ffffff !important;
        padding: 0.75rem 1rem;
        margin: 0.25rem;
        border-radius: 0.5rem;
        transition: all 0.2s ease;
    }
    [data-testid="stSidebar"] div[role="listbox"] div[role="option"]:hover {
        background-color: rgba(52, 152, 219, 0.4) !important;
    }
    [data-testid="stSidebar"] div[role="listbox"] div[role="option"][aria-selected="true"] {
        background-color: #3498db !important;
        color: #ffffff !important;
        font-weight: 600;
    }
    
    /* 侧边栏按钮样式 */
    [data-testid="stSidebar"] button {
        background-color: rgba(255, 255, 255, 0.15) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.3);
        font-weight: 600;
    }
    [data-testid="stSidebar"] button:hover {
        background-color: rgba(255, 255, 255, 0.25) !important;
        border-color: rgba(255, 255, 255, 0.5);
    }
    [data-testid="stSidebar"] button[kind="primary"] {
        background-color: #3498db !important;
        border-color: #3498db !important;
    }
    [data-testid="stSidebar"] button[kind="primary"]:hover {
        background-color: #2980b9 !important;
        border-color: #2980b9 !important;
    }
    
    /* 聊天消息气泡样式 */
    .stChatMessage {
        padding: 1rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
    }
    
    /* 通用按钮样式 */
    .stButton > button {
        width: 100%;
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* 输入框样式 */
    .stTextInput > div > div > input {
        border-radius: 0.5rem;
    }
    
    /* 提示消息样式（成功/警告/错误） */
    .stSuccess, .stWarning, .stError {
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid;
    }
    .stSuccess {
        background-color: #d4edda;
        border-color: #28a745;
    }
    .stWarning {
        background-color: #fff3cd;
        border-color: #ffc107;
    }
    .stError {
        background-color: #f8d7da;
        border-color: #dc3545;
    }
    
    /* 信息框样式 */
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* 图片卡片核心样式（确保图片在卡片内） */
    .image-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        border: 2px solid #e9ecef;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .image-card p {
        color: #6c757d;
        font-size: 0.9rem;
        margin: 0 0 1rem 0;
    }
    .image-card img {
        max-width: 300px;  /* 统一图片宽度 */
        border-radius: 0.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# 后端地址配置
BACKEND_URL = "http://localhost:5000"

# 初始化Session State（避免重复定义）
session_keys = [
    "history", "selected_personality", "user_id", "agent_created",
    "last_personality", "show_personality_detail", "personality_detail_data",
    "conversation_round", "next_image_round"
]
for key in session_keys:
    if key not in st.session_state:
        if key == "history":
            st.session_state[key] = []
        elif key == "user_id":
            st.session_state[key] = str(uuid.uuid4())
        elif key == "next_image_round":
            st.session_state[key] = random.randint(3, 10)
        elif key == "conversation_round":
            st.session_state[key] = 0
        else:
            st.session_state[key] = ""

# 页面标题
st.markdown("""
<div style='text-align: center; padding: 2rem 0;'>
    <h1>🎭 AI人格穿越聊天</h1>
    <p style='font-size: 1.2rem; color: #6b7280; margin-top: 1rem;'>
        与历史名人对话，体验跨越时空的智慧与情感
    </p>
</div>
""", unsafe_allow_html=True)

# 侧边栏区域
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 2rem 1rem;'>
        <h2>⚙️ 设置</h2>
        <p style='font-size: 0.9rem; opacity: 0.9;'>选择你想要对话的角色</p>
    </div>
    """, unsafe_allow_html=True)

    # 获取人格列表
    @st.cache_data
    def get_personality_list():
        try:
            res = requests.get(f"{BACKEND_URL}/api/personalities")
            return res.json().get("data", [])
        except Exception as e:
            st.error(f"获取人格列表失败：{str(e)}")
            return []

    personalities = get_personality_list()
    
    # 人格选择框
    if personalities:
        st.markdown("""
        <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;'>
            <h3>🎭 选择聊天人格</h3>
        </div>
        """, unsafe_allow_html=True)
        
        def on_personality_change():
            """切换人格时重置状态"""
            st.session_state.agent_created = False
            st.session_state.history = []
            st.session_state.conversation_round = 0
            st.session_state.next_image_round = random.randint(3, 10)

        selected_persona = st.selectbox(
            label="选择人格",
            options=personalities,
            index=personalities.index(st.session_state.selected_personality) if st.session_state.selected_personality in personalities else 0,
            key="selected_personality",
            on_change=on_personality_change,
            label_visibility="collapsed"
        )

    # 创建Agent和查看详情按钮
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 创建", use_container_width=True, type="primary"):
            if st.session_state.selected_personality:
                try:
                    res = requests.post(
                        f"{BACKEND_URL}/api/createagent",
                        json={"personality_name": st.session_state.selected_personality}
                    )
                    result = res.json()
                    if result.get("code") == 200:
                        st.session_state.agent_created = True
                        st.session_state.last_personality = st.session_state.selected_personality
                        st.success("✅ Agent 创建成功！")
                    else:
                        st.error(f"❌ {result.get('msg', '创建失败')}")
                except Exception as e:
                    st.error(f"❌ 连接后端失败：{str(e)}")
            else:
                st.warning("⚠️ 请先选择人格")

    with col2:
        if st.button("📖 详情", use_container_width=True):
            if st.session_state.selected_personality:
                try:
                    res = requests.get(
                        f"{BACKEND_URL}/api/personality-detail",
                        params={"name": st.session_state.selected_personality}
                    )
                    result = res.json()
                    if result.get("code") == 200:
                        st.session_state.show_personality_detail = True
                        st.session_state.personality_detail_data = result.get("data")
                        st.success("✅ 获取成功！")
                    else:
                        st.error(f"❌ {result.get('msg', '获取详情失败')}")
                except Exception as e:
                    st.error(f"❌ 连接后端失败：{str(e)}")
            else:
                st.warning("⚠️ 请先选择人格")

    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.2);'><br>", unsafe_allow_html=True)

    # 显示人格详情
    if st.session_state.show_personality_detail and st.session_state.personality_detail_data:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
            <h3>📖 人格详情</h3>
        </div>
        """, unsafe_allow_html=True)
        
        def format_personality_detail(persona_data):
            """格式化人格详情为HTML"""
            name = persona_data.get('name', '未知人格')
            background = persona_data.get('background', '暂无背景信息')
            traits = persona_data.get('personality_traits', [])
            dialogue_style = persona_data.get('dialogue_style', '')
            
            html = [
                '<div class="sidebar-detail-content">',
                f'<h4 style="margin: 0 0 1rem 0; font-size: 1rem; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 0.5rem;">{name}</h4>',
                
                # 背景信息
                '<div style="margin-bottom: 1rem;">',
                '<h5 style="margin: 0 0 0.5rem 0; font-size: 0.9rem;">🎭 背景</h5>',
                f'<p style="margin: 0; font-size: 0.8rem; line-height: 1.3;">{background}</p>',
                '</div>',
                
                # 性格特征
                '<div style="margin-bottom: 1rem;">',
                '<h5 style="margin: 0 0 0.5rem 0; font-size: 0.9rem;">✨ 性格特征</h5>',
            ]
            
            if traits:
                html.append('<ul style="margin: 0; padding-left: 1rem; font-size: 0.8rem;">')
                for trait in traits:
                    html.append(f'<li style="margin-bottom: 0.3rem;">{trait}</li>')
                html.append('</ul>')
            else:
                html.append('<p style="margin: 0; font-size: 0.8rem; color: rgba(255,255,255,0.7);">暂无性格特征</p>')
            html.append('</div>')
            
            # 对话风格
            html.extend([
                '<div>',
                '<h5 style="margin: 0 0 0.5rem 0; font-size: 0.9rem;">💬 对话风格</h5>',
            ])
            
            if dialogue_style:
                html.append('<div style="background: rgba(255,255,255,0.05); padding: 0.8rem; border-radius: 0.3rem; border-left: 3px solid #667eea;">')
                lines = dialogue_style.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith('###'):
                        title = line.replace('###', '').strip()
                        html.append(f'<h6 style="margin: 0.8rem 0 0.5rem 0; font-size: 0.9rem; font-weight: bold;">{title}</h6>')
                    elif line.startswith(('1.', '2.', '3.', '4.', '5.')):
                        if '：' in line:
                            label, text = line.split('：', 1)
                            html.append(f'<div style="margin-bottom: 0.5rem;"><span style="font-weight: bold; font-size: 0.8rem;">{label}</span> <span style="font-size: 0.8rem;">{text}</span></div>')
                        else:
                            html.append(f'<div style="margin-bottom: 0.5rem; font-size: 0.8rem;">{line}</div>')
                    elif line.startswith('"') and line.endswith('"'):
                        html.append(f'<div style="margin: 0.5rem 0; padding: 0.5rem; background: rgba(255,255,255,0.03); border-radius: 0.3rem; font-style: italic; font-size: 0.8rem;">{line}</div>')
                    else:
                        html.append(f'<div style="margin-bottom: 0.5rem; font-size: 0.8rem;">{line}</div>')
                html.append('</div>')
            else:
                html.append('<p style="margin: 0; font-size: 0.8rem; color: rgba(255,255,255,0.7);">暂无对话风格信息</p>')
            
            html.extend(['</div>', '</div>'])
            return ''.join(html)
        
        st.markdown(
            f'<div class="sidebar-detail-container">{format_personality_detail(st.session_state.personality_detail_data)}</div>',
            unsafe_allow_html=True
        )
        
        # 关闭详情按钮
        if st.button("关闭详情", use_container_width=True, type="secondary"):
            st.session_state.show_personality_detail = False
            # 兼容Streamlit新旧版本的刷新
            try:
                st.rerun()
            except AttributeError:
                st.experimental_rerun()

    # 提示信息
    st.markdown("""
    <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;'>
        <h4>💡 提示</h4>
        <p style='font-size: 0.8rem; margin: 0.5rem 0 0 0;'>
            在3-10轮对话后，系统会自动生成人物动作图片
        </p>
    </div>
    """, unsafe_allow_html=True)

# 主聊天区域
st.markdown("<br><hr style='border-color: #e5e7eb;'><br>", unsafe_allow_html=True)

if not st.session_state.agent_created:
    # 未创建Agent时的提示
    st.markdown("""
    <div style='background: linear-gradient(135deg, #fff3cd 0%, #ffe69c 100%); padding: 2rem; border-radius: 1rem; text-align: center; border-left: 5px solid #ffc107;'>
        <h3 style='color: #856404; margin: 0 0 0.5rem 0; font-size: 1.3rem;'>⚠️ 请先创建 Agent</h3>
        <p style='color: #856404; margin: 0; font-size: 1rem;'>在左侧选择人格并点击"创建"按钮开始对话</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # 已创建Agent的聊天区域
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem 2rem; border-radius: 1rem; margin-bottom: 1.5rem;'>
        <h2 style='color: white; margin: 0; font-size: 1.5rem;'>💬 聊天窗口</h2>
        <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 0.9rem;'>
            当前对话角色：<strong>{st.session_state.selected_personality}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 显示聊天历史
    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            # 消息气泡
            bubble_style = "linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); border-radius: 1rem 1rem 1rem 0;" if msg["role"] == "user" else "linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); border-radius: 1rem 1rem 0 1rem;"
            text_color = "#1565c0" if msg["role"] == "user" else "#6a1b9a"
            
            st.markdown(f"""
            <div style='background: {bubble_style}; padding: 1rem 1.5rem; margin: 0.5rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <p style='margin: 0; color: {text_color}; font-weight: 500;'>{msg['content']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 显示图片（嵌入卡片内）
            if "image" in msg and msg["image"]:
                image_html = f"""
                <div class="image-card">
                    <p>🎨 {st.session_state.selected_personality} 的动作</p>
                    <img src="{msg['image']}" alt="{st.session_state.selected_personality}的动作" />
                </div>
                """
                st.markdown(image_html, unsafe_allow_html=True)

    # 聊天输入框
    user_input = st.chat_input("💬 输入你想聊的内容...")
    
    if user_input and st.session_state.selected_personality:
        # 添加用户消息到历史
        st.session_state.history.append({"role": "user", "content": user_input})
        
        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); padding: 1rem 1.5rem; border-radius: 1rem 1rem 1rem 0; margin: 0.5rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <p style='margin: 0; color: #1565c0; font-weight: 500;'>{user_input}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 获取AI回复
        with st.spinner("🤔 AI正在思考..."):
            try:
                res = requests.post(
                    f"{BACKEND_URL}/api/chat",
                    json={
                        "query": user_input,
                        "personality_name": st.session_state.selected_personality,
                        "user_id": st.session_state.user_id
                    }
                )
                res_data = res.json()
                
                if res_data.get("code") == 200:
                    ai_reply = res_data.get("data", "")
                    st.session_state.conversation_round += 1
                    
                    # 构建AI消息
                    ai_msg = {"role": "assistant", "content": ai_reply}
                    
                    # 检查是否生成图片
                    if st.session_state.conversation_round >= st.session_state.next_image_round:
                        with st.spinner("🎨 正在生成人物动作图片..."):
                            img_res = requests.post(
                                f"{BACKEND_URL}/api/image",
                                json={
                                    "personality_name": st.session_state.selected_personality,
                                    "query": ai_reply
                                }
                            )
                            img_data = img_res.json()
                            
                            if img_data.get("code") == 200:
                                img_url = img_data.get("data", "")
                                if isinstance(img_url, dict):
                                    img_url = img_url.get("image", "")
                                if img_url:
                                    ai_msg["image"] = img_url
                                    # 重置图片生成轮次
                                    st.session_state.next_image_round = st.session_state.conversation_round + random.randint(3, 10)
                    
                    # 添加AI消息到历史
                    st.session_state.history.append(ai_msg)
                    
                    # 显示AI回复
                    with st.chat_message("assistant"):
                        # AI消息气泡
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); padding: 1rem 1.5rem; border-radius: 1rem 1rem 0 1rem; margin: 0.5rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                            <p style='margin: 0; color: #6a1b9a; font-weight: 500;'>{ai_reply}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # 显示AI生成的图片（嵌入卡片）
                        if "image" in ai_msg and ai_msg["image"]:
                            img_html = f"""
                            <div class="image-card">
                                <p>🎨 {st.session_state.selected_personality} 的动作</p>
                                <img src="{ai_msg['image']}" alt="{st.session_state.selected_personality}的动作" />
                            </div>
                            """
                            st.markdown(img_html, unsafe_allow_html=True)
                else:
                    st.error(f"❌ AI回复失败：{res_data.get('msg', '未知错误')}")
            except Exception as e:
                st.error(f"❌ 连接后端失败：{str(e)}")