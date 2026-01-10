from flask import Flask, jsonify
import os
from dotenv import load_dotenv   # ✅ ADD THIS

load_dotenv() 
from .extensions import (
    db, jwt, mail, cloudinary_client, mongo_client,
    migrate, cors, bcrypt, oauth, limiter, socketio
)

from .models import *
from .routes import auth, admin_routes, candidate_routes, ai_routes, mfa_routes, sso_routes, analytics_routes, chat_routes, offer_routes  # import sso_routes
from .websocket_handler import register_websocket_handlers
from .config import config  # <-- import the config dictionary

def create_app(config_name=None):
    app = Flask(__name__)

    # Pick config dynamically
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "production").lower()

    # Use dictionary to fetch the config class
    app.config.from_object(config.get(config_name, config['production']))
    
    # ---------------- Custom Env Config ----------------
    app.config['GOOGLE_CALENDAR_CREDENTIALS_PATH'] = os.getenv(
        'GOOGLE_CALENDAR_CREDENTIALS_PATH'
    )
    app.config['GOOGLE_CALENDAR_TOKEN_PATH'] = os.getenv(
        'GOOGLE_CALENDAR_TOKEN_PATH'
    )


    # ---------------- Initialize Extensions ----------------
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    oauth.init_app(app)
    bcrypt.init_app(app)
    cloudinary_client.init_app(app)
    limiter.init_app(app)
    socketio.init_app(
        app,
        cors_allowed_origins="*",
        async_mode='eventlet',  # or 'gevent' depending on your setup
        manage_session=False,
        ping_timeout=60,
        ping_interval=25
    )
    cors.init_app(
        app,
        origins=["*"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
        supports_credentials=True,
    )

    # ---------------- Register Blueprints ----------------
    auth.init_auth_routes(app)  # existing auth routes
    app.register_blueprint(admin_routes.admin_bp, url_prefix="/api/admin")
    app.register_blueprint(candidate_routes.candidate_bp, url_prefix="/api/candidate")
    app.register_blueprint(ai_routes.ai_bp)
    app.register_blueprint(mfa_routes.mfa_bp, url_prefix="/api/auth")  # MFA routes
    app.register_blueprint(analytics_routes.analytics_bp, url_prefix="/api")
    app.register_blueprint(chat_routes.chat_bp, url_prefix="/api/chat")
    app.register_blueprint(offer_routes.offer_bp, url_prefix="/api/offer")

    # ---------------- Register SSO Blueprint ----------------
    sso_routes.register_sso_provider(app)      # initialize Auth0 / SSO provider
    app.register_blueprint(sso_routes.sso_bp)  # SSO routes

    # ---------------- Register WebSocket Handlers ----------------
    register_websocket_handlers(app)
    
    # ---------------- Health Check Route ----------------
    @app.route("/api/health")
    def health():
        return {"status": "ok", "message": "Recruitment backend is running!"}, 200
    
    # ---------------- Version Endpoint ----------------
    @app.route("/version")
    def version():
        return jsonify({"version": os.getenv("APP_VERSION", "unknown")})

    return app
