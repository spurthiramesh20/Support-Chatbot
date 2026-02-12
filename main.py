import logging
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from src.graph import app as graph_app

logging.getLogger("httpx").setLevel(logging.WARNING) # Silences the HTTP logs

api = FastAPI(title="Support Chatbot")


class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = "local_test"


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
def chat(req: ChatRequest) -> ChatResponse:
    config = {"configurable": {"thread_id": req.thread_id}}
    result = graph_app.invoke({"messages": [("user", req.message)]}, config)

    messages = result.get("messages", [])
    reply = ""
    if messages:
        last_msg = messages[-1]
        if hasattr(last_msg, "content") and last_msg.content:
            reply = last_msg.content

    return ChatResponse(reply=reply)

def run_bot():
    config = {"configurable": {"thread_id": "igot_user_1"}}
    print("iGOT Support Bot is Online. Type 'exit' to quit.")
    
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]: break
        
        for event in graph_app.stream({"messages": [("user", user_input)]}, config):
            for value in event.values():
                if "messages" in value:
                    msg = value["messages"][-1]
                    if hasattr(msg, "content") and msg.content:
                        print(f"\nBot: {msg.content}")

if __name__ == "__main__":
    run_bot()
