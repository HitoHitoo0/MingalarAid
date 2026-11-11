from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(190), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)
    def public(self): return {"id": self.id, "full_name": self.full_name, "email": self.email}

class AssistanceRequest(db.Model):
    __tablename__ = "assistance_requests"
    id = db.Column(db.Integer, primary_key=True)
    reference_id = db.Column(db.String(24), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(190))
    region = db.Column(db.String(100), nullable=False)
    township = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    categories = db.Column(db.Text, nullable=False)
    people_affected = db.Column(db.Integer, nullable=False)
    urgency = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    contact_method = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class VolunteerApplication(db.Model):
    __tablename__ = "volunteer_applications"
    id = db.Column(db.Integer, primary_key=True)
    reference_id = db.Column(db.String(24), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(190), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(190), nullable=False)
    available_days = db.Column(db.String(190), nullable=False)
    skills = db.Column(db.Text, nullable=False)
    interests = db.Column(db.String(255), nullable=False)
    motivation = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DemoDonation(db.Model):
    __tablename__ = "demo_donations"
    id = db.Column(db.Integer, primary_key=True)
    reference_id = db.Column(db.String(24), unique=True, nullable=False)
    donor_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(190), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    purpose = db.Column(db.String(80), nullable=False)
    payment_status = db.Column(db.String(30), default="DEMO_ONLY")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DisasterReport(db.Model):
    __tablename__ = "disaster_reports"
    id = db.Column(db.Integer, primary_key=True)
    disaster_type = db.Column(db.String(60), nullable=False)
    title = db.Column(db.String(190), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    published_date = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text, nullable=False)
    is_sample = db.Column(db.Boolean, default=True)
