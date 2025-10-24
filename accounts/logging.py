import logging
from django.utils import timezone
from .models import User

# Get a logger instance
logger = logging.getLogger('accounts')

def log_failed_login(username, ip_address=None, user_agent=None):
    """
    Log failed login attempts.
    """
    logger.warning(
        f"Failed login attempt for username: {username} "
        f"from IP: {ip_address} "
        f"with User-Agent: {user_agent} "
        f"at {timezone.now()}"
    )

def log_successful_login(user, ip_address=None, user_agent=None):
    """
    Log successful login attempts.
    """
    logger.info(
        f"Successful login for user: {user.username} (ID: {user.id}) "
        f"from IP: {ip_address} "
        f"with User-Agent: {user_agent} "
        f"at {timezone.now()}"
    )

def log_password_change(user):
    """
    Log password change events.
    """
    logger.info(
        f"Password changed for user: {user.username} (ID: {user.id}) "
        f"at {timezone.now()}"
    )

def log_account_lockout(username, ip_address=None):
    """
    Log account lockout events.
    """
    logger.warning(
        f"Account locked out for username: {username} "
        f"from IP: {ip_address} "
        f"at {timezone.now()}"
    )

def log_suspicious_activity(user, activity_type, details=None, ip_address=None):
    """
    Log suspicious activities.
    """
    logger.warning(
        f"Suspicious activity detected - Type: {activity_type} "
        f"for user: {user.username} (ID: {user.id}) "
        f"Details: {details} "
        f"from IP: {ip_address} "
        f"at {timezone.now()}"
    )