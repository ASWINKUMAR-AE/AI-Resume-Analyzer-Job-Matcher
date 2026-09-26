from functools import wraps
from flask import request
import jwt
from datetime import datetime, timezone, timedelta
from config import Config
from utils.response import api_response
from database.connection import get_db

def generate_token(user_id, email, role, name=None):
    """
    Generates a secure JWT token containing user identity and role.
    """
    payload = {
        "user_id": user_id,
        "email": email,
        "role": role,
        "name": name,
        "exp": datetime.now(timezone.utc) + timedelta(hours=Config.JWT_ACCESS_TOKEN_EXPIRES_HOURS),
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm="HS256")

def decode_token(token):
    """
    Decodes and validates a JWT token.
    """
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """
    Flask decorator that enforces valid JWT bearer token.
    Passes `current_user` dict to the wrapped endpoint.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return api_response(success=False, message="Authorization token is missing", status_code=401)
        
        parts = auth_header.split(" ")
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return api_response(success=False, message="Invalid Authorization header format. Expected 'Bearer <token>'", status_code=401)
            
        token = parts[1]
        payload = decode_token(token)
        if not payload:
            return api_response(success=False, message="Token is invalid or expired. Please log in again.", status_code=401)
            
        # Verify user still exists in database and is active
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, name, email, role, status FROM users WHERE id = %s", (payload["user_id"],))
                user = cursor.fetchone()
                if not user or user["status"] != "active":
                    return api_response(success=False, message="Account is deactivated or does not exist", status_code=403)
                    
        return f(current_user=user, *args, **kwargs)
    return decorated

def role_required(*allowed_roles):
    """
    Decorator that checks if the authenticated user possesses one of the allowed roles.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(current_user, *args, **kwargs):
            if current_user.get("role") not in allowed_roles:
                return api_response(
                    success=False,
                    message=f"Access forbidden: requires one of [{', '.join(allowed_roles)}] permissions.",
                    status_code=403
                )
            return f(current_user=current_user, *args, **kwargs)
        return decorated_function
    return decorator
