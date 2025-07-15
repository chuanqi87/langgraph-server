"""
LangGraph Agent 包

基于 LangGraph 和 Google Gemini 模型的智能 Agent 服务。
"""

from .agent import LangGraphAgent, create_agent
from .config import (
    AgentConfig,
    ServerConfig,
    AppConfig,
    get_agent_config,
    get_server_config,
    get_app_config
)
from .main import app, run_server

__version__ = "1.0.0"
__author__ = "LangGraph Agent Team"
__email__ = "contact@langgraph-agent.com"

__all__ = [
    "LangGraphAgent",
    "create_agent",
    "AgentConfig",
    "ServerConfig", 
    "AppConfig",
    "get_agent_config",
    "get_server_config",
    "get_app_config",
    "app",
    "run_server"
] 