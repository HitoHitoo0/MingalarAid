from flask import Blueprint, request, jsonify
from models import db, AssistanceRequest
import secrets, json
assistance_bp = Blueprint("assistance", __name__)

@assistance_bp.post("/assistance")
def create_request():
    d = request.get_json(silent=True) or {}
    required = ["full_name","phone","region","township","address","people_affected","urgency","description"]
    if any(not str(d.get(k,"")).strip() for k in required) or not d.get("categories"):
        return jsonify(error="Please complete all required fields and select at least one assistance category."), 400
    try: people = int(d["people_affected"])
    except (TypeError, ValueError): return jsonify(error="Number of affected people must be a valid number."), 400
    if people < 1: return jsonify(error="Number of affected people must be at least 1."), 400
    ref = "MA-REQ-" + secrets.token_hex(4).upper()
    row = AssistanceRequest(reference_id=ref, full_name=d["full_name"].strip(), phone=d["phone"].strip(),
        email=(d.get("email") or "").strip(), region=d["region"], township=d["township"], address=d["address"],
        categories=json.dumps(d["categories"]), people_affected=people, urgency=d["urgency"],
        description=d["description"], contact_method=d.get("contact_method","Phone call"))
    db.session.add(row); db.session.commit()
    return jsonify(message="Request received", reference_id=ref), 201
