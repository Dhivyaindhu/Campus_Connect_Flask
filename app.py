# Workbook Chapters 02, 05, 09, 11, 12 — the app entry point.
# Registers extensions, blueprints, and consistent JSON error handlers.

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from models import db
from routes.clubs import clubs_bp
from routes.events import events_bp
from routes.auth import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)
    CORS(app, origins=app.config["CORS_ORIGINS"])

    app.register_blueprint(clubs_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(auth_bp)

    @app.route("/")
    def home():
        return jsonify({
            "message": "CampusConnect API is running.",
            "endpoints": ["/clubs", "/events", "/login", "/signup"],
        })

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
