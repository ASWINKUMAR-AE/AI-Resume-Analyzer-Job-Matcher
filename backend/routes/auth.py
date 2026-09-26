from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from database.connection import get_db
from utils.response import api_response
from utils.auth_middleware import generate_token, token_required
from utils.validators import validate_email, validate_password, require_fields

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Registers a new user (student or company).
    Automatically creates the corresponding profile table record.
    """
    data = request.get_json() or {}
    role = data.get("role", "student").lower()
    
    if role not in ["student", "company"]:
        return api_response(success=False, message="Invalid role. Must be 'student' or 'company'.", status_code=400)
        
    valid, err = require_fields(data, ["name", "email", "password"])
    if not valid:
        return api_response(success=False, message=err, status_code=400)
        
    email = data["email"].strip().lower()
    if not validate_email(email):
        return api_response(success=False, message="Invalid email address format.", status_code=400)
        
    valid_pw, pw_err = validate_password(data["password"])
    if not valid_pw:
        return api_response(success=False, message=pw_err, status_code=400)

    with get_db() as conn:
        with conn.cursor() as cursor:
            # Check duplicate email
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return api_response(success=False, message="An account with this email already exists.", status_code=409)

            pw_hash = generate_password_hash(data["password"])
            cursor.execute(
                """
                INSERT INTO users (name, email, password_hash, role, status)
                VALUES (%s, %s, %s, %s, 'active')
                """,
                (data["name"].strip(), email, pw_hash, role)
            )
            user_id = cursor.lastrowid

            # Create respective profile
            if role == "student":
                cursor.execute(
                    """
                    INSERT INTO student_profiles (user_id, phone, location, college, degree, graduation_year, experience, bio)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        user_id,
                        data.get("phone", ""),
                        data.get("location", ""),
                        data.get("college", ""),
                        data.get("degree", ""),
                        data.get("graduation_year") or None,
                        data.get("experience", "Entry Level"),
                        data.get("bio", "")
                    )
                )
            elif role == "company":
                cursor.execute(
                    """
                    INSERT INTO company_profiles (user_id, company_name, company_email, phone, website, industry, location, description)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        user_id,
                        data.get("company_name", data["name"].strip()),
                        email,
                        data.get("phone", ""),
                        data.get("website", ""),
                        data.get("industry", ""),
                        data.get("location", ""),
                        data.get("description", "")
                    )
                )

    token = generate_token(user_id, email, role, data["name"].strip())
    return api_response(
        success=True,
        message=f"{role.capitalize()} registration successful!",
        data={
            "token": token,
            "user": {
                "id": user_id,
                "name": data["name"].strip(),
                "email": email,
                "role": role
            }
        },
        status_code=201
    )

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticates user and returns JWT token and user details.
    """
    data = request.get_json() or {}
    valid, err = require_fields(data, ["email", "password"])
    if not valid:
        return api_response(success=False, message=err, status_code=400)

    email = data["email"].strip().lower()

    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, email, password_hash, role, status, must_change_password
                FROM users WHERE email = %s
                """,
                (email,)
            )
            user = cursor.fetchone()

    if not user or not check_password_hash(user["password_hash"], data["password"]):
        return api_response(success=False, message="Invalid email or password.", status_code=401)

    if user["status"] != "active":
        return api_response(success=False, message="Your account is inactive or pending approval.", status_code=403)

    token = generate_token(user["id"], user["email"], user["role"], user["name"])
    
    return api_response(
        success=True,
        message="Login successful!",
        data={
            "token": token,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"],
                "must_change_password": bool(user["must_change_password"])
            }
        }
    )

@auth_bp.route("/me", methods=["GET"])
@token_required
def get_current_user_profile(current_user):
    """
    Returns full profile information for the authenticated user.
    """
    user_id = current_user["id"]
    role = current_user["role"]
    profile_data = {}

    with get_db() as conn:
        with conn.cursor() as cursor:
            if role == "student":
                cursor.execute("SELECT * FROM student_profiles WHERE user_id = %s", (user_id,))
                profile_data = cursor.fetchone() or {}
            elif role == "company":
                cursor.execute("SELECT * FROM company_profiles WHERE user_id = %s", (user_id,))
                profile_data = cursor.fetchone() or {}

    return api_response(
        success=True,
        data={
            "user": current_user,
            "profile": profile_data
        }
    )

@auth_bp.route("/logout", methods=["POST"])
@token_required
def logout(current_user):
    """
    Stateless JWT logout endpoint.
    """
    return api_response(success=True, message="Successfully logged out.")

@auth_bp.route("/change-password", methods=["POST"])
@token_required
def change_password(current_user):
    """
    Changes user's password.
    """
    data = request.get_json() or {}
    valid, err = require_fields(data, ["old_password", "new_password"])
    if not valid:
        return api_response(success=False, message=err, status_code=400)

    valid_pw, pw_err = validate_password(data["new_password"])
    if not valid_pw:
        return api_response(success=False, message=pw_err, status_code=400)

    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT password_hash FROM users WHERE id = %s", (current_user["id"],))
            user = cursor.fetchone()
            if not user or not check_password_hash(user["password_hash"], data["old_password"]):
                return api_response(success=False, message="Incorrect current password.", status_code=400)

            new_hash = generate_password_hash(data["new_password"])
            cursor.execute(
                "UPDATE users SET password_hash = %s, must_change_password = 0 WHERE id = %s",
                (new_hash, current_user["id"])
            )

    return api_response(success=True, message="Password updated successfully.")
