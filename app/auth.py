from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from models.user import User
from app import db  
from flask import current_app

# ========================
# JWT Configuration
# ========================

# Set JWT configurations in your app
current_app.config["JWT_SECRET_KEY"] = "Secret_key"  # Use a strong, environment-specific secret key
current_app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(current_app)

# ========================
# Helper Functions
# ========================

def authenticate_user(email, password):
    """
    Authenticate a user and generate a JWT token if the credentials are valid.
    :param email: User's email
    :param password: User's password
    :return: JWT token if authentication is successful, or an error message with status code
    """
    # Fetch user by email
    user = User.query.filter_by(email=email).first()
    if not user:
        return {"error": "User does not exist."}, 404

    # Verify password
    if not check_password_hash(user.password, password):
        return {"error": "Invalid credentials."}, 401

    # Generate JWT token with user details as identity
    token = create_access_token(identity={"user_id": user.id, "email": user.email, "is_admin": user.is_admin})
    return {"token": token}, 200


def register_user(email, password, is_admin=False):
    """
    Register a new user by creating a hashed password and saving to the database.
    :param email: New user's email
    :param password: New user's password
    :param is_admin: Boolean flag to indicate admin privileges
    :return: The created user object or an error message with status code
    """
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {"error": "User with this email already exists."}, 400

    # Hash password
    hashed_password = generate_password_hash(password)

    # Create and save the new user
    new_user = User(email=email, password=hashed_password, is_admin=is_admin)
    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201
    except Exception as e:
        db.session.rollback()
        return {"error": f"An error occurred: {str(e)}"}, 500


@jwt.user_identity_loader
def user_identity_lookup(user):
    """
    Specify what data should be used as the JWT identity.
    """
    return {"user_id": user["user_id"], "email": user["email"], "is_admin": user["is_admin"]}


@jwt.user_lookup_loader
def user_lookup_callback(jwt_header, jwt_data):
    """
    Fetch the user from the database using the identity from the JWT.
    """
    identity = jwt_data["sub"]
    return User.query.get(identity["user_id"])
