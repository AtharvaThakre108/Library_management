from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .routes.Librarian import librarian_bp  # Import librarian routes
from .routes.Library import library_bp  # Import library routes
from config import Config  # A separate file for configuration settings

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    """
    Factory function to create and configure the Flask app.
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    
    # Register Blueprints
    app.register_blueprint(library_bp, url_prefix='/api')  # Library user routes
    app.register_blueprint(librarian_bp, url_prefix='/api')  # Librarian routes
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
