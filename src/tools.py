from typing import List, Optional
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool

MAX_RETRIES = 2


class SupportState(TypedDict, total=False):
    messages: List[BaseMessage]
    email: Optional[str]
    password_tried: Optional[bool]
    otp_received: Optional[bool]
    last_action: Optional[str]
    retry_count: Optional[int]


def _loop_guard(state: SupportState, action: str) -> bool:
    return (
        state.get("last_action") == action
        and state.get("retry_count", 0) >= MAX_RETRIES
    )


@tool
def handle_login_issue(state: SupportState) -> str:
    """Guide the user through the login troubleshooting flow based on state."""
    # ASK EMAIL
    if state.get("email") is None:
        if _loop_guard(state, "ASK_EMAIL"):
            return "I’ll pause here \nShare your registered email when ready."

        state["last_action"] = "ASK_EMAIL"
        state["retry_count"] = state.get("retry_count", 0) + 1
        return "Please confirm your registered email ID."

    # PASSWORD RESET
    if state.get("password_tried") is None:
        if _loop_guard(state, "ASK_PASSWORD"):
            return "Let me know once you’ve tried resetting your password."

        state["last_action"] = "ASK_PASSWORD"
        state["retry_count"] = state.get("retry_count", 0) + 1
        return "Have you tried resetting your password using *Forgot Password*?"

    # OTP CHECK
    if state["password_tried"] and state.get("otp_received") is None:
        if _loop_guard(state, "ASK_OTP"):
            return "Please wait a few minutes — OTPs can take time "

        state["last_action"] = "ASK_OTP"
        state["retry_count"] = state.get("retry_count", 0) + 1
        return "Did you receive an OTP?"

    # OTP NOT RECEIVED
    if state.get("otp_received") is False:
        return "OTPs can take up to 10 minutes. Please retry."

    return " I can escalate this to support if needed."
