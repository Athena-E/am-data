from flask import Flask
from flask_socketio import SocketIO, emit

from scripts.db.utils import init_db

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    from app.routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    from app.routes.home import home_bp
    app.register_blueprint(home_bp)

    #* Add socket methods
    socketio.init_app(app)

    return app
