# LangGraph Agent 服务

基于 LangGraph 构建的 Agent 后端服务，集成 Google Gemini 模型，支持在 Render 平台部署。

## 🚀 功能特性

- 🤖 基于 LangGraph 0.3.28 构建的智能 Agent
- 🧠 集成 Google Gemini 1.5 Flash 模型
- ⚡ FastAPI 0.116.1 高性能 Web 服务
- 💾 内存对话历史管理
- 🔄 支持多会话管理
- 🌐 支持 Render 平台一键部署
- 🔧 现代化的异步架构

## 📋 快速开始

### 1. 环境配置

```bash
# 克隆项目
git clone <your-repo-url>
cd langgraph-server

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp env_template.txt .env
# 编辑 .env 文件，设置你的 GEMINI_API_KEY
```

### 2. 获取 Gemini API Key

1. 访问 [Google AI Studio](https://aistudio.google.com/)
2. 登录你的 Google 账户
3. 点击 "Create API Key"
4. 将 API Key 复制到 `.env` 文件中

### 3. 本地运行

```bash
# 方式1：使用快速启动脚本
python start.py

# 方式2：直接使用 uvicorn
uvicorn src.langgraph_agent.main:app --host 0.0.0.0 --port 8000

# 方式3：安装为包后运行
pip install -e .
langgraph-agent
```

### 4. 验证环境

```bash
# 检查版本兼容性
python check_versions.py

# 运行测试
python test_service.py
```

## 📡 API 接口

### 健康检查
```
GET /health
```

### 聊天接口
```
POST /chat
Content-Type: application/json

{
  "message": "你好，请介绍一下你自己",
  "session_id": "user_123"
}
```

响应：
```json
{
  "response": "你好！我是基于 LangGraph 构建的AI助手...",
  "session_id": "user_123"
}
```

## 🚀 Render 部署

### 方式一：使用 render.yaml (推荐)

1. 将代码推送到 GitHub
2. 在 Render 中创建新的 Web Service
3. 连接你的 GitHub 仓库
4. Render 会自动检测 `render.yaml` 配置
5. 在环境变量中设置 `GEMINI_API_KEY`

### 方式二：手动配置

1. 在 Render 中创建 Web Service
2. 设置构建命令：`pip install -r requirements.txt`
3. 设置启动命令：`python app.py`
4. 添加环境变量：`GEMINI_API_KEY`

## 📁 项目结构

```
langgraph-server/
├── src/                    # 源代码目录
│   └── langgraph_agent/    # 主应用包
│       ├── __init__.py     # 包初始化
│       ├── main.py         # FastAPI 主应用
│       ├── agent.py        # LangGraph Agent 实现
│       └── config.py       # 配置管理
├── tests/                  # 测试目录
│   ├── __init__.py         # 测试包初始化
│   └── test_agent.py       # Agent 测试
├── scripts/                # 工具脚本目录
│   ├── test_deployment.py  # 部署后服务测试
│   ├── check_versions.py   # 版本兼容性检查
│   └── README.md           # 工具脚本说明
├── requirements.txt        # Python 依赖
├── setup.py               # 包安装配置
├── env_template.txt       # 环境变量模板
├── render.yaml            # Render 部署配置
├── Dockerfile             # Docker 配置
├── start.py              # 快速启动脚本
├── README.md             # 项目说明
└── .gitignore            # Git 忽略文件
```

## 📚 技术栈

- **LangGraph 0.3.28**: 状态图对话管理
- **LangChain 0.3.23**: 大语言模型集成
- **FastAPI 0.116.1**: 现代化 Web 框架
- **Pydantic 2.10.4**: 数据验证
- **Google Gemini 1.5 Flash**: 高性能大语言模型
- **Uvicorn 0.34.0**: ASGI 服务器

## 🛠️ 工具脚本

项目包含了一些有用的工具脚本，位于 `scripts/` 目录：

### 服务测试
```bash
# 测试部署后的服务
pip install requests
python3 scripts/test_deployment.py [服务地址]
```

### 版本检查
```bash
# 检查依赖版本兼容性
python3 scripts/check_versions.py
```

更多详细信息请参考 [scripts/README.md](scripts/README.md)

## 💡 开发指南

### 扩展 Agent 功能

编辑 `src/langgraph_agent/agent.py` 文件，可以添加更多功能：

```python
# 添加自定义节点
def custom_node(state: AgentState):
    # 你的逻辑
    return {"messages": [...]}

# 添加到工作流
workflow.add_node("custom", custom_node)
```

### 修改模型参数

在 `src/langgraph_agent/config.py` 中调整配置：

```python
# 修改默认配置
DEFAULT_MODEL = "gemini-1.5-pro"  # 或 gemini-1.5-flash
DEFAULT_TEMPERATURE = 0.8         # 调整创造性
DEFAULT_MAX_TOKENS = 2048         # 最大输出长度
```

### 开发环境设置

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/

# 代码格式化
black src/ tests/
isort src/ tests/

# 类型检查
mypy src/
```

## 🔧 故障排除

### 常见问题

1. **Import Error**: 确保所有依赖已正确安装
   ```bash
   pip install -r requirements.txt
   python check_versions.py  # 检查版本兼容性
   ```

2. **API Key Error**: 检查 `GEMINI_API_KEY` 是否正确设置
   ```bash
   # 确认环境变量设置
   python -c "import os; print(os.getenv('GEMINI_API_KEY'))"
   ```

3. **Port Error**: 确保端口 8000 未被占用
   ```bash
   # 检查端口占用
   lsof -i :8000
   ```

4. **Version Conflicts**: 使用指定版本安装依赖
   ```bash
   pip install -r requirements.txt --force-reinstall
   python check_versions.py  # 验证版本
   ```

### 日志查看

```bash
# 查看应用日志
tail -f app.log

# 或在 Render 中查看日志
```

## 🔄 版本更新说明

### v1.0.0 (最新)

#### 📦 依赖升级
- **FastAPI**: 0.104.1 → 0.116.1
- **Uvicorn**: 0.24.0 → 0.34.0
- **LangGraph**: 0.0.62 → 0.3.28
- **LangChain**: 0.1.20 → 0.3.23
- **Pydantic**: 2.5.0 → 2.10.4
- **Google GenerativeAI**: 0.3.2 → 0.8.5
- **LangChain Google GenAI**: 1.0.8 → 2.0.11

#### 🔧 代码改进
- 使用现代化的 `lifespan` 上下文管理器替代 `@app.on_event`
- 改进的消息处理，支持 LangChain 核心消息类型
- 更新的 LangGraph API 调用 (START, END 节点)
- 更好的错误处理和日志记录
- 添加版本兼容性检查脚本

#### 🆕 新功能
- 版本兼容性检查脚本 (`check_versions.py`)
- 更详细的故障排除文档
- 改进的项目结构和文档

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## �� 许可证

MIT License 