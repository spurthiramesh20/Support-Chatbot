import operator
import os
import yaml
from typing import Annotated, TypedDict, Union
from pathlib import Path

from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI

# 1. Stick to the TypedDict for proper state management
class SupportState(TypedDict):
    # Annotated with operator.add ensures new messages are appended, not overwritten
    messages: Annotated[list[BaseMessage], operator.add]

# -------- Load tools --------
from src.tools import (
    registration_unable_tool,
    registration_email_exists_tool,
    registration_parichay_error_tool,
    login_unable_tool,
    login_otp_not_received_tool,
    login_parichay_error_tool,
    login_invalid_credentials_tool,
    course_not_visible_tool,
    course_progress_stuck_tool,
    course_completion_not_updated_tool,
    certificate_not_generated_tool,
    certificate_name_incorrect_tool,
    certificate_download_failed_tool,
    profile_not_visible_tool,
    profile_update_failed_tool,
    profile_verification_pending_tool,
    multiple_account_issue_tool,
    dashboard_data_not_visible_tool,
    dashboard_data_partial_visible_tool,
    dashboard_karma_points_missing_tool,
    dashboard_karma_points_not_updated_tool,
    dashboard_weekly_clap_missing_tool,
    dashboard_weekly_clap_not_reflecting_tool,
    dashboard_course_progress_not_updated_tool,
    dashboard_course_completed_not_reflected_tool,
    dashboard_stuck_loading_tool,
    dashboard_blank_page_tool,
    create_support_ticket,
)

TOOLS = [
    registration_unable_tool, registration_email_exists_tool, registration_parichay_error_tool,
    login_unable_tool, login_otp_not_received_tool, login_parichay_error_tool, login_invalid_credentials_tool,
    course_not_visible_tool, course_progress_stuck_tool, course_completion_not_updated_tool,
    certificate_not_generated_tool, certificate_name_incorrect_tool, certificate_download_failed_tool,
    profile_not_visible_tool, profile_update_failed_tool, profile_verification_pending_tool, multiple_account_issue_tool,
    dashboard_data_not_visible_tool, dashboard_data_partial_visible_tool, dashboard_karma_points_missing_tool,
    dashboard_karma_points_not_updated_tool, dashboard_weekly_clap_missing_tool, dashboard_weekly_clap_not_reflecting_tool,
    dashboard_course_progress_not_updated_tool, dashboard_course_completed_not_reflected_tool,
    dashboard_stuck_loading_tool, dashboard_blank_page_tool, create_support_ticket,
]

# -------- Load system prompt --------
PROMPT_PATH = Path(__file__).parent / "prompts" / "prompt.yml"
PROMPT_DATA = yaml.safe_load(PROMPT_PATH.read_text(encoding="utf-8"))
SYSTEM_PROMPT = PROMPT_DATA["v1"]["system"]

# -------- Gemini via LiteLLM --------
llm = ChatOpenAI(
    model=os.getenv("GEMINI_MODEL", "gemini-flash"),
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=os.getenv("GEMINI_BASE_URL"),
    temperature=0.2,
).bind_tools(TOOLS)

# -------- Agent Node --------
def agent_node(state: SupportState):
    messages = state["messages"]
    response = llm.invoke(
        [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    )
    return {"messages": [response]}

# 3. FIXED: Correct Graph Construction
builder = StateGraph(SupportState)

builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(TOOLS))

builder.set_entry_point("agent")

# 4. FIXED: Conditional logic to decide between Tool use and Ending
def should_continue(state: SupportState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

builder.add_conditional_edges("agent", should_continue)

# 5. FIXED: The Cyclic Edge
# Tool results must go back to the agent so the LLM can see the output
builder.add_edge("tools", "agent")

# 6. Memory for conversation persistence
memory = MemorySaver()
app = builder.compile(checkpointer=memory)