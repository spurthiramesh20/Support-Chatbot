from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage
from langchain_groq import ChatGroq
import yaml
from pathlib import Path


# ---------- Load prompt.yml ----------
PROMPT_PATH = Path(__file__).parent / "prompts" / "support_prompts.yml"
PROMPT_DATA = yaml.safe_load(PROMPT_PATH.read_text(encoding="utf-8"))
SYSTEM_PROMPT = PROMPT_DATA["v2"]["system"]


# ---------- Groq LLM ----------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
)


def chatbot_node(state: dict):
    """
    Single-pass chatbot node.
    Prompt controls flow. No loops.
    """
    messages = state["messages"]

    response = llm.invoke(
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + messages
    )

    return {
        "messages": messages + [AIMessage(content=response.content)]
    }


# ---------- LangGraph ----------
builder = StateGraph(dict)
builder.add_node("chatbot", chatbot_node)
builder.set_entry_point("chatbot")
builder.add_edge("chatbot", END)

app = builder.compile()
