from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager
from config import Config
from models import db, DisasterReport
from routes.auth import auth_bp
from routes.assistance import assistance_bp
from routes.volunteers import volunteers_bp
from routes.donations import donations_bp
from routes.disasters import disasters_bp
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
SAMPLE_DISASTERS = [
    {"disaster_type": "FLOOD", "title": "Flooding across Myanmar", "region": "Myanmar",
     "published_date": "27 Sep 2024", "description": "Illustrative overview of flood-related needs across multiple states and regions. This is historical sample content, not live conditions."},
    {"disaster_type": "FLOOD", "title": "Flood impacts across central Myanmar", "region": "Mandalay Region",
     "published_date": "22 Sep 2024", "description": "Sample report showing how local access and essential supplies could be presented. Not a current situation report."},
    {"disaster_type": "FLOOD", "title": "Sittaung River flooding in Taungoo", "region": "Bago Region",
     "published_date": "18 Sep 2024", "description": "Illustrative township-level update with space for local context and relief information. Not live data."},
]
def create_app():
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)
    CORS(app, supports_credentials=True, origins=app.config.get("CORS_ORIGINS", "*"))
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    with app.app_context():
        db.create_all()
        if DisasterReport.query.count() == 0:
            for item in SAMPLE_DISASTERS:
                db.session.add(DisasterReport(**item, is_sample=True))
            db.session.commit()

    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return db.session.get(User, int(user_id))

    @app.get("/")
    def index():
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.get("/<path:path>")
    def frontend_files(path):
        candidate = FRONTEND_DIR / path
        if candidate.is_file():
            return send_from_directory(FRONTEND_DIR, path)
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.get("/api/health")
    def health():
        return jsonify(status="ok", service="MingalarAid API")

    for blueprint in (auth_bp, assistance_bp, volunteers_bp, donations_bp, disasters_bp):
        app.register_blueprint(blueprint, url_prefix="/api")

    @app.errorhandler(404)
    def not_found(_):
        return jsonify(error="Resource not found"), 404

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=app.config.get("DEBUG", False))
