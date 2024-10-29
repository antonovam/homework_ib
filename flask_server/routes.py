from flask import Flask
from flask_server.config import Config
from flask_server.v2.routes import v2 as v2_blueprint  # Import the v2 Blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # Register the v2 Blueprint with the URL prefix `/api/v2`
    app.register_blueprint(v2_blueprint, url_prefix='/api/v2')

    return app
