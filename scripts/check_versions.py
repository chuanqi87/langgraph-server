#!/usr/bin/env python3
"""
版本兼容性检查脚本
验证所有依赖包的版本是否正确安装且相互兼容
"""

import sys
import pkg_resources
from packaging import version

def check_package_version(package_name, expected_version):
    """检查包版本是否符合预期"""
    try:
        installed_version = pkg_resources.get_distribution(package_name).version
        if installed_version == expected_version:
            print(f"✅ {package_name}: {installed_version} (符合预期)")
            return True
        else:
            print(f"⚠️  {package_name}: {installed_version} (预期: {expected_version})")
            return False
    except pkg_resources.DistributionNotFound:
        print(f"❌ {package_name}: 未安装")
        return False

def check_import_compatibility():
    """检查导入兼容性"""
    print("\n🔍 检查导入兼容性...")
    
    try:
        # 测试 FastAPI
        from fastapi import FastAPI
        print("✅ FastAPI 导入成功")
        
        # 测试 LangGraph
        from langgraph.graph import StateGraph, START, END
        print("✅ LangGraph 导入成功")
        
        # 测试 LangChain
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
        print("✅ LangChain 导入成功")
        
        # 测试 Pydantic
        from pydantic import BaseModel
        print("✅ Pydantic 导入成功")
        
        # 测试其他依赖
        from dotenv import load_dotenv
        import httpx
        print("✅ 其他依赖导入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def main():
    print("🔍 开始版本兼容性检查...")
    print("=" * 50)
    
    # 预期版本
    expected_versions = {
        "fastapi": "0.116.1",
        "uvicorn": "0.34.0",
        "langgraph": "0.3.28",
        "langchain": "0.3.23",
        "langchain-google-genai": "2.0.11",
        "google-generativeai": "0.8.5",
        "pydantic": "2.10.4",
        "python-dotenv": "1.0.1",
        "httpx": "0.28.1"
    }
    
    # 检查版本
    print("📦 检查包版本...")
    version_ok = True
    for package, expected in expected_versions.items():
        if not check_package_version(package, expected):
            version_ok = False
    
    # 检查导入兼容性
    import_ok = check_import_compatibility()
    
    # 最终结果
    print("\n" + "=" * 50)
    if version_ok and import_ok:
        print("🎉 所有检查通过！环境配置正确。")
        print("你可以运行以下命令启动服务：")
        print("   python app.py")
        print("或者：")
        print("   python start.py")
        return 0
    else:
        print("❌ 检查未通过，请修复上述问题。")
        print("建议运行：")
        print("   pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 