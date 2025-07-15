import os
from typing import TypedDict, Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import operator

# 定义状态
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]

def create_agent():
    """创建 LangGraph agent"""
    
    # 检查 API Key
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("未设置 GEMINI_API_KEY 环境变量")
    
    # 初始化 Gemini 模型
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=gemini_api_key,
        temperature=0.7
    )
    
    # 定义 agent 节点
    def call_model(state: AgentState):
        """调用模型生成回复"""
        messages = state["messages"]
        
        # 构建提示
        system_prompt = """你是一个有用的AI助手，基于 LangGraph 构建。
请用中文回复用户的问题，保持友好和专业的态度。"""
        
        # 格式化消息为 LangChain 消息格式
        formatted_messages = [SystemMessage(content=system_prompt)]
        for msg in messages:
            if isinstance(msg, dict):
                if msg.get("role") == "user":
                    formatted_messages.append(HumanMessage(content=msg["content"]))
                elif msg.get("role") == "assistant":
                    formatted_messages.append(AIMessage(content=msg["content"]))
                else:
                    formatted_messages.append(HumanMessage(content=str(msg)))
            elif isinstance(msg, str):
                formatted_messages.append(HumanMessage(content=msg))
            else:
                formatted_messages.append(HumanMessage(content=str(msg)))
        
        # 调用模型
        response = llm.invoke(formatted_messages)
        
        return {"messages": [{"role": "assistant", "content": response.content}]}
    
    # 创建图
    workflow = StateGraph(AgentState)
    
    # 添加节点
    workflow.add_node("agent", call_model)
    
    # 设置入口点和边
    workflow.add_edge(START, "agent")
    workflow.add_edge("agent", END)
    
    # 添加内存
    memory = MemorySaver()
    
    # 编译图
    app = workflow.compile(checkpointer=memory)
    
    return app

# 测试函数
async def test_agent():
    """测试 agent 功能"""
    agent = create_agent()
    
    # 测试对话
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "你好，请介绍一下你自己"}]},
        config={"configurable": {"thread_id": "test"}}
    )
    
    print("测试回复:", response["messages"][-1]["content"])

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_agent()) 