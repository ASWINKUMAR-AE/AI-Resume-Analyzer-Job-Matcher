import re

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

def validate_email(email):
    """
    Validates email format.
    """
    if not email or not isinstance(email, str):
        return False
    return bool(re.match(EMAIL_REGEX, email.strip()))

def validate_password(password):
    """
    Validates password strength (minimum 6 characters).
    """
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, None

def require_fields(data, required_fields):
    """
    Checks if all required fields are present and non-empty in input dictionary.
    """
    missing = []
    for field in required_fields:
        if field not in data or data[field] is None or (isinstance(data[field], str) and not data[field].strip()):
            missing.append(field)
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, None
