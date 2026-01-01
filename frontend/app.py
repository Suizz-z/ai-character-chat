import streamlit as st
import requests
import json
import uuid
import random

st.set_page_config(
    page_title="AI人格穿越聊天 - 多人格智能对话",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* 全局样式 */
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
    
    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    /* 侧边栏详情样式 */
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
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* 侧边栏标题 */
    [data-testid="stSidebar"] h2 {
        color: #ffffff !important;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] h4 {
        color: #ffffff !important;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] p {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* 侧边栏Selectbox 终极修复：强制覆盖所有内部元素 */
    [data-testid="stSidebar"] .stSelectbox {
        margin: 1rem 0;
    }
    
    /* 1. Selectbox最外层容器 */
    [data-testid="stSidebar"] .stSelectbox > div:first-child {
        background-color: #1a252f !important; /* 强制深色背景 */
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 0.75rem;
        padding: 0.5rem;
        transition: all 0.3s ease;
    }
    
    /* 2. Selectbox内部所有子容器（覆盖输入区域） */
    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"],
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1a252f !important; /* 强制深色背景，消除白色区域 */
        color: #ffffff !important; /* 强制白色文字 */
        width: 100%;
    }
    
    /* 3. Selectbox输入框文字（直接命中input元素） */
    [data-testid="stSidebar"] .stSelectbox input,
    [data-testid="stSidebar"] .stSelectbox span {
        background-color: transparent !important;
        color: #ffffff !important; /* 强制白色文字 */
        font-weight: 600;
        font-size: 1rem;
    }
    
    /* 4. Selectbox下拉箭头 */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] svg {
        fill: #ffffff !important;
    }
    
    /* 5. 下拉选项列表 */
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
    
    /* 侧边栏按钮 */
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
    
    /* 聊天消息样式 */
    .stChatMessage {
        padding: 1rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
    }
    
    /* 按钮样式 */
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
    
    /* 成功消息 */
    .stSuccess {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    
    /* 警告消息 */
    .stWarning {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    
    /* 错误消息 */
    .stError {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 0.5rem;
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
    
    /* 卡片样式 */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    /* 图片容器 */
    .image-container {
        text-align: center;
        margin: 1rem 0;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 1rem;
    }
</style>
""", unsafe_allow_html=True)

user_id = str(uuid.uuid4())

BACKEND_URL = "http://localhost:5000"

# 初始化session state
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


st.markdown("""
<div style='text-align: center; padding: 2rem 0;'>
    <h1 style='font-size: 3rem; font-weight: 700; color: #1f2937; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);'>
        🎭 AI人格穿越聊天
    </h1>
    <p style='font-size: 1.2rem; color: #6b7280; margin-top: 1rem;'>
        与历史名人对话，体验跨越时空的智慧与情感
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style='text-align: center; padding: 2rem 1rem;'>
    <h2 style='font-size: 1.8rem; font-weight: 600; margin-bottom: 0.5rem;'>
        ⚙️ 设置
    </h2>
    <p style='font-size: 0.9rem; opacity: 0.9;'>
        选择你想要对话的角色
    </p>
</div>
""", unsafe_allow_html=True)

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
    """修复HTML格式，确保正确渲染"""
    # 基础信息提取
    name = personality.get('name', '未知人格')
    background = personality.get('background', '暂无背景信息')
    traits = personality.get('personality_traits', [])
    dialogue_style = personality.get('dialogue_style', '')
    
    # 构建完整的HTML结构
    html_parts = [
        '<div class="sidebar-detail-content">',
        f'<h4 style="color: #ffffff; margin: 0 0 1rem 0; font-size: 1rem; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 0.5rem;">📖 {name}</h4>',
        
        # 背景部分
        '<div style="margin-bottom: 1rem;">',
        '<h5 style="color: #bbdefb; margin: 0 0 0.5rem 0; font-size: 0.9rem;">🎭 背景</h5>',
        f'<p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.8rem; line-height: 1.3;">{background}</p>',
        '</div>',
        
        # 性格特征部分
        '<div style="margin-bottom: 1rem;">',
        '<h5 style="color: #bbdefb; margin: 0 0 0.5rem 0; font-size: 0.9rem;">✨ 性格特征</h5>',
    ]
    
    # 处理性格特征
    if traits:
        html_parts.append('<ul style="color: rgba(255,255,255,0.9); margin: 0; padding-left: 1rem; font-size: 0.8rem;">')
        for trait in traits:
            html_parts.append(f'<li style="margin-bottom: 0.3rem;">{trait}</li>')
        html_parts.append('</ul>')
    else:
        html_parts.append('<p style="color: rgba(255,255,255,0.7); margin: 0; font-size: 0.8rem;">暂无性格特征</p>')
    
    html_parts.append('</div>')
    
    # 对话风格部分
    html_parts.extend([
        '<div>',
        '<h5 style="color: #bbdefb; margin: 0 0 0.5rem 0; font-size: 0.9rem;">💬 对话风格</h5>',
    ])
    
    if dialogue_style:
        # 处理对话风格，使其更美观地显示
        html_parts.append('<div style="background: rgba(255,255,255,0.05); padding: 0.8rem; border-radius: 0.3rem; border-left: 3px solid #667eea;">')
        
        # 解析 Markdown 格式的内容并转换为美观的 HTML
        lines = dialogue_style.split('\n')
        current_section = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 处理标题行（### 开头）
            if line.startswith('###'):
                title_text = line.replace('###', '').strip()
                html_parts.append(f'<h6 style="color: #e1f5fe; margin: 0.8rem 0 0.5rem 0; font-size: 0.9rem; font-weight: bold;">{title_text}</h6>')
                
            # 处理子标题行（1. 2. 3. 开头）
            elif line.startswith(('1.', '2.', '3.', '4.', '5.')):
                # 清理内容中的特殊字符并加粗关键词
                content = line
                if '：' in content:
                    parts = content.split('：', 1)
                    if len(parts) == 2:
                        label, text = parts
                        text = text.strip()
                        html_parts.append(f'<div style="margin-bottom: 0.5rem;"><span style="color: #bbdefb; font-weight: bold; font-size: 0.8rem;">{label}</span><span style="color: rgba(255,255,255,0.9); font-size: 0.8rem;">{text}</span></div>')
                    else:
                        html_parts.append(f'<div style="margin-bottom: 0.5rem; color: rgba(255,255,255,0.9); font-size: 0.8rem;">{content}</div>')
                else:
                    html_parts.append(f'<div style="margin-bottom: 0.5rem; color: rgba(255,255,255,0.9); font-size: 0.8rem;">{content}</div>')
                    
            # 处理普通文本
            else:
                # 处理引用或特殊格式
                if line.startswith('"') and line.endswith('"'):
                    html_parts.append(f'<div style="margin: 0.5rem 0; padding: 0.5rem; background: rgba(255,255,255,0.03); border-radius: 0.3rem; font-style: italic; color: rgba(255,255,255,0.8); font-size: 0.8rem;">{line}</div>')
                else:
                    html_parts.append(f'<div style="margin-bottom: 0.5rem; color: rgba(255,255,255,0.9); font-size: 0.8rem;">{line}</div>')
        
        html_parts.append('</div>')
    else:
        html_parts.append('<p style="color: rgba(255,255,255,0.7); margin: 0; font-size: 0.8rem;">暂无对话风格信息</p>')
    
    html_parts.append('</div>')
    html_parts.append('</div>')
    
    # 拼接并返回完整HTML
    return ''.join(html_parts)

def on_personality_change():
    if st.session_state.last_personality != "" and st.session_state.last_personality != st.session_state.selected_personality:
        st.session_state.agent_created = False
        st.session_state.history = []
        st.session_state.conversation_round = 0
        st.session_state.next_image_round = random.randint(3, 10)

# 获取人格列表
personalities = get_personality_list()
if personalities:
    st.sidebar.markdown("""
    <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;'>
        <h3 style='color: white; font-size: 1rem; margin-bottom: 0.5rem;'>🎭 选择聊天人格</h3>
    </div>
    """, unsafe_allow_html=True)
    
    selected = st.sidebar.selectbox(
        "选择人格",
        personalities,
        index=0 if st.session_state.selected_personality == "" else personalities.index(st.session_state.selected_personality),
        key="selected_personality",
        on_change=on_personality_change,
        label_visibility="collapsed"
    )

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# 创建和详情按钮
col1, col2 = st.sidebar.columns(2)
with col1:
    create_btn = st.button("🚀 创建", use_container_width=True, type="primary")
with col2:
    detail_btn = st.button("📖 详情", use_container_width=True)

if create_btn:
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

if detail_btn:
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

st.sidebar.markdown("<br><hr style='border-color: rgba(255,255,255,0.2);'><br>", unsafe_allow_html=True)

# 显示人格详情
if st.session_state.show_personality_detail and st.session_state.personality_detail_data:
    
    st.sidebar.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
        <h3 style='color: white; margin: 0; font-size: 1.1rem;'>📖 人格详情</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 使用容器包裹详情内容，确保样式正确
    st.sidebar.markdown(
        f'<div class="sidebar-detail-container">{format_personality_detail(st.session_state.personality_detail_data)}</div>',
        unsafe_allow_html=True
    )
    
    # 操作按钮
    col1, = st.sidebar.columns(1)
    with col1:
        if st.button("关闭详情", use_container_width=True, type="secondary"):
            st.session_state.show_personality_detail = False
            st.rerun()
    
    st.sidebar.markdown("<br>", unsafe_allow_html=True)

# 提示信息
st.sidebar.markdown("""
<div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;'>
    <h4 style='color: white; font-size: 0.9rem; margin: 0;'>💡 提示</h4>
    <p style='color: rgba(255,255,255,0.8); font-size: 0.8rem; margin: 0.5rem 0 0 0;'>
        在3-10轮对话后，系统会自动生成人物动作图片
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><hr style='border-color: #e5e7eb;'><br>", unsafe_allow_html=True)

# 主聊天区域
if not st.session_state.agent_created:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #fff3cd 0%, #ffe69c 100%); padding: 2rem; border-radius: 1rem; text-align: center; border-left: 5px solid #ffc107;'>
        <h3 style='color: #856404; margin: 0 0 0.5rem 0; font-size: 1.3rem;'>⚠️ 请先创建 Agent</h3>
        <p style='color: #856404; margin: 0; font-size: 1rem;'>在左侧选择人格并点击"创建"按钮开始对话</p>
    </div>
    """, unsafe_allow_html=True)
else:
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
            if msg["role"] == "user":
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); padding: 1rem 1.5rem; border-radius: 1rem 1rem 1rem 0; margin: 0.5rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    <p style='margin: 0; color: #1565c0; font-weight: 500;'>{msg['content']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); padding: 1rem 1.5rem; border-radius: 1rem 1rem 0 1rem; margin: 0.5rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    <p style='margin: 0; color: #6a1b9a; font-weight: 500;'>{msg['content']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # 显示图片（如果有）
            if "image" in msg and msg["image"]:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 1rem; text-align: center; border: 2px solid #e9ecef;'>
                    <p style='color: #6c757d; margin: 0 0 1rem 0; font-size: 0.9rem;'>🎨 {st.session_state.selected_personality} 的动作</p>
                </div>
                """, unsafe_allow_html=True)
                st.image(msg["image"], caption=f"{st.session_state.selected_personality}的动作", width="auto")
                st.markdown("<br>", unsafe_allow_html=True)

    # 聊天输入框
    user_input = st.chat_input("💬 输入你想聊的内容...")

    if user_input and st.session_state.selected_personality:
        # 添加用户消息到历史
        st.session_state.history.append({"role": "user", "content": user_input})
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
                if res.json()["code"] == 200:
                    reply = res.json()["data"]
                    st.session_state.conversation_round += 1
                    
                    msg_data = {"role": "assistant", "content": reply}
                    
                    # 检查是否需要生成图片
                    if st.session_state.conversation_round >= st.session_state.next_image_round:
                        with st.spinner("🎨 正在生成人物动作图片..."):
                            image_result = generate_image(st.session_state.selected_personality, reply)
                            
                            if image_result["code"] == 200:
                                image_data = image_result["data"]
                                if isinstance(image_data, dict) and "image" in image_data:
                                    msg_data["image"] = image_data["image"]
                                elif isinstance(image_data, str):
                                    msg_data["image"] = image_data
                                
                                # 更新下一次生成图片的轮数
                                st.session_state.next_image_round = st.session_state.conversation_round + random.randint(3, 10)
                    
                    # 添加AI回复到历史
                    st.session_state.history.append(msg_data)
                    
                    # 显示AI回复
                    with st.chat_message("assistant"):
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); padding: 1rem 1.5rem; border-radius: 1rem 1rem 0 1rem; margin: 0.5rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                            <p style='margin: 0; color: #6a1b9a; font-weight: 500;'>{reply}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # 显示图片（如果有）
                        if "image" in msg_data and msg_data["image"]:
                            st.markdown("<br>", unsafe_allow_html=True)
                            st.markdown(f"""
                            <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 1rem; text-align: center; border: 2px solid #e9ecef;'>
                                <p style='color: #6c757d; margin: 0 0 1rem 0; font-size: 0.9rem;'>🎨 {st.session_state.selected_personality} 的动作</p>
                            </div>
                            """, unsafe_allow_html=True)
                            st.image(msg_data["image"], caption=f"{st.session_state.selected_personality}的动作", width="auto")
                            st.markdown("<br>", unsafe_allow_html=True)
                else:
                    # 显示错误信息
                    st.markdown(f"""
                    <div style='background: #f8d7da; padding: 1rem 1.5rem; border-radius: 0.5rem; border-left: 4px solid #dc3545; margin: 1rem 0;'>
                        <p style='margin: 0; color: #721c24; font-weight: 500;'>❌ {res.json()['msg']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                # 显示异常信息
                st.markdown(f"""
                <div style='background: #f8d7da; padding: 1rem 1.5rem; border-radius: 0.5rem; border-left: 4px solid #dc3545; margin: 1rem 0;'>
                    <p style='margin: 0; color: #721c24; font-weight: 500;'>❌ 聊天失败：{e}</p>
                </div>
                """, unsafe_allow_html=True)