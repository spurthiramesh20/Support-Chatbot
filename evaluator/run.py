import json
from evaluator.judge import llm_judge
from src.agent import app as graph_app


def handle_user_query(user_input: str) -> str:
    result = graph_app.invoke({"messages": [("user", user_input)]})
    messages = result.get("messages", [])
    if not messages:
        return ""
    last_msg = messages[-1]
    if hasattr(last_msg, "content") and last_msg.content:
        return last_msg.content
    return ""


def main():
    with open("evaluator/test_cases.json") as f:
        test_cases = json.load(f)

    results = []
    for case in test_cases:
        user_input = case["input"]

        # Call LangGraph chatbot
        bot_response = handle_user_query(user_input)

        # Judge it
        scores = llm_judge(user_input, bot_response)

        result = {
            "input": user_input,
            "response": bot_response,
            "scores": scores,
            "meta": {
                "framework": "langgraph"
            }
        }

        results.append(result)

    with open("evaluator/output.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("Wrote results to evaluator/output.json")


if __name__ == "__main__":
    main()
