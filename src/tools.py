from langchain_core.tools import tool
import random

@tool
def check_igot_account_status(email: str):
    """Checks the link between iGOT ID and Parichay/SPV."""
    if "ramesh" in email.lower():
        return "RESULT: ID NOT LINKED. User must complete onboarding at janparichay.nic.in."
    return "RESULT: Account is active and synced."


@tool
def verify_certificate_eligibility(email: str, course_name: str):
    """Checks assessment scores for a course."""
    score = random.randint(50, 95)
    if score < 70:
        return f"RESULT: Assessment score for {course_name} is {score}%. 70% required."
    return f"RESULT: Eligibility met (Score: {score}%)."


@tool
def create_igot_ticket(email: str, phone: str, issue_description: str):
    """Creates a formal support ticket after all checks."""
    ticket_id = f"IGOT-{random.randint(10000, 99999)}"
    return (
        f"SUCCESS: Ticket prepared.\n"
        f"Ticket ID: {ticket_id}\n"
        f"Email: {email}\n"
        f"Phone: {phone}\n"
        f"Issue: {issue_description}"
    )
