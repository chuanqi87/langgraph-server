"""
Agent 测试模块
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from langgraph_agent.agent import create_agent, LangGraphAgent
from langgraph_agent.config import AgentConfig


class TestAgentConfig:
    """测试 AgentConfig 类"""
    
    def test_agent_config_default_values(self):
        """测试 AgentConfig 的默认值"""
        with patch('os.getenv') as mock_getenv:
            mock_getenv.return_value = "test_api_key"
            config = AgentConfig()
            assert config.model == "gemini-1.5-flash"
            assert config.temperature == 0.7
            assert config.api_key == "test_api_key"
    
    def test_agent_config_missing_api_key(self):
        """测试缺少API密钥时的行为"""
        with patch('os.getenv') as mock_getenv:
            mock_getenv.return_value = None
            with pytest.raises(ValueError, match="未设置.*环境变量"):
                AgentConfig()


class TestLangGraphAgent:
    """测试 LangGraphAgent 类"""
    
    @pytest.fixture
    def mock_config(self):
        """创建模拟配置"""
        with patch('os.getenv') as mock_getenv:
            mock_getenv.return_value = "test_api_key"
            return AgentConfig()
    
    def test_create_agent_success(self, mock_config):
        """测试成功创建 Agent"""
        with patch('langgraph_agent.agent.ChatGoogleGenerativeAI') as mock_llm:
            mock_llm.return_value = Mock()
            agent = create_agent(mock_config)
            assert isinstance(agent, LangGraphAgent)
            assert agent.config == mock_config
    
    def test_create_agent_with_default_config(self):
        """测试使用默认配置创建 Agent"""
        with patch('langgraph_agent.agent.get_agent_config') as mock_get_config:
            mock_get_config.return_value = Mock()
            with patch('langgraph_agent.agent.ChatGoogleGenerativeAI') as mock_llm:
                mock_llm.return_value = Mock()
                agent = create_agent()
                assert isinstance(agent, LangGraphAgent)
                mock_get_config.assert_called_once()


class TestMessageFormatter:
    """测试 MessageFormatter 类"""
    
    def test_format_message_dict(self):
        """测试格式化字典消息"""
        from langgraph_agent.agent import MessageFormatter
        from langchain_core.messages import HumanMessage, AIMessage
        
        # 测试用户消息
        user_msg = {"role": "user", "content": "Hello"}
        formatted = MessageFormatter.format_message(user_msg)
        assert isinstance(formatted, HumanMessage)
        assert formatted.content == "Hello"
        
        # 测试助手消息
        assistant_msg = {"role": "assistant", "content": "Hi there"}
        formatted = MessageFormatter.format_message(assistant_msg)
        assert isinstance(formatted, AIMessage)
        assert formatted.content == "Hi there"
    
    def test_format_message_string(self):
        """测试格式化字符串消息"""
        from langgraph_agent.agent import MessageFormatter
        from langchain_core.messages import HumanMessage
        
        formatted = MessageFormatter.format_message("Hello")
        assert isinstance(formatted, HumanMessage)
        assert formatted.content == "Hello"
    
    def test_format_messages_with_system_prompt(self):
        """测试格式化消息列表"""
        from langgraph_agent.agent import MessageFormatter
        from langchain_core.messages import SystemMessage, HumanMessage
        
        messages = [{"role": "user", "content": "Hello"}]
        system_prompt = "You are a helpful assistant."
        
        formatted = MessageFormatter.format_messages(messages, system_prompt)
        
        assert len(formatted) == 2
        assert isinstance(formatted[0], SystemMessage)
        assert formatted[0].content == system_prompt
        assert isinstance(formatted[1], HumanMessage)
        assert formatted[1].content == "Hello"


@pytest.mark.asyncio
class TestAgentIntegration:
    """测试 Agent 集成"""
    
    async def test_agent_invoke_success(self):
        """测试 Agent 调用成功"""
        with patch('langgraph_agent.agent.get_agent_config') as mock_get_config:
            mock_config = Mock()
            mock_config.model = "gemini-1.5-flash"
            mock_config.api_key = "test_key"
            mock_config.temperature = 0.7
            mock_config.max_tokens = 1024
            mock_config.system_prompt = "Test prompt"
            mock_get_config.return_value = mock_config
            
            with patch('langgraph_agent.agent.ChatGoogleGenerativeAI') as mock_llm_class:
                mock_llm = Mock()
                mock_response = Mock()
                mock_response.content = "Test response"
                mock_llm.invoke.return_value = mock_response
                mock_llm_class.return_value = mock_llm
                
                agent = create_agent()
                
                # 模拟异步调用
                with patch.object(agent.app, 'ainvoke', new_callable=AsyncMock) as mock_ainvoke:
                    mock_ainvoke.return_value = {
                        "messages": [{"role": "assistant", "content": "Test response"}]
                    }
                    
                    result = await agent.ainvoke(
                        {"messages": [{"role": "user", "content": "Hello"}]},
                        config={"configurable": {"thread_id": "test"}}
                    )
                    
                    assert result["messages"][0]["content"] == "Test response"
                    mock_ainvoke.assert_called_once()
    
    async def test_agent_invoke_error_handling(self):
        """测试 Agent 错误处理"""
        with patch('langgraph_agent.agent.get_agent_config') as mock_get_config:
            mock_config = Mock()
            mock_config.model = "gemini-1.5-flash"
            mock_config.api_key = "test_key"
            mock_config.temperature = 0.7
            mock_config.max_tokens = 1024
            mock_config.system_prompt = "Test prompt"
            mock_get_config.return_value = mock_config
            
            with patch('langgraph_agent.agent.ChatGoogleGenerativeAI') as mock_llm_class:
                mock_llm = Mock()
                mock_llm.invoke.side_effect = Exception("API Error")
                mock_llm_class.return_value = mock_llm
                
                agent = create_agent()
                
                # 模拟异步调用错误
                with patch.object(agent.app, 'ainvoke', new_callable=AsyncMock) as mock_ainvoke:
                    mock_ainvoke.side_effect = Exception("Agent Error")
                    
                    with pytest.raises(Exception, match="Agent Error"):
                        await agent.ainvoke(
                            {"messages": [{"role": "user", "content": "Hello"}]},
                            config={"configurable": {"thread_id": "test"}}
                        ) 