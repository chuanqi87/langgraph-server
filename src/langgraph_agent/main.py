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
    LOG_FORMAT
)
from copilotkit import CopilotKitRemoteEndpoint, add_fastapi_endpoint
from copilotkit.agents import LangGraphAgent

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT
)
logger = logging.getLogger(__name__)

# 全局变量存储 agent
agent = None

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

sdk = CopilotKitRemoteEndpoint(
    agents=[
        LangGraphAgent(
            name="langgraph_agent",
            description="A LangGraph agent to use as a starting point for your own agent.",
            graph=agent,
        )
    ],
)

add_fastapi_endpoint(app, sdk, "/copilotkit")


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