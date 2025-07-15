# LangGraph Agent 服务

基于 LangGraph 构建的 Agent 后端服务，集成 Google Gemini 模型，支持在 Render 平台部署。

## 功能特性

- 🤖 基于 LangGraph 构建的智能 Agent
- 🧠 集成 Google Gemini 1.5 Flash 模型
- 🚀 FastAPI 高性能 Web 服务
- 💾 内存对话历史管理
- 🔄 支持多会话管理
- 🌐 支持 Render 平台一键部署

## 快速开始

### 1. 环境配置

```bash
# 克隆项目
git clone <your-repo-url>
cd langgraph-server

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置你的 GEMINI_API_KEY
```

### 2. 获取 Gemini API Key

1. 访问 [Google AI Studio](https://aistudio.google.com/)
2. 创建新的 API Key
3. 将 API Key 复制到 `.env` 文件中

### 3. 本地运行

```bash
# 启动服务
python app.py

# 或使用 uvicorn
uvicorn app:app --host 0.0.0.0 --port 8000
```

### 4. 测试服务

```bash
# 运行测试
python test_service.py
```

## API 接口

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

## Render 部署

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

## 项目结构

```
langgraph-server/
├── app.py              # FastAPI 主应用
├── agent.py            # LangGraph Agent 实现
├── requirements.txt    # Python 依赖
├── .env.example       # 环境变量示例
├── render.yaml        # Render 部署配置
├── Dockerfile         # Docker 配置
├── test_service.py    # 测试脚本
└── README.md          # 项目说明
```

## 开发指南

### 扩展 Agent 功能

编辑 `agent.py` 文件，可以添加更多功能：

```python
# 添加工具
from langgraph.prebuilt import ToolExecutor

# 添加自定义节点
def custom_node(state: AgentState):
    # 你的逻辑
    return {"messages": [...]}

# 添加到工作流
workflow.add_node("custom", custom_node)
```

### 修改模型参数

在 `agent.py` 中调整模型配置：

```python
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # 或 gemini-1.5-pro
    temperature=0.7,           # 调整创造性
    max_output_tokens=1024,    # 最大输出长度
)
```

## 故障排除

### 常见问题

1. **Import Error**: 确保所有依赖已正确安装
2. **API Key Error**: 检查 `GEMINI_API_KEY` 是否正确设置
3. **Port Error**: 确保端口 8000 未被占用

### 日志查看

```bash
# 查看应用日志
tail -f app.log

# 或在 Render 中查看日志
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License 