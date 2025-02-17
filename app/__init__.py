from flask import Flask
from scripts.db.utils import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    init_db()

    from app.routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    from app.routes.home import home_bp
    app.register_blueprint(home_bp)

    return app
