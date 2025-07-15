#!/usr/bin/env python3
"""
快速启动脚本
帮助用户快速设置和启动 LangGraph Agent 服务
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """检查 Python 版本"""
    if sys.version_info < (3, 8):
        print("❌ 需要 Python 3.8 或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    print(f"✅ Python 版本: {sys.version}")
    return True

def check_and_install_dependencies():
    """检查并安装依赖"""
    print("\n检查依赖...")
    
    # 检查 requirements.txt 是否存在
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt 文件不存在")
        return False
    
    try:
        # 安装依赖
        print("正在安装依赖...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("❌ 依赖安装失败:")
            print(result.stderr)
            return False
        
        print("✅ 依赖安装成功")
        return True
    except Exception as e:
        print(f"❌ 依赖安装失败: {e}")
        return False

def check_env_file():
    """检查环境变量文件"""
    print("\n检查环境变量配置...")
    
    if not os.path.exists(".env"):
        print("❌ .env 文件不存在")
        print("请按照以下步骤创建 .env 文件：")
        print("1. 复制 env_template.txt 为 .env")
        print("2. 编辑 .env 文件，设置你的 GEMINI_API_KEY")
        print("3. 获取 API Key: https://aistudio.google.com/")
        return False
    
    # 检查 API Key 是否设置
    from dotenv import load_dotenv
    load_dotenv()
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key or gemini_key == "your_gemini_api_key_here":
        print("❌ GEMINI_API_KEY 未正确设置")
        print("请在 .env 文件中设置你的 Gemini API Key")
        print("获取地址: https://aistudio.google.com/")
        return False
    
    print("✅ 环境变量配置正确")
    return True

def start_service():
    """启动服务"""
    print("\n🚀 启动 LangGraph Agent 服务...")
    
    try:
        # 获取端口
        port = os.getenv("PORT", "8000")
        
        # 启动服务
        print(f"服务将在 http://localhost:{port} 启动")
        print("按 Ctrl+C 停止服务")
        print("-" * 50)
        
        # 使用 uvicorn 启动
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app:app",
            "--host", "0.0.0.0",
            "--port", str(port),
            "--reload"
        ])
        
    except KeyboardInterrupt:
        print("\n服务已停止")
    except Exception as e:
        print(f"❌ 启动服务失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("🤖 LangGraph Agent 服务启动器")
    print("=" * 50)
    
    # 检查 Python 版本
    if not check_python_version():
        return
    
    # 安装依赖
    if not check_and_install_dependencies():
        return
    
    # 检查环境变量
    if not check_env_file():
        return
    
    # 启动服务
    start_service()

if __name__ == "__main__":
    main() 