import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()


def llm_judge(user_input: str, bot_response: str) -> dict:
    prompt = (Path(__file__).parent / "judge_prompt.yml").read_text(encoding="utf-8")
    filled_prompt = (
        prompt.replace("{user_input}", user_input)
        .replace("{bot_response}", bot_response)
    )

    base_url = os.getenv("GEMINI_BASE_URL")
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-flash")

    if not api_key or not base_url:
        raise RuntimeError(
            "Missing GEMINI_API_KEY or GEMINI_BASE_URL. "
            "Set them in .env before running the evaluator."
        )

    llm = ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=0,
        timeout=60,
        max_retries=2,
    )

    resp = llm.invoke([HumanMessage(content=filled_prompt)])
    text = (resp.content or "").strip()

    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:].strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text}
