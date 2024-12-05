from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from app.models import User

# Initialize JWT
app.config["JWT_SECRET_KEY"] = "your-secret-key"  # Change this to a strong secret key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

# Helper function for generating tokens
def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return create_access_token(identity={"user_id": user.id, "username": user.username})
    return None
