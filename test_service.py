import asyncio
import httpx
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

async def test_health():
    """测试健康检查接口"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8000/health")
            print(f"健康检查状态: {response.status_code}")
            print(f"响应: {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"健康检查失败: {e}")
            return False

async def test_chat():
    """测试聊天接口"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            payload = {
                "message": "你好，请介绍一下你自己",
                "session_id": "test_session"
            }
            response = await client.post("http://localhost:8000/chat", json=payload)
            print(f"聊天接口状态: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"回复: {result['response']}")
                return True
            else:
                print(f"错误: {response.text}")
                return False
        except Exception as e:
            print(f"聊天接口测试失败: {e}")
            return False

async def main():
    """主测试函数"""
    print("开始测试 LangGraph Agent 服务...")
    
    # 检查环境变量
    if not os.getenv("GEMINI_API_KEY"):
        print("警告: 未设置 GEMINI_API_KEY 环境变量")
        return
    
    # 测试健康检查
    print("\n1. 测试健康检查接口...")
    health_ok = await test_health()
    
    if not health_ok:
        print("健康检查失败，请检查服务是否启动")
        return
    
    # 测试聊天功能
    print("\n2. 测试聊天接口...")
    chat_ok = await test_chat()
    
    if chat_ok:
        print("\n✅ 所有测试通过！服务运行正常")
    else:
        print("\n❌ 聊天接口测试失败")

if __name__ == "__main__":
    asyncio.run(main()) 