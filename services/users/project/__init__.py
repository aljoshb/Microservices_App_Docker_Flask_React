import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# Instantiate the database
db = SQLAlchemy()

# Create an instance of the Flask toolbar
toolbar = DebugToolbarExtension()

# Data migration
migrate = Migrate()

# Bcrypt for password hashing extension
bcrypt = Bcrypt()


def create_app(script_info=None):

    # Instantiate the app
    app = Flask(__name__)

    # Enable CORS on all routes from any domain
    CORS(app)

    # Set configuration
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # Set up extensions
    db.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Register the blueprints
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)
    from project.api.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
