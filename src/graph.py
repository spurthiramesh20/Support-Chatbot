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
from src.tools import check_igot_account_status, verify_certificate_eligibility, create_igot_ticket

# Load environment variables from root .env (fallback to src/.env if needed)
load_dotenv()
if not os.getenv("GROQ_API_KEY"):
    load_dotenv("src/.env")

# 1. Define the State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Initialize tools and LLM
tools = [check_igot_account_status, verify_certificate_eligibility, create_igot_ticket]
tool_node = ToolNode(tools)

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# 3. Define the Nodes
def assistant(state: State):
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: State):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

# 4. Build the Graph
builder = StateGraph(State)
builder.add_node("agent", assistant)
builder.add_node("tools", tool_node)

builder.set_entry_point("agent")
builder.add_conditional_edges("agent", should_continue)
builder.add_edge("tools", "agent")

# 5. Compile with Persistence
memory = MemorySaver()
app = builder.compile(checkpointer=memory)
