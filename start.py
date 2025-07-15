#!/usr/bin/env python3
"""
快速启动脚本

LangGraph Agent 服务的快速启动工具。
自动检查环境、安装依赖、配置服务并启动应用。
"""

import os
import sys
import subprocess
import platform
from typing import Optional, Tuple, List
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 常量定义
MINIMUM_PYTHON_VERSION = (3, 8)
REQUIRED_FILES = ["requirements.txt", "src/langgraph_agent/main.py", "src/langgraph_agent/agent.py"]
ENV_FILE = ".env"
ENV_TEMPLATE = "env_template.txt"
GEMINI_API_STUDIO_URL = "https://aistudio.google.com/"
DEFAULT_PORT = 8000


class Colors:
    """终端颜色定义"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class StartupChecker:
    """启动检查器"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        
    def print_colored(self, message: str, color: str = Colors.WHITE) -> None:
        """打印带颜色的消息"""
        print(f"{color}{message}{Colors.END}")
    
    def print_success(self, message: str) -> None:
        """打印成功消息"""
        self.print_colored(f"✅ {message}", Colors.GREEN)
    
    def print_error(self, message: str) -> None:
        """打印错误消息"""
        self.print_colored(f"❌ {message}", Colors.RED)
    
    def print_warning(self, message: str) -> None:
        """打印警告消息"""
        self.print_colored(f"⚠️  {message}", Colors.YELLOW)
    
    def print_info(self, message: str) -> None:
        """打印信息消息"""
        self.print_colored(f"ℹ️  {message}", Colors.BLUE)
    
    def print_header(self, title: str) -> None:
        """打印标题"""
        self.print_colored(f"\n{Colors.BOLD}{title}{Colors.END}")
        self.print_colored("=" * len(title))
    
    def check_python_version(self) -> bool:
        """
        检查 Python 版本
        
        Returns:
            bool: 版本是否满足要求
        """
        current_version = sys.version_info[:2]
        
        if current_version < MINIMUM_PYTHON_VERSION:
            self.print_error(f"需要 Python {MINIMUM_PYTHON_VERSION[0]}.{MINIMUM_PYTHON_VERSION[1]} 或更高版本")
            self.print_error(f"当前版本: {sys.version}")
            return False
        
        self.print_success(f"Python 版本: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        return True
    
    def check_required_files(self) -> bool:
        """
        检查必需文件是否存在
        
        Returns:
            bool: 所有必需文件是否存在
        """
        missing_files = []
        
        for file_name in REQUIRED_FILES:
            file_path = self.project_root / file_name
            if not file_path.exists():
                missing_files.append(file_name)
        
        if missing_files:
            self.print_error(f"缺少必需文件: {', '.join(missing_files)}")
            return False
        
        self.print_success("所有必需文件都存在")
        return True
    
    def check_and_install_dependencies(self) -> bool:
        """
        检查并安装依赖
        
        Returns:
            bool: 依赖安装是否成功
        """
        requirements_file = self.project_root / "requirements.txt"
        
        if not requirements_file.exists():
            self.print_error("requirements.txt 文件不存在")
            return False
        
        try:
            self.print_info("正在安装依赖...")
            
            # 先尝试升级pip
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                capture_output=True,
                check=False
            )
            
            # 安装项目依赖
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            if result.returncode != 0:
                self.print_error("依赖安装失败:")
                self.print_error(result.stderr)
                return False
            
            self.print_success("依赖安装成功")
            return True
            
        except subprocess.TimeoutExpired:
            self.print_error("依赖安装超时")
            return False
        except Exception as e:
            self.print_error(f"依赖安装失败: {e}")
            return False
    
    def check_env_file(self) -> bool:
        """
        检查环境变量文件
        
        Returns:
            bool: 环境变量配置是否正确
        """
        env_file = self.project_root / ENV_FILE
        env_template = self.project_root / ENV_TEMPLATE
        
        # 检查 .env 文件是否存在
        if not env_file.exists():
            self.print_error(f"{ENV_FILE} 文件不存在")
            
            if env_template.exists():
                self.print_info("可以通过以下步骤创建环境变量文件:")
                self.print_info(f"1. 复制 {ENV_TEMPLATE} 为 {ENV_FILE}")
                self.print_info(f"2. 编辑 {ENV_FILE} 文件，设置你的 GEMINI_API_KEY")
                self.print_info(f"3. 获取 API Key: {GEMINI_API_STUDIO_URL}")
                
                # 提供自动创建选项
                response = input("\n是否要自动创建 .env 文件？(y/n): ").lower().strip()
                if response == 'y':
                    try:
                        env_template.read_text()
                        env_file.write_text(env_template.read_text())
                        self.print_success(f"已创建 {ENV_FILE} 文件")
                        self.print_warning(f"请编辑 {ENV_FILE} 文件并设置你的 GEMINI_API_KEY")
                    except Exception as e:
                        self.print_error(f"创建 {ENV_FILE} 文件失败: {e}")
                        return False
            else:
                self.print_error(f"{ENV_TEMPLATE} 模板文件也不存在")
            
            return False
        
        # 检查 API Key 是否设置
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
            
            gemini_key = os.getenv("GEMINI_API_KEY")
            if not gemini_key or gemini_key == "your_gemini_api_key_here":
                self.print_error("GEMINI_API_KEY 未正确设置")
                self.print_info(f"请在 {ENV_FILE} 文件中设置你的 Gemini API Key")
                self.print_info(f"获取地址: {GEMINI_API_STUDIO_URL}")
                return False
            
            self.print_success("环境变量配置正确")
            return True
            
        except ImportError:
            self.print_error("python-dotenv 未安装，请先安装依赖")
            return False
        except Exception as e:
            self.print_error(f"检查环境变量失败: {e}")
            return False
    
    def get_server_config(self) -> Tuple[str, int]:
        """
        获取服务器配置
        
        Returns:
            Tuple[str, int]: 主机地址和端口
        """
        host = "0.0.0.0"
        port = int(os.getenv("PORT", DEFAULT_PORT))
        
        return host, port
    
    def start_service(self) -> bool:
        """
        启动服务
        
        Returns:
            bool: 服务是否成功启动
        """
        try:
            host, port = self.get_server_config()
            
            self.print_header("🚀 启动 LangGraph Agent 服务")
            self.print_info(f"服务地址: http://{host}:{port}")
            self.print_info(f"API 文档: http://localhost:{port}/docs")
            self.print_info(f"ReDoc 文档: http://localhost:{port}/redoc")
            self.print_info("按 Ctrl+C 停止服务")
            self.print_colored("-" * 60, Colors.CYAN)
            
            # 启动服务
            subprocess.run([
                sys.executable, "-m", "uvicorn",
                "src.langgraph_agent.main:app",
                "--host", host,
                "--port", str(port),
                "--reload",
                "--log-level", "info"
            ])
            
            return True
            
        except KeyboardInterrupt:
            self.print_info("\n服务已停止")
            return True
        except FileNotFoundError:
            self.print_error("uvicorn 未找到，请确保已安装 FastAPI 和 uvicorn")
            return False
        except Exception as e:
            self.print_error(f"启动服务失败: {e}")
            return False
    
    def run_startup_checks(self) -> bool:
        """
        运行所有启动检查
        
        Returns:
            bool: 所有检查是否通过
        """
        checks = [
            ("检查 Python 版本", self.check_python_version),
            ("检查必需文件", self.check_required_files),
            ("安装依赖", self.check_and_install_dependencies),
            ("检查环境变量", self.check_env_file),
        ]
        
        for check_name, check_func in checks:
            self.print_header(f"🔍 {check_name}")
            
            if not check_func():
                self.print_error(f"{check_name} 失败")
                return False
        
        return True


def print_welcome_message() -> None:
    """打印欢迎消息"""
    welcome_text = """
    🤖 LangGraph Agent 服务启动器
    
    这个工具将帮助你快速设置和启动 LangGraph Agent 服务。
    它会自动检查环境、安装依赖并启动服务。
    """
    
    print(Colors.BOLD + Colors.CYAN + welcome_text + Colors.END)


def main() -> None:
    """
    主函数
    
    执行完整的启动流程：环境检查、依赖安装、服务启动。
    """
    print_welcome_message()
    
    checker = StartupChecker()
    
    # 运行启动检查
    if not checker.run_startup_checks():
        checker.print_error("启动检查失败，请解决上述问题后重试")
        sys.exit(1)
    
    # 启动服务
    if not checker.start_service():
        checker.print_error("服务启动失败")
        sys.exit(1)
    
    checker.print_success("服务启动完成")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}用户中断操作{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}启动过程中发生错误: {e}{Colors.END}")
        sys.exit(1) 