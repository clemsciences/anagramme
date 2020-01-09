from flask import Flask, jsonify, Blueprint

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]

main = Blueprint('main', __name__)

from app.routes import *


def create_app():
    app = Flask(__name__)
    # app.config.from_object(Config)
    app.secret_key = "anagramme"

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({"success": False, "message": "Unknown page"})

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({"success": False, "message": "Internal error"})

    app.register_blueprint(main)

    return app
