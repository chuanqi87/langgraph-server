"""
LangGraph Agent 实现

基于 LangGraph 和 Google Gemini 模型的智能 Agent 实现。
提供对话管理、消息处理和状态维护功能。
"""

import logging
from typing import TypedDict, Annotated, List, Dict, Any, Union

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
import operator

from .config import AgentConfig, get_agent_config, LOG_FORMAT

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT
)
logger = logging.getLogger(__name__)


class AgentState(TypedDict):
    """Agent 状态类型定义"""
    
    messages: Annotated[List[Dict[str, str]], operator.add]


class MessageFormatter:
    """消息格式化器"""
    
    @staticmethod
    def format_message(msg: Union[Dict[str, Any], str, BaseMessage]) -> BaseMessage:
        """
        格式化单个消息为 LangChain 消息格式
        
        Args:
            msg: 输入消息，可以是字典、字符串或 BaseMessage
            
        Returns:
            BaseMessage: 格式化后的消息
        """
        if isinstance(msg, BaseMessage):
            return msg
        elif isinstance(msg, dict):
            role = msg.get("role", "user")
            content = msg.get("content", str(msg))
            
            if role == "user":
                return HumanMessage(content=content)
            elif role == "assistant":
                return AIMessage(content=content)
            elif role == "system":
                return SystemMessage(content=content)
            else:
                return HumanMessage(content=content)
        elif isinstance(msg, str):
            return HumanMessage(content=msg)
        else:
            return HumanMessage(content=str(msg))
    
    @staticmethod
    def format_messages(messages: List[Any], system_prompt: str) -> List[BaseMessage]:
        """
        格式化消息列表为 LangChain 消息格式
        
        Args:
            messages: 原始消息列表
            system_prompt: 系统提示词
            
        Returns:
            List[BaseMessage]: 格式化后的消息列表
        """
        formatted_messages = [SystemMessage(content=system_prompt)]
        
        for msg in messages:
            try:
                formatted_msg = MessageFormatter.format_message(msg)
                formatted_messages.append(formatted_msg)
            except Exception as e:
                logger.warning(f"格式化消息失败: {e}, 消息: {msg}")
                # 如果格式化失败，将其转换为字符串消息
                formatted_messages.append(HumanMessage(content=str(msg)))
        
        return formatted_messages


class LangGraphAgent:
    """LangGraph Agent 类"""
    
    def __init__(self, config: AgentConfig):
        """
        初始化 Agent
        
        Args:
            config: Agent 配置
        """
        self.config = config
        self.llm = self._create_llm()
        self.formatter = MessageFormatter()
        self.workflow = self._create_workflow()
        self.app = self._compile_workflow()
    
    def _create_llm(self) -> ChatGoogleGenerativeAI:
        """
        创建语言模型实例
        
        Returns:
            ChatGoogleGenerativeAI: 配置好的语言模型
        """
        try:
            return ChatGoogleGenerativeAI(
                model=self.config.model,
                google_api_key=self.config.api_key,
                temperature=self.config.temperature,
                max_output_tokens=self.config.max_tokens
            )
        except Exception as e:
            logger.error(f"创建语言模型失败: {e}")
            raise
    
    def _create_workflow(self) -> StateGraph:
        """
        创建工作流图
        
        Returns:
            StateGraph: 配置好的工作流图
        """
        workflow = StateGraph(AgentState)
        
        # 添加节点
        workflow.add_node("agent", self._call_model)
        
        # 设置边
        workflow.add_edge(START, "agent")
        workflow.add_edge("agent", END)
        
        return workflow
    
    def _compile_workflow(self):
        """
        编译工作流
        
        Returns:
            编译后的工作流应用
        """
        try:
            memory = MemorySaver()
            app = self.workflow.compile(checkpointer=memory)
            logger.info("工作流编译成功")
            return app
        except Exception as e:
            logger.error(f"工作流编译失败: {e}")
            raise
    
    def _call_model(self, state: AgentState) -> Dict[str, List[Dict[str, str]]]:
        """
        调用模型生成回复
        
        Args:
            state: 当前状态
            
        Returns:
            Dict: 包含新消息的状态更新
        """
        try:
            messages = state["messages"]
            
            # 格式化消息
            formatted_messages = self.formatter.format_messages(
                messages, 
                self.config.system_prompt
            )
            
            # 调用模型
            response = self.llm.invoke(formatted_messages)
            
            if not response or not response.content:
                logger.error("模型响应为空")
                return {"messages": [{"role": "assistant", "content": "抱歉，我暂时无法回答您的问题。"}]}
            
            return {"messages": [{"role": "assistant", "content": response.content}]}
            
        except Exception as e:
            logger.error(f"调用模型失败: {e}")
            return {"messages": [{"role": "assistant", "content": f"处理请求时发生错误: {str(e)}"}]}
    
    async def ainvoke(self, input_data: Dict[str, Any], config: Dict[str, Any] = None):
        """
        异步调用 Agent
        
        Args:
            input_data: 输入数据
            config: 配置参数
            
        Returns:
            Agent 响应
        """
        try:
            return await self.app.ainvoke(input_data, config)
        except Exception as e:
            logger.error(f"Agent 调用失败: {e}")
            raise


def create_agent(config: AgentConfig = None) -> LangGraphAgent:
    """
    创建 LangGraph Agent 实例
    
    Args:
        config: Agent 配置，如果为 None 则使用默认配置
        
    Returns:
        LangGraphAgent: 配置好的 Agent 实例
        
    Raises:
        ValueError: 当配置错误时
        Exception: 当创建失败时
    """
    try:
        if config is None:
            config = get_agent_config()
        
        logger.info(f"创建 Agent - 模型: {config.model}, 温度: {config.temperature}")
        agent = LangGraphAgent(config)
        logger.info("Agent 创建成功")
        return agent
        
    except Exception as e:
        logger.error(f"创建 Agent 失败: {e}")
        raise


async def test_agent() -> None:
    """
    测试 Agent 功能
    
    创建 Agent 实例并进行简单的对话测试。
    """
    try:
        logger.info("开始测试 Agent 功能...")
        
        # 创建 Agent
        agent = create_agent()
        
        # 测试用例
        test_cases = [
            "你好，请介绍一下你自己",
            "请计算 2 + 2 等于多少？",
            "你能用中文回答问题吗？"
        ]
        
        for i, test_message in enumerate(test_cases, 1):
            logger.info(f"测试用例 {i}: {test_message}")
            
            response = await agent.ainvoke(
                {"messages": [{"role": "user", "content": test_message}]},
                config={"configurable": {"thread_id": f"test_{i}"}}
            )
            
            if response and response.get("messages"):
                reply = response["messages"][-1]["content"]
                logger.info(f"回复 {i}: {reply[:100]}...")
            else:
                logger.error(f"测试用例 {i} 失败：无响应")
        
        logger.info("Agent 测试完成")
        
    except Exception as e:
        logger.error(f"Agent 测试失败: {e}")
        raise


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_agent()) 