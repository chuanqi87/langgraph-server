#!/usr/bin/env python3
"""
测试部署的 LangGraph Agent 服务
"""

import requests
import json
import time
import sys
from typing import Dict, Any, Optional

class ServiceTester:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'LangGraph-Service-Tester/1.0'
        })
        
    def test_endpoint(self, endpoint: str, method: str = 'GET', data: Optional[Dict] = None) -> Dict[str, Any]:
        """测试单个端点"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, timeout=30)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, timeout=30)
            else:
                return {'success': False, 'error': f'不支持的方法: {method}'}
            
            result = {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds(),
                'content_type': response.headers.get('content-type', ''),
                'content_length': len(response.content)
            }
            
            try:
                result['data'] = response.json()
            except json.JSONDecodeError:
                result['data'] = response.text[:500]  # 截取前500字符
                
            return result
            
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': str(e)}
    
    def test_health_endpoints(self):
        """测试健康检查端点"""
        print("🔍 测试健康检查端点...")
        
        # 测试根路径
        print("\n📍 测试根路径 (/)")
        result = self.test_endpoint('/')
        if result['success']:
            print(f"✅ 根路径正常 - 响应时间: {result['response_time']:.2f}s")
            print(f"   数据: {result['data']}")
        else:
            print(f"❌ 根路径失败: {result.get('error', '未知错误')}")
        
        # 测试健康检查
        print("\n📍 测试健康检查 (/health)")
        result = self.test_endpoint('/health')
        if result['success']:
            print(f"✅ 健康检查正常 - 响应时间: {result['response_time']:.2f}s")
            print(f"   数据: {result['data']}")
        else:
            print(f"❌ 健康检查失败: {result.get('error', '未知错误')}")
            
        return result['success'] if result else False
    
    def test_chat_functionality(self):
        """测试聊天功能"""
        print("\n🤖 测试聊天功能...")
        
        # 测试用例
        test_cases = [
            {
                'name': '简单问候',
                'message': '你好！',
                'session_id': 'test_session_1'
            },
            {
                'name': '数学问题',
                'message': '请计算 2+2 等于多少？',
                'session_id': 'test_session_2'
            },
            {
                'name': '长文本测试',
                'message': '请解释什么是人工智能，以及它在现代社会中的应用场景。',
                'session_id': 'test_session_3'
            },
            {
                'name': '中文处理',
                'message': '请用中文回答：今天天气怎么样？',
                'session_id': 'test_session_4'
            }
        ]
        
        success_count = 0
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 测试用例 {i}: {test_case['name']}")
            print(f"   消息: {test_case['message']}")
            
            data = {
                'message': test_case['message'],
                'session_id': test_case['session_id']
            }
            
            result = self.test_endpoint('/chat', method='POST', data=data)
            
            if result['success']:
                print(f"✅ 测试通过 - 响应时间: {result['response_time']:.2f}s")
                response_data = result['data']
                print(f"   回复: {response_data.get('response', '无回复')[:100]}...")
                print(f"   会话ID: {response_data.get('session_id', '无')}")
                success_count += 1
            else:
                print(f"❌ 测试失败: {result.get('error', '未知错误')}")
                if 'data' in result:
                    print(f"   错误详情: {result['data']}")
        
        print(f"\n📊 聊天测试结果: {success_count}/{len(test_cases)} 通过")
        return success_count == len(test_cases)
    
    def test_error_handling(self):
        """测试错误处理"""
        print("\n🛡️ 测试错误处理...")
        
        # 测试空消息
        print("\n📍 测试空消息")
        result = self.test_endpoint('/chat', method='POST', data={'message': '', 'session_id': 'test'})
        print(f"   结果: {'✅ 正确处理' if not result['success'] or 'error' in str(result.get('data', '')) else '❌ 未正确处理'}")
        
        # 测试缺少字段
        print("\n📍 测试缺少必需字段")
        result = self.test_endpoint('/chat', method='POST', data={'session_id': 'test'})
        print(f"   结果: {'✅ 正确处理' if not result['success'] else '❌ 未正确处理'}")
        
        # 测试不存在的端点
        print("\n📍 测试不存在的端点")
        result = self.test_endpoint('/nonexistent')
        print(f"   结果: {'✅ 正确处理' if result['status_code'] == 404 else '❌ 未正确处理'}")
        
    def test_performance(self):
        """测试性能"""
        print("\n⚡ 测试性能...")
        
        # 并发测试
        print("\n📍 测试响应时间")
        times = []
        for i in range(5):
            result = self.test_endpoint('/health')
            if result['success']:
                times.append(result['response_time'])
            time.sleep(0.1)
        
        if times:
            avg_time = sum(times) / len(times)
            max_time = max(times)
            min_time = min(times)
            print(f"   平均响应时间: {avg_time:.2f}s")
            print(f"   最大响应时间: {max_time:.2f}s")
            print(f"   最小响应时间: {min_time:.2f}s")
            print(f"   性能评级: {'✅ 优秀' if avg_time < 1 else '⚠️ 一般' if avg_time < 3 else '❌ 较慢'}")
        else:
            print("   ❌ 无法获取响应时间数据")
    
    def run_all_tests(self):
        """运行所有测试"""
        print(f"🚀 开始测试服务: {self.base_url}")
        print("=" * 60)
        
        # 1. 健康检查
        health_ok = self.test_health_endpoints()
        
        if not health_ok:
            print("\n❌ 健康检查失败，跳过其他测试")
            return False
        
        # 2. 聊天功能测试
        chat_ok = self.test_chat_functionality()
        
        # 3. 错误处理测试
        self.test_error_handling()
        
        # 4. 性能测试
        self.test_performance()
        
        # 总结
        print("\n" + "=" * 60)
        print("📋 测试总结:")
        print(f"   健康检查: {'✅ 通过' if health_ok else '❌ 失败'}")
        print(f"   聊天功能: {'✅ 通过' if chat_ok else '❌ 失败'}")
        print(f"   整体状态: {'✅ 服务正常' if health_ok and chat_ok else '⚠️ 存在问题'}")
        
        return health_ok and chat_ok

def main():
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = 'https://langgraph-server-84mc.onrender.com'
    
    print(f"🔧 LangGraph Agent 服务测试工具")
    print(f"📍 测试地址: {base_url}")
    print(f"⏰ 测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    tester = ServiceTester(base_url)
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 