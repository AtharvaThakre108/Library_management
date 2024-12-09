import os
from datetime import timedelta

class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.environ.get("SECRET_KEY", "accessToken")  # Secure your secret key
    FLASK_ENV = os.environ.get("FLASK_ENV", "development")  # 'development' or 'production'
    DEBUG = True if FLASK_ENV == "development" else False

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///site.db")  # Default SQLite database
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask-SQLAlchemy modification tracking

    # JWT settings
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your-jwt-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Set token expiration time
    
    # CORS (Cross-Origin Resource Sharing) settings (if needed)
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")  # Allows all domains by default

