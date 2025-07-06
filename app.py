import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.secret_key = os.environ.get("SESSION_SECRET", "hawaii-realty-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///hawaii_realty.db")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["UPLOAD_FOLDER"] = "static/uploads"
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size
    
    # Proxy fix for deployment
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Login manager configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))
    
    # Create upload directory
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    
    with app.app_context():
        # Import models and routes
        import models
        import routes
        
        # Create tables
        db.create_all()
        
        # Register routes
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(routes.auth_bp)
        app.register_blueprint(routes.property_bp)
        app.register_blueprint(routes.realtor_bp)
        app.register_blueprint(routes.booking_bp)
        app.register_blueprint(routes.crm_bp)
    
    return app

# Create the application instance
app = create_app()
