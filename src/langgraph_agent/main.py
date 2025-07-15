"""
LangGraph Agent 服务

基于 FastAPI 和 LangGraph 构建的智能 Agent 服务，集成 Google Gemini 模型。
提供 RESTful API 接口用于与 AI Agent 进行对话交互。
"""

import logging
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from .agent import create_agent
from .config import (
    get_app_config, 
    get_server_config,
    DEFAULT_SESSION_ID,
    INPUT_MAX_LENGTH,
    INPUT_MIN_LENGTH,
    SESSION_ID_MAX_LENGTH,
    SESSION_ID_MIN_LENGTH,
    LOG_FORMAT
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT
)
logger = logging.getLogger(__name__)

# 全局变量存储 agent
agent = None


class ChatRequest(BaseModel):
    """聊天请求模型"""
    
    message: str = Field(
        ...,
        description="用户输入的消息",
        min_length=INPUT_MIN_LENGTH,
        max_length=INPUT_MAX_LENGTH,
        example="你好，请介绍一下你自己"
    )
    session_id: str = Field(
        default=DEFAULT_SESSION_ID,
        description="会话ID，用于维护对话上下文",
        min_length=SESSION_ID_MIN_LENGTH,
        max_length=SESSION_ID_MAX_LENGTH,
        example="user_123"
    )


class ChatResponse(BaseModel):
    """聊天响应模型"""
    
    response: str = Field(
        ...,
        description="AI助手的回复",
        example="你好！我是基于LangGraph构建的AI助手，很高兴为您服务！"
    )
    session_id: str = Field(
        ...,
        description="会话ID",
        example="user_123"
    )


class HealthResponse(BaseModel):
    """健康检查响应模型"""
    
    status: str = Field(
        ...,
        description="服务状态",
        example="healthy"
    )
    agent_ready: bool = Field(
        ...,
        description="Agent是否已准备就绪",
        example=True
    )


class StatusResponse(BaseModel):
    """状态响应模型"""
    
    message: str = Field(
        ...,
        description="状态消息",
        example="LangGraph Agent Service is running"
    )
    status: str = Field(
        ...,
        description="服务状态",
        example="healthy"
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    
    在应用启动时初始化 Agent，在关闭时清理资源。
    """
    global agent
    
    # 启动时初始化
    try:
        logger.info("开始初始化 Agent...")
        agent = create_agent()
        logger.info("Agent 初始化成功")
    except Exception as e:
        logger.error(f"Agent 初始化失败: {e}")
        raise
    
    yield
    
    # 关闭时清理资源
    logger.info("应用关闭，清理资源...")
    agent = None


# 获取应用配置
app_config = get_app_config()

# 创建 FastAPI 应用
app = FastAPI(
    title=app_config.title,
    description=app_config.description,
    version=app_config.version,
    lifespan=lifespan,
    docs_url=app_config.docs_url,
    redoc_url=app_config.redoc_url
)


@app.get("/", response_model=StatusResponse)
async def root() -> StatusResponse:
    """
    根路径 - 服务状态检查
    
    Returns:
        StatusResponse: 包含服务状态的响应
    """
    return StatusResponse(
        message="LangGraph Agent Service is running",
        status="healthy"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    健康检查接口
    
    检查服务是否正常运行以及 Agent 是否已准备就绪。
    
    Returns:
        HealthResponse: 包含服务健康状态的响应
    """
    return HealthResponse(
        status="healthy",
        agent_ready=agent is not None
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    聊天接口
    
    与 AI Agent 进行对话交互。支持多轮对话，通过 session_id 维护对话上下文。
    
    Args:
        request: 聊天请求，包含用户消息和会话ID
        
    Returns:
        ChatResponse: 包含 AI 回复的响应
        
    Raises:
        HTTPException: 当 Agent 未初始化或处理请求失败时
    """
    if not agent:
        logger.error("Agent 未初始化")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Agent 服务暂时不可用，请稍后重试"
        )
    
    try:
        logger.info(f"处理聊天请求 - 会话ID: {request.session_id}")
        
        # 调用 agent 处理消息
        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": request.message}]},
            config={"configurable": {"thread_id": request.session_id}}
        )
        
        # 提取最后一条消息作为回复
        if not response.get("messages"):
            logger.error("Agent 响应为空")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Agent 响应为空，请重试"
            )
        
        last_message = response["messages"][-1]
        if not isinstance(last_message, dict) or "content" not in last_message:
            logger.error(f"Agent 响应格式错误: {last_message}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Agent 响应格式错误，请重试"
            )
        
        reply_content = last_message["content"]
        logger.info(f"成功处理聊天请求 - 会话ID: {request.session_id}")
        
        return ChatResponse(
            response=reply_content,
            session_id=request.session_id
        )
        
    except HTTPException:
        # 重新抛出 HTTPException
        raise
    except Exception as e:
        logger.error(f"处理聊天请求时发生错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"处理请求时发生错误: {str(e)}"
        )


def run_server() -> None:
    """
    运行服务器
    
    从环境变量获取端口配置，启动 FastAPI 服务器。
    """
    import uvicorn
    
    server_config = get_server_config()
    logger.info(f"启动服务器，监听端口: {server_config.port}")
    
    uvicorn.run(
        "src.langgraph_agent.main:app",
        host=server_config.host,
        port=server_config.port,
        reload=server_config.reload,
        log_level=server_config.log_level.lower()
    )


if __name__ == "__main__":
    run_server() 