from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError
from models import db, User
auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/auth/register")
def register():
    d = request.get_json(silent=True) or {}
    name, email, password = (d.get("full_name") or "").strip(), (d.get("email") or "").strip().lower(), d.get("password") or ""
    if not name or not email or len(password) < 8:
        return jsonify(error="Enter your name, a valid email and a password of at least 8 characters."), 400
    user = User(full_name=name, email=email); user.set_password(password)
    try:
        db.session.add(user); db.session.commit()
    except IntegrityError:
        db.session.rollback(); return jsonify(error="An account with this email already exists."), 409
    login_user(user)
    return jsonify(message="Account created", user=user.public()), 201

@auth_bp.post("/auth/login")
def login():
    d = request.get_json(silent=True) or {}
    user = User.query.filter_by(email=(d.get("email") or "").strip().lower()).first()
    if not user or not user.check_password(d.get("password") or ""):
        return jsonify(error="Incorrect email or password."), 401
    login_user(user)
    return jsonify(message="Logged in", user=user.public())

@auth_bp.post("/auth/logout")
@login_required
def logout():
    logout_user(); return jsonify(message="Logged out")

@auth_bp.get("/auth/me")
def me():
    return jsonify(user=current_user.public() if current_user.is_authenticated else None)
