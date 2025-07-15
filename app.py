from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from agent import create_agent
import asyncio

# 加载环境变量
load_dotenv()

app = FastAPI(
    title="LangGraph Agent Service",
    description="基于 LangGraph 构建的 Agent 服务，集成 Gemini 模型",
    version="1.0.0"
)

# 请求模型
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    session_id: str

# 全局变量存储 agent
agent = None

@app.on_event("startup")
async def startup_event():
    """应用启动时初始化 agent"""
    global agent
    try:
        agent = create_agent()
        print("Agent 初始化成功")
    except Exception as e:
        print(f"Agent 初始化失败: {e}")
        raise

@app.get("/")
async def root():
    """健康检查接口"""
    return {"message": "LangGraph Agent Service is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "agent_ready": agent is not None}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """聊天接口"""
    if not agent:
        raise HTTPException(status_code=500, detail="Agent 未初始化")
    
    try:
        # 调用 agent 处理消息
        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": request.message}]},
            config={"configurable": {"session_id": request.session_id}}
        )
        
        # 提取最后一条消息作为回复
        last_message = response["messages"][-1]
        return ChatResponse(
            response=last_message["content"],
            session_id=request.session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理请求时发生错误: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 