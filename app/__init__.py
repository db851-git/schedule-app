from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import config_by_name

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app(config_name='dev'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        from .routes.main import main_bp
        from .routes.api import api_bp
        from .routes.errors import errors_bp
        from .routes.auth import auth_bp  # New auth blueprint

        app.register_blueprint(main_bp)
        app.register_blueprint(api_bp, url_prefix='/api/v1')
        app.register_blueprint(errors_bp)
        app.register_blueprint(auth_bp, url_prefix='/auth') # Registered here

        db.create_all()

    return app