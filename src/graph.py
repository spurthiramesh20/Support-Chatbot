import os
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from src.prompt import SYSTEM_PROMPT
from src.tools import (
    check_igot_account_status,
    verify_certificate_eligibility,
    create_igot_ticket,
)

# Load env
load_dotenv()
if not os.getenv("GROQ_API_KEY"):
    load_dotenv("src/.env")

# ---- State ----
class State(TypedDict):
    messages: Annotated[list, add_messages]

# ---- Tools ----
tools = [
    check_igot_account_status,
    verify_certificate_eligibility,
    create_igot_ticket,
]

tool_node = ToolNode(tools)

# ---- LLM ----
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
)

llm_with_tools = llm.bind_tools(tools)

# ---- Agent Node ----
def agent(state: State):
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# ---- Routing Logic ----
def route(state: State):
    last_msg = state["messages"][-1]
    if getattr(last_msg, "tool_calls", None):
        return "tools"
    return END

# ---- Graph ----
builder = StateGraph(State)

builder.add_node("agent", agent)
builder.add_node("tools", tool_node)

builder.set_entry_point("agent")
builder.add_conditional_edges("agent", route)
builder.add_edge("tools", "agent")

# ---- Compile ----
memory = MemorySaver()
app = builder.compile(checkpointer=memory)
