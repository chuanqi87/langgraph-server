#!/usr/bin/env python3
"""
Render 部署验证脚本
用于测试部署到 Render 后的服务状态
"""

import asyncio
import httpx
import sys
import os
from urllib.parse import urlparse

async def test_deployment(base_url):
    """测试部署的服务"""
    print(f"测试部署的服务: {base_url}")
    
    # 测试结果
    results = {
        "health": False,
        "root": False,
        "chat": False
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        
        # 1. 测试根路径
        try:
            print("\n1. 测试根路径...")
            response = await client.get(f"{base_url}/")
            print(f"状态码: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"响应: {data}")
                results["root"] = True
            else:
                print(f"错误: {response.text}")
        except Exception as e:
            print(f"根路径测试失败: {e}")
        
        # 2. 测试健康检查
        try:
            print("\n2. 测试健康检查...")
            response = await client.get(f"{base_url}/health")
            print(f"状态码: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"响应: {data}")
                results["health"] = data.get("status") == "healthy"
            else:
                print(f"错误: {response.text}")
        except Exception as e:
            print(f"健康检查失败: {e}")
        
        # 3. 测试聊天接口
        if results["health"]:
            try:
                print("\n3. 测试聊天接口...")
                payload = {
                    "message": "你好，这是一个部署测试",
                    "session_id": "deploy_test"
                }
                response = await client.post(f"{base_url}/chat", json=payload)
                print(f"状态码: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"回复: {data['response'][:100]}...")
                    results["chat"] = True
                else:
                    print(f"错误: {response.text}")
            except Exception as e:
                print(f"聊天接口测试失败: {e}")
        else:
            print("\n3. 跳过聊天接口测试 (健康检查失败)")
    
    return results

def print_results(results):
    """打印测试结果"""
    print("\n" + "="*50)
    print("部署验证结果:")
    print("="*50)
    
    status_icon = lambda x: "✅" if x else "❌"
    
    print(f"{status_icon(results['root'])} 根路径: {'正常' if results['root'] else '异常'}")
    print(f"{status_icon(results['health'])} 健康检查: {'正常' if results['health'] else '异常'}")
    print(f"{status_icon(results['chat'])} 聊天功能: {'正常' if results['chat'] else '异常'}")
    
    if all(results.values()):
        print("\n🎉 所有测试通过！部署成功！")
        return True
    else:
        print("\n⚠️  部分测试失败，请检查部署配置")
        return False

async def main():
    """主函数"""
    # 从命令行参数获取 URL，或使用默认值
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = input("请输入你的 Render 部署 URL (如: https://your-app.onrender.com): ").strip()
    
    # 验证 URL 格式
    try:
        parsed = urlparse(base_url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("无效的 URL 格式")
    except Exception as e:
        print(f"URL 格式错误: {e}")
        print("请使用完整的 URL，例如: https://your-app.onrender.com")
        return
    
    # 移除末尾的斜杠
    base_url = base_url.rstrip('/')
    
    try:
        results = await test_deployment(base_url)
        success = print_results(results)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 