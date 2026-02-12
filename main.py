import logging
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
    return """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Support Chatbot</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
      :root {
        --ink: #0f172a;
        --muted: #475569;
        --bg: #f8fafc;
        --card: #ffffff;
        --accent: #2563eb;
        --border: #e2e8f0;
        --shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        min-height: 100vh;
        font-family: "Plus Jakarta Sans", system-ui, -apple-system, Segoe UI, sans-serif;
        color: var(--ink);
        background: var(--bg);
      }
      .wrap {
        max-width: 820px;
        margin: 0 auto;
        padding: 40px 16px 64px;
      }
      .title {
        font-size: 28px;
        font-weight: 700;
        margin: 0 0 8px;
      }
      .card {
        background: var(--card);
        border-radius: 12px;
        padding: 16px;
        box-shadow: var(--shadow);
        border: 1px solid var(--border);
      }
      .chat {
        display: grid;
        grid-template-rows: 1fr auto;
        height: 520px;
      }
      .messages {
        overflow: auto;
        padding: 6px;
        display: flex;
        flex-direction: column;
        gap: 12px;
      }
      .bubble {
        max-width: 80%;
        padding: 12px 14px;
        border-radius: 14px;
        font-size: 14px;
        line-height: 1.4;
        position: relative;
        animation: floatIn 360ms ease;
        white-space: pre-line;
      }
      .bubble.user {
        align-self: flex-end;
        background: var(--accent);
        color: white;
        border-top-right-radius: 6px;
      }
      .bubble.bot {
        align-self: flex-start;
        background: #f1f5f9;
        border: 1px solid var(--border);
        border-top-left-radius: 6px;
      }
      .composer {
        display: grid;
        grid-template-columns: 1fr auto;
        gap: 12px;
        margin-top: 12px;
      }
      .input {
        padding: 12px 14px;
        border-radius: 10px;
        border: 1px solid var(--border);
        font-size: 14px;
        font-family: inherit;
      }
      .btn {
        border: none;
        background: var(--accent);
        color: white;
        padding: 12px 16px;
        border-radius: 10px;
        cursor: pointer;
        font-weight: 600;
        letter-spacing: 0.2px;
        transition: transform 120ms ease, box-shadow 120ms ease;
        box-shadow: 0 10px 20px rgba(37, 99, 235, 0.25);
      }
      .btn:active { transform: translateY(1px); }
      @keyframes floatIn {
        from { transform: translateY(6px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
      }
      @media (max-width: 640px) {
        .chat { height: 520px; }
      }
    </style>
  </head>
  <body>
    <div class="wrap">
      <h1 class="title">Support Chatbot</h1>
      <div class="card chat">
        <div id="messages" class="messages"></div>
        <div class="composer">
          <input id="input" class="input" placeholder="Type your message..." />
          <button id="send" class="btn">Send</button>
        </div>
      </div>
    </div>
    <script>
      const messages = document.getElementById("messages");
      const input = document.getElementById("input");
      const send = document.getElementById("send");

      function addBubble(text, who) {
        const div = document.createElement("div");
        div.className = `bubble ${who}`;
        div.textContent = text;
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
      }

      async function sendMessage() {
        const text = input.value.trim();
        if (!text) return;
        addBubble(text, "user");
        input.value = "";

        const res = await fetch("/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: text, thread_id: "ui_demo" })
        });
        const data = await res.json();
        addBubble(data.reply || "No response.", "bot");
      }

      send.addEventListener("click", sendMessage);
      input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") sendMessage();
      });

      addBubble("Hi! How can I help you today?", "bot");
    </script>
  </body>
</html>
"""


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
