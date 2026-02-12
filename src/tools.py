from langchain_core.tools import tool
import random

# ENSURE THIS NAME MATCHES EXACTLY
@tool
def check_igot_account_status(email: str):
    """Checks the link between iGOT ID and Parichay/SPV."""
    if "ramesh" in email.lower():
        return "RESULT: ID NOT LINKED. User must complete onboarding at janparichay.nic.in."
    return "RESULT: Account is active and synced."

# ENSURE THIS NAME MATCHES EXACTLY
@tool
def verify_certificate_eligibility(email: str, course_name: str):
    """Checks assessment scores for a course."""
    score = random.randint(50, 95)
    if score < 70:
        return f"RESULT: Assessment score for {course_name} is {score}%. 70% required."
    return f"RESULT: Eligibility met (Score: {score}%)."

# ENSURE THIS NAME MATCHES EXACTLY
@tool
def create_igot_ticket(email: str, issue_description: str):
    """Creates a formal support ticket."""
    ticket_id = f"IGOT-{random.randint(10000, 99999)}"
    return f"SUCCESS: Ticket {ticket_id} created for {email}."