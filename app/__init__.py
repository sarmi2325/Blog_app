#Import required Flask extensions and modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ckeditor import CKEditor
import os

#Initialize Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()
ckeditor = CKEditor()

def create_app():
    # Create Flask application instance with static folder configuration
    app = Flask(__name__, static_folder='static')
    # Configure application settings
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    app.config['CKEDITOR_PKG_TYPE'] = 'mini'

    # Initialize Flask extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    ckeditor.init_app(app)
    
     # Import User model for login manager
    from .model import User
    
     # User loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register blueprints
    from .routes.auth import auth as auth_blueprint
    from .routes.blog import blog as blog_blueprint
    from .routes.main import main 

    # Register blueprints with the application
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(blog_blueprint)
    app.register_blueprint(main)

    return app

    