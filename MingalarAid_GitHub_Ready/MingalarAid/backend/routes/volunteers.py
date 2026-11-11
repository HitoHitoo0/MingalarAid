from flask import Blueprint, request, jsonify
from models import db, VolunteerApplication
import secrets
volunteers_bp = Blueprint("volunteers", __name__)

@volunteers_bp.post("/volunteers")
def apply():
    d = request.get_json(silent=True) or {}
    required = ["full_name","email","phone","age","location","available_days","skills","interests","motivation"]
    if any(not str(d.get(k,"")).strip() for k in required):
        return jsonify(error="Please complete all required volunteer fields."), 400
    try: age = int(d["age"])
    except (TypeError, ValueError): return jsonify(error="Please enter a valid age."), 400
    if age < 13 or age > 100: return jsonify(error="Please enter a valid age."), 400
    ref = "MA-VOL-" + secrets.token_hex(4).upper()
    row = VolunteerApplication(reference_id=ref, full_name=d["full_name"], email=d["email"].lower(),
        phone=d["phone"], age=age, location=d["location"], available_days=d["available_days"],
        skills=d["skills"], interests=d["interests"], motivation=d["motivation"])
    db.session.add(row); db.session.commit()
    return jsonify(message="Application received", reference_id=ref), 201
