"""
配置管理模块

集中管理应用的所有配置项，包括环境变量、常量和默认值。
"""

import os
from typing import Optional
from dataclasses import dataclass
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 环境变量名称
ENV_GEMINI_API_KEY = "GEMINI_API_KEY"
ENV_PORT = "PORT"

# 默认值
DEFAULT_PORT = 8000
DEFAULT_HOST = "0.0.0.0"
DEFAULT_MODEL = "gemini-1.5-flash"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 4096
DEFAULT_SESSION_ID = "default"

# 应用信息
APP_NAME = "langgraph-agent"
APP_TITLE = "LangGraph Agent Service"
APP_DESCRIPTION = "基于 LangGraph 构建的智能 Agent 服务，集成 Google Gemini 模型"
APP_VERSION = "1.0.0"

# API 配置
API_DOCS_URL = "/docs"
API_REDOC_URL = "/redoc"

# 日志配置
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 系统提示词
SYSTEM_PROMPT = """你是一个有用的AI助手，基于 LangGraph 构建。
请用中文回复用户的问题，保持友好和专业的态度。
如果遇到不确定的问题，请诚实说明并提供可能的建议。"""

# 外部服务URL
GEMINI_API_STUDIO_URL = "https://aistudio.google.com/"

# 验证配置
INPUT_MAX_LENGTH = 4000
INPUT_MIN_LENGTH = 1
SESSION_ID_MAX_LENGTH = 100
SESSION_ID_MIN_LENGTH = 1

# 超时配置
REQUEST_TIMEOUT = 30
LLM_TIMEOUT = 60


@dataclass
class ServerConfig:
    """服务器配置"""
    
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    reload: bool = False
    log_level: str = LOG_LEVEL
    
    @classmethod
    def from_env(cls) -> "ServerConfig":
        """从环境变量创建配置"""
        return cls(
            host=os.getenv("HOST", DEFAULT_HOST),
            port=int(os.getenv(ENV_PORT, DEFAULT_PORT)),
            reload=os.getenv("RELOAD", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", LOG_LEVEL)
        )


@dataclass
class AgentConfig:
    """Agent 配置"""
    
    model: str = DEFAULT_MODEL
    temperature: float = DEFAULT_TEMPERATURE
    max_tokens: int = DEFAULT_MAX_TOKENS
    system_prompt: str = SYSTEM_PROMPT
    api_key: Optional[str] = None
    
    def __post_init__(self):
        """初始化后处理"""
        if self.api_key is None:
            self.api_key = os.getenv(ENV_GEMINI_API_KEY)
            if not self.api_key:
                raise ValueError(f"未设置 {ENV_GEMINI_API_KEY} 环境变量")
    
    @classmethod
    def from_env(cls) -> "AgentConfig":
        """从环境变量创建配置"""
        return cls(
            model=os.getenv("GEMINI_MODEL", DEFAULT_MODEL),
            temperature=float(os.getenv("GEMINI_TEMPERATURE", DEFAULT_TEMPERATURE)),
            max_tokens=int(os.getenv("GEMINI_MAX_TOKENS", DEFAULT_MAX_TOKENS)),
            system_prompt=os.getenv("SYSTEM_PROMPT", SYSTEM_PROMPT),
            api_key=os.getenv(ENV_GEMINI_API_KEY)
        )


@dataclass
class AppConfig:
    """应用配置"""
    
    name: str = APP_NAME
    title: str = APP_TITLE
    description: str = APP_DESCRIPTION
    version: str = APP_VERSION
    docs_url: str = API_DOCS_URL
    redoc_url: str = API_REDOC_URL
    
    @classmethod
    def from_env(cls) -> "AppConfig":
        """从环境变量创建配置"""
        return cls(
            name=os.getenv("APP_NAME", APP_NAME),
            title=os.getenv("APP_TITLE", APP_TITLE),
            description=os.getenv("APP_DESCRIPTION", APP_DESCRIPTION),
            version=os.getenv("APP_VERSION", APP_VERSION),
            docs_url=os.getenv("API_DOCS_URL", API_DOCS_URL),
            redoc_url=os.getenv("API_REDOC_URL", API_REDOC_URL)
        )


def get_env_file_path() -> Path:
    """获取环境变量文件路径"""
    return PROJECT_ROOT / ".env"


def get_env_template_path() -> Path:
    """获取环境变量模板文件路径"""
    return PROJECT_ROOT / "env_template.txt"


def load_env_file() -> None:
    """加载环境变量文件"""
    try:
        from dotenv import load_dotenv
        env_file = get_env_file_path()
        if env_file.exists():
            load_dotenv(env_file)
    except ImportError:
        pass  # python-dotenv 未安装时忽略


def validate_environment() -> None:
    """验证环境配置"""
    gemini_key = os.getenv(ENV_GEMINI_API_KEY)
    if not gemini_key or gemini_key == "your_gemini_api_key_here":
        raise ValueError(f"请设置正确的 {ENV_GEMINI_API_KEY} 环境变量")


# 全局配置实例
def get_app_config() -> AppConfig:
    """获取应用配置"""
    return AppConfig.from_env()


def get_server_config() -> ServerConfig:
    """获取服务器配置"""
    return ServerConfig.from_env()


def get_agent_config() -> AgentConfig:
    """获取Agent配置"""
    return AgentConfig.from_env()


# 初始化配置
load_env_file() 