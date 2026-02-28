from langchain_core.tools import tool
from typing import Optional
import uuid
# ========== REGISTRATION ISSUES ==========

@tool
def registration_unable_tool(email: str) -> str:
    """User is unable to register on the platform."""
    return (
        " Registration Issue: Unable to register.\n"
        "Please ensure:\n"
        "• You are using a valid government email\n"
        "• Parichay authentication is successful\n"
        "• Try again after clearing browser cache"
    )


@tool
def registration_email_exists_tool(email: str) -> str:
    """User gets 'email already exists' during registration."""
    return (
        f" The email **{email}** is already registered.\n"
        "Please try logging in instead or use the *Forgot Password* option."
    )


@tool
def registration_parichay_error_tool() -> str:
    """Parichay error during registration."""
    return (
        " Parichay Registration Error detected.\n"
        "Please ensure:\n"
        " Aadhaar is linked correctly\n"
        "• Parichay services are accessible\n"
        "• Try again after some time"
    )

# ========== LOGIN ISSUES ==========

@tool
def login_unable_tool(user_id: Optional[str] = None) -> str:
    """User is unable to login."""
    return (
        " Login failed.\n"
        "Please verify your credentials and try again.\n"
        "If the issue persists, reset your password."
    )


@tool
def login_otp_not_received_tool(email: str) -> str:
    """OTP not received during login."""
    return (
        f" OTP not received for **{email}**.\n"
        "Please wait 5-10 minutes and retry.\n"
        "Also check spam/junk folder."
    )


@tool
def login_parichay_error_tool() -> str:
    """Parichay authentication error during login."""
    return (
        " Parichay Login Error.\n"
        "Please retry logging in via Parichay.\n"
        "If the issue persists, Parichay services may be temporarily unavailable."
    )


@tool
def login_invalid_credentials_tool() -> str:
    """Invalid username or password."""
    return (
        "Invalid credentials.\n"
        "Please use *Forgot Password* to reset your password."
    )

# ========== COURSE ISSUES ==========

@tool
def course_not_visible_tool(course_name: Optional[str] = None) -> str:
    """Course not visible after enrollment."""
    return (
        f" Course **{course_name or ''}** is not visible.\n"
        "Please log out and log in again.\n"
        "If still not visible, syncing may be pending."
    )


@tool
def course_progress_stuck_tool(course_name: str) -> str:
    """Course progress stuck."""
    return (
        f" Progress for **{course_name}** appears stuck.\n"
        "Please complete all modules fully and refresh the page."
    )


@tool
def course_completion_not_updated_tool(course_name: str) -> str:
    """Course completion not updated."""
    return (
        f" Completion not updated for **{course_name}**.\n"
        "Completion sync can take up to 24 hours."
    )

# ========== CERTIFICATE ISSUES ==========

@tool
def certificate_not_generated_tool(course_name: str) -> str:
    """Certificate not generated after course completion."""
    return (
        f" Certificate not yet generated for **{course_name}**.\n"
        "Certificates are issued within 24 hours after completion."
    )


@tool
def certificate_name_incorrect_tool(correct_name: str) -> str:
    """Incorrect name on certificate."""
    return (
        f"Certificate name correction requested.\n"
        f"Correct name: **{correct_name}**.\n"
        "Our team will process this shortly."
    )


@tool
def certificate_download_failed_tool() -> str:
    """Certificate download failure."""
    return (
        "Certificate download failed.\n"
        "Please try using a different browser or device."
    )


@tool
def profile_not_visible_tool():
    """User profile not visible."""
    return (
        "If your profile is not visible:\n"
        "1. Log out and log back in.\n"
        "2. Check if your profile verification is pending.\n"
        "3. Ensure you are logged in with the correct email ID.\n"
        "4. Try clearing browser cache and refreshing the page.\n\n"
        "If the issue still persists, you can create a support ticket."
    )


@tool
def profile_update_failed_tool():
    """Profile update failed."""
    return (
        "If profile update is failing:\n"
        "1. Ensure all mandatory fields are filled.\n"
        "2. Avoid special characters in name or designation.\n"
        "3. Try updating from a different browser.\n\n"
        "If the issue still persists, you can create a support ticket."
    )


@tool
def profile_verification_pending_tool():
    """Profile verification pending."""
    return (
        "Profile verification can take some time.\n"
        "Please wait for verification to complete.\n"
        "If it remains pending for a long time, you may create a support ticket."
    )


@tool
def multiple_account_issue_tool():
    """Multiple accounts detected."""
    return (
        "Multiple accounts detected.\n"
        "Please use the primary registered email ID.\n"
        "Avoid creating duplicate accounts.\n\n"
        "If access is blocked, you may create a support ticket."
    )

# ---------------- DASHBOARD DATA ISSUES ---------------- #
@tool
def dashboard_data_not_visible_tool():
    """Dashboard data not visible."""
    return(
            "Your dashboard data is not visible.\n\n"
            "Steps to resolve:\n"
            "1. Log out and log in again.\n"
            "2. Refresh the dashboard page.\n"
            "3. Ensure at least one course is enrolled.\n\n"
            "If the issue still persists, you may proceed to create a support ticket."
        )


@tool
def dashboard_data_partial_visible_tool():
    """Dashboard data partially visible."""
    return  (
            "Only partial data is visible on your dashboard.\n\n"
            "Steps to resolve:\n"
            "1. Clear browser cache and cookies.\n"
            "2. Try accessing the dashboard using a different browser.\n\n"
            "If the issue continues, you may proceed to create a support ticket."
        )
    

# ---------------- KARMA POINT ISSUES ---------------- #
@tool
def dashboard_karma_points_missing_tool():
    """Dashboard karma points missing."""
    return  (
            "Your Karma points are missing from the dashboard.\n\n"
            "Steps to resolve:\n"
            "1. Karma points sync may take up to 24 hours.\n"
            "2. Refresh the dashboard after some time.\n\n"
            "If the issue still persists, you may proceed to create a support ticket."
        )


@tool
def dashboard_karma_points_not_updated_tool():
    """Dashboard karma points not updated."""
    return (
            "Your Karma points are not updating correctly.\n\n"
            "Steps to resolve:\n"
            "1. Esure course activities are fully completed.\n"
            "2. Log out and log back in after a few hours.\n\n"
            "If the issue remains unresolved, you may proceed to create a support ticket."
        )
    


# ---------------- WEEKLY CLAP ISSUES ---------------- #
@tool
def dashboard_weekly_clap_missing_tool():
    """Dashboard weekly clap missing."""
    return {
        "reply": (
            "Your weekly clap is missing from the dashboard.\n\n"
            "Steps to resolve:\n"
            "1. Weekly claps are updated once per week.\n"
            "2. Please wait for the next update cycle.\n\n"
            "If the issue still persists after the update, you may proceed to create a support ticket."
        )
    }

@tool
def dashboard_weekly_clap_not_reflecting_tool():
    """Dashboard weekly clap not reflecting."""
    return {
        "reply": (
            "Your weekly clap is not reflecting correctly.\n\n"
            "Steps to resolve:\n"
            "1. Refresh the dashboard page.\n"
            "2. Try logging in again after some time.\n\n"
            "If the issue persists, you may proceed to create a support ticket."
        )
    }


# ---------------- COURSE PROGRESS ON DASHBOARD ---------------- #
@tool
def dashboard_course_progress_not_updated_tool():
    """Dashboard course progress not updated."""
    return {
        "reply": (
            "Your course progress is not updated on the dashboard.\n\n"
            "Steps to resolve:\n"
            "1. Ensure all videos are watched till the end.\n"
            "2. Complete all required assessments.\n"
            "3. Refresh the dashboard page.\n\n"
            "If the issue continues, you may proceed to create a support ticket."
        )
    }

@tool
def dashboard_course_completed_not_reflected_tool():
    """Dashboard course completed not reflected."""
    return {
        "reply": (
            "Your completed course is not reflected on the dashboard.\n\n"
            "Steps to resolve:\n"
            "1. Log out and log back in.\n"
            "2. Wait for up to 24 hours for sync.\n\n"
            "If the issue still persists, you may proceed to create a support ticket."
        )
    }


# ---------------- DASHBOARD LOADING ISSUES ---------------- #
@tool
def dashboard_stuck_loading_tool():
    """Dashboard stuck loading."""
    return {
        "reply": (
            "Your dashboard is stuck on loading.\n\n"
            "Steps to resolve:\n"
            "1. Refresh the page.\n"
            "2. Disable browser extensions.\n"
            "3. Try accessing from a different browser or device.\n\n"
            "If the issue persists, you may proceed to create a support ticket."
        )
    }

@tool
def dashboard_blank_page_tool():
    """Dashboard blank page."""
    return {
        "reply": (
            "The dashboard page is appearing blank.\n\n"
            "Steps to resolve:\n"
            "1. Clear browser cache.\n"
            "2. Open the dashboard in incognito mode.\n\n"
            "If the issue continues, you may proceed to create a support ticket."
        )
    }

@tool
def create_support_ticket(
    email: str,
    phone_number: str,
    issue_type: str,
    issue_description: str
) -> str:
    """
    Creates a support ticket. This is the final escalation step when troubleshooting fails.
    Requires: email, phone_number, issue_type, and issue_description.

    Mandatory Fields:
    - Registered Email ID
    - Phone Number
    - Issue Type
    - Issue Description
    """

    # Validation 
    if not email or not phone_number or not issue_description:
        return (
            "To proceed, I need all required details:\n"
            "- Registered Email ID\n"
            "- Phone Number\n"
            "- Issue Description"
        )

    # Simulated ticket creation (replace with real API later)
    import uuid
    ticket_id = f"IGOT-{uuid.uuid4().hex[:8].upper()}"

    return (
        " Your support request has been successfully recorded.\n\n"
        f"Ticket ID: {ticket_id}\n"
        f"Issue Type: {issue_type}\n\n"
        "Our support team will review this and get back to you."
    )