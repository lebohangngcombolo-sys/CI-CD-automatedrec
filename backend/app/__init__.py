from flask import Flask, jsonify
import os
from .extensions import (
    db, jwt, mail, cloudinary_client, mongo_client,
    migrate, cors, bcrypt, oauth, limiter
)
from .models import *
from .routes import auth, admin_routes, candidate_routes, ai_routes, mfa_routes, sso_routes, analytics_routes
from .config import config  # <-- import the config dictionary

def create_app(config_name=None):
    app = Flask(__name__)

    # Pick config dynamically
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "production").lower()

    # Use dictionary to fetch the config class
    app.config.from_object(config.get(config_name, config['production']))

    # ---------------- Initialize Extensions ----------------
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    oauth.init_app(app)
    bcrypt.init_app(app)
    cloudinary_client.init_app(app)
    limiter.init_app(app)
    cors.init_app(
        app,
        origins=["*"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
        supports_credentials=True,
    )

    # ---------------- Register Blueprints ----------------
    auth.init_auth_routes(app)
    app.register_blueprint(admin_routes.admin_bp, url_prefix="/api/admin")
    app.register_blueprint(candidate_routes.candidate_bp, url_prefix="/api/candidate")
    app.register_blueprint(ai_routes.ai_bp)
    app.register_blueprint(mfa_routes.mfa_bp, url_prefix="/api/auth")
    app.register_blueprint(analytics_routes.analytics_bp, url_prefix="/api")
    sso_routes.register_sso_provider(app)
    app.register_blueprint(sso_routes.sso_bp)

    # ---------------- Health Check Route ----------------
    @app.route("/api/health")
    def health():
        return {"status": "ok", "message": "Recruitment backend is running!"}, 200
    
    # ---------------- Version Endpoint ----------------
    @app.route("/version")
    def version():
        return jsonify({"version": os.getenv("APP_VERSION", "unknown")})

    return app
