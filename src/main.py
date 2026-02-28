import logging
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

# Load .env
_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=_ROOT / ".env")

from src.agent import app as graph_app  # noqa: E402

logging.getLogger("httpx").setLevel(logging.WARNING) 

api = FastAPI(title="Support Chatbot- LangGraph")

class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = "local_test" # Now matches your frontend localStorage ID

class ChatResponse(BaseModel):
    reply: str

@api.get("/health")
def health() -> dict:
    return {"status": "ok"}

@api.get("/", response_class=HTMLResponse)
def index() -> str:
    html_path = Path(__file__).parent / "chatbot.html"
    return html_path.read_text(encoding="utf-8")

@api.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    # 1. Prepare the thread configuration for MemorySaver
    config = {"configurable": {"thread_id": req.thread_id}}
    
    # 2. Use ainvoke (async) for smoother UI performance
    # This ensures history is preserved for this specific thread_id
    result = await graph_app.ainvoke(
        {"messages": [HumanMessage(content=req.message)]}, 
        config=config
    )

    # 3. Extract the last AI response
    messages = result.get("messages", [])
    reply = "I'm sorry, I couldn't process that. Please try again."
    
    if messages:
        last_msg = messages[-1]
        if hasattr(last_msg, "content") and last_msg.content:
            reply = last_msg.content

    return ChatResponse(reply=reply)

# CLI mode for testing
def run_bot():
    import asyncio
    config = {"configurable": {"thread_id": "cli_test_user"}}
    print("iGOT Support Bot (CLI) Online. Type 'exit' to quit.")
    
    async def main_loop():
        while True:
            user_input = input("User: ")
            if user_input.lower() in ["exit", "quit"]: break
            
            # Using stream for CLI feedback
            async for event in graph_app.astream({"messages": [HumanMessage(content=user_input)]}, config):
                for value in event.values():
                    if "messages" in value:
                        msg = value["messages"][-1]
                        if msg.type == "ai" and msg.content:
                            print(f"Bot: {msg.content}")

    asyncio.run(main_loop())

if __name__ == "__main__":
    run_bot()