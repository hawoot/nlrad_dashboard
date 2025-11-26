"""
User identification for logging and audit trails.
"""
import os
import getpass


def get_current_user():
    """
    Get current user identifier.

    Tries multiple strategies in order:
    1. Environment variable USER_ID (for explicit setting)
    2. Environment variable USER (Unix standard)
    3. getpass.getuser() (cross-platform)
    4. "unknown" (fallback)

    Returns:
        User identifier string
    """
    # Try explicit USER_ID first
    user = os.environ.get('USER_ID')
    if user:
        return user

    # Try standard USER environment variable
    user = os.environ.get('USER')
    if user:
        return user

    # Try getpass (cross-platform)
    try:
        user = getpass.getuser()
        if user:
            return user
    except Exception:
        pass

    # Fallback
    return "unknown"
