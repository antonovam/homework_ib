from flask import Flask
from flask_server.config import Config
from flask_server.routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_routes(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5001)
