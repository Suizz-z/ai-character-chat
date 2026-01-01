# 多人格智能对话系统

一个基于AI的多人格穿越聊天应用，让您可以与历史名人、文学角色等进行沉浸式对话，系统会自动生成人物动作图片，提供更加生动的交互体验。

## 项目简介

随缘占卜AI是一个创新的AI对话系统，通过大语言模型和图像生成技术，让用户能够与不同的人格角色进行自然对话。系统内置了多个经典历史人物和文学角色，每个角色都有独特的性格、背景和对话风格。

### 核心特性

- 多人格对话：支持李白、林黛玉、甄嬛、李逵等多个经典角色
- 智能对话：基于大语言模型，角色回复符合其性格特点和历史背景
- 自动生图：在3-10轮对话后，自动根据AI回复内容生成人物动作图片
- 知识库检索：使用向量数据库存储和检索人格信息
- 实时交互：Streamlit提供流畅的Web界面
- 易于扩展：支持添加新的人格角色

## 功能特性

### 对话功能
- 选择不同的人格角色进行对话
- 角色回复完全符合其历史背景和性格特点
- 支持多轮对话，保持对话上下文
- 自动追踪对话轮次

### 图片生成
- 在3-10轮对话后自动触发图片生成
- 根据AI回复内容智能生成人物动作描述
- 图片显示在AI消息之后，增强沉浸感
- 支持多种艺术风格（水墨、写实、3D卡通等）

### 人格管理
- 查看人格详细信息（背景、性格、对话风格）
- 动态切换人格角色
- 支持自定义人格配置

## 技术栈

### 前端
- **Streamlit**: Web应用框架
- **Requests**: HTTP客户端

### 后端
- **Flask**: Web框架
- **Flask-CORS**: 跨域支持
- **LangChain**: AI应用框架
- **ChromaDB**: 向量数据库

### AI服务
- **DashScope (通义千问)**: 大语言模型和图像生成
- **OpenAI**: 兼容API接口

### 其他
- **Python-dotenv**: 环境变量管理
- **LangChain Agents**: Agent框架

## 项目结构

```
suiyuan-divination-ai/
├── backend/                    # 后端服务
│   ├── config/                # 配置文件
│   │   └── personalities.json # 人格配置
│   ├── knowledge_base/        # 知识库
│   │   └── init_chroma.py    # 向量数据库初始化
│   ├── src/                   # 源代码
│   │   ├── agent/            # Agent模块
│   │   │   ├── chat_agent.py # 聊天Agent
│   │   │   ├── image_agent.py # 图片生成Agent
│   │   │   └── tools/       # 工具函数
│   │   └── model.py         # 模型配置
│   ├── utils/                # 工具函数
│   │   └── kb_utils.py      # 知识库工具
│   └── app.py               # Flask应用入口
├── frontend/                 # 前端应用
│   └── app.py               # Streamlit应用
├── .env                     # 环境变量
├── .gitignore              # Git忽略文件
└── README.md               # 项目文档
```

## 安装和配置

### 环境要求

- Python 3.8+
- pip

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/suiyuan-divination-ai.git
cd suiyuan-divination-ai
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

如果需要手动安装，主要依赖包括：

```bash
pip install streamlit flask flask-cors langchain chromadb dashscope python-dotenv requests
```

### 4. 配置环境变量

创建 `.env` 文件，配置以下环境变量：

```env
# DashScope API密钥
DASHSCOPE_API_KEY=your_dashscope_api_key_here

# 可选：OpenAI API密钥
OPENAI_API_KEY=your_openai_api_key_here

# 后端服务地址（前端使用）
BACKEND_URL=http://localhost:5000
```

### 5. 初始化知识库

```bash
cd backend
python knowledge_base/init_chroma.py
```

## 使用方法

### 启动后端服务

```bash
cd backend
python app.py
```

后端服务将在 `http://localhost:5000` 启动。

### 启动前端服务

打开新的终端窗口：

```bash
cd frontend
streamlit run app.py
```

前端应用将在浏览器中自动打开，默认地址为 `http://localhost:8501`。

### 使用流程

1. **选择人格角色**：在左侧边栏选择想要对话的角色（如李白、林黛玉等）
2. **创建Agent**：点击"创建 Agent"按钮初始化对话系统
3. **开始对话**：在聊天窗口输入消息，与角色进行对话
4. **查看人格详情**：点击"查看人格详情"了解角色的背景和性格特点
5. **自动生图**：在3-10轮对话后，系统会自动生成人物动作图片

## API文档

### 获取人格列表

**请求**
```
GET /api/personalities
```

**响应**
```json
{
  "code": 200,
  "data": ["李白", "林黛玉", "甄嬛", "李逵"]
}
```

### 创建Agent

**请求**
```
POST /api/createagent
Content-Type: application/json

{
  "personality_name": "李白"
}
```

**响应**
```json
{
  "code": 200,
  "msg": "success"
}
```

### 发送聊天消息

**请求**
```
POST /api/chat
Content-Type: application/json

{
  "query": "你好，李白",
  "personality_name": "李白",
  "user_id": "user123"
}
```

**响应**
```json
{
  "code": 200,
  "data": "快哉快哉！且饮一杯！"
}
```

### 生成图片

**请求**
```
POST /api/image
Content-Type: application/json

{
  "personality_name": "李白",
  "query": "正在举杯邀明月"
}
```

**响应**
```json
{
  "code": 200,
  "data": "base64_encoded_image_data"
}
```

### 获取人格详情

**请求**
```
POST /api/personality/detail
Content-Type: application/json

{
  "personality_name": "李白"
}
```

**响应**
```json
{
  "code": 200,
  "data": {
    "name": "李白（字太白，号青莲居士）",
    "background": "唐代浪漫主义诗人...",
    "personality_traits": ["豪放洒脱", "自信狂傲", "浪漫感性", "重情重义"],
    "dialogue_style": "### 语气细节：\n1. 说话自带酒气...",
    "prompt_template": "你现在是唐代诗仙李白..."
  }
}
```

## 人格配置

### 添加新人格

在 `backend/config/personalities.json` 中添加新的人格配置：

```json
{
  "name": "角色名称",
  "background": "角色背景介绍",
  "personality_traits": ["性格特征1", "性格特征2"],
  "dialogue_style": "### 语气细节：\n1. 语气描述\n2. 说话习惯\n### 核心口头禅：\n"口头禅1", "口头禅2"",
  "prompt_template": "你现在是[角色名]，必须完全模仿他的人格与语言风格：\n1. 背景：{background}\n2. 性格：{personality_traits}\n3. 说话风格：{dialogue_style}\n4. 强制规则：\n- 规则1\n- 规则2"
}
```

### 人格配置说明

- **name**: 角色的完整名称和称号
- **background**: 角色的历史背景和生平介绍
- **personality_traits**: 角色的性格特征列表
- **dialogue_style**: 详细的对话风格描述，包括语气、说话习惯、口头禅等
- **prompt_template**: AI角色的提示词模板，使用 `{background}`、`{personality_traits}`、`{dialogue_style}` 作为占位符

### 内置人格

项目内置了以下经典角色：

1. **李白（诗仙）**：豪放洒脱，浪漫感性，喜欢饮酒作诗
2. **林黛玉（红楼梦）**：敏感细腻，多愁善感，才情过人
3. **甄嬛（甄嬛传）**：聪慧隐忍，冷静果决，洞察人心
4. **李逵（水浒传）**：鲁莽直率，忠诚勇猛，嫉恶如仇

## 常见问题

### Q: 如何更换API密钥？

A: 编辑 `.env` 文件，修改 `DASHSCOPE_API_KEY` 的值，然后重启后端服务。

### Q: 图片生成失败怎么办？

A: 检查以下几点：
1. 确认DashScope API密钥正确
2. 确认网络连接正常
3. 检查API配额是否充足
4. 查看后端日志获取详细错误信息

### Q: 如何添加新的人格角色？

A: 按照"人格配置"章节的说明，在 `backend/config/personalities.json` 中添加新的人格配置，然后重新初始化知识库。

### Q: 对话轮次如何计算？

A: 每次用户发送消息并收到AI回复算作一轮对话。系统会在3-10轮之间随机选择一个轮次触发图片生成。

### Q: 可以自定义图片生成风格吗？

A: 可以。修改 `backend/src/agent/image_agent.py` 中的 `create_image_prompt()` 函数，调整提示词词典和风格参数。

## 开发指南

### 添加新功能

1. 后端功能：在 `backend/app.py` 中添加新的API端点
2. 前端功能：在 `frontend/app.py` 中添加新的UI组件
3. Agent功能：在 `backend/src/agent/` 中创建新的Agent模块

### 测试

```bash
# 运行后端测试
cd backend
python -m pytest

# 运行前端测试
cd frontend
streamlit run app.py
```

### 调试

- 后端日志：查看终端输出
- 前端日志：查看Streamlit控制台
- 知识库：检查 `backend/knowledge_base/chroma_db/` 目录

## 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 致谢

- DashScope (通义千问) 提供的大语言模型和图像生成服务
- LangChain 提供的AI应用框架
- Streamlit 提供的Web应用框架
- ChromaDB 提供的向量数据库

## 联系方式

- 邮箱：1344278076@qq.com

---

**随缘占卜AI** - 让历史人物与您对话，体验跨越时空的智慧与情感！
