from flask import Blueprint, request, jsonify
from models import db, DemoDonation
import secrets
donations_bp = Blueprint("donations", __name__)

@donations_bp.post("/donations/demo")
def demo_donation():
    d = request.get_json(silent=True) or {}
    name, email, purpose = (d.get("donor_name") or "").strip(), (d.get("email") or "").strip().lower(), d.get("purpose","General Relief")
    try: amount = int(d.get("amount", 0))
    except (TypeError, ValueError): amount = 0
    if not name or "@" not in email or amount < 1000 or amount > 100000000:
        return jsonify(error="Enter a name, valid email and an amount between 1,000 and 100,000,000 MMK."), 400
    ref = "MA-DEMO-" + secrets.token_hex(4).upper()
    row = DemoDonation(reference_id=ref, donor_name=name, email=email, amount=amount, purpose=purpose, payment_status="DEMO_ONLY")
    db.session.add(row); db.session.commit()
    return jsonify(message="Demo donation recorded. No payment was processed.", reference_id=ref, amount=amount, payment_status="DEMO_ONLY"), 201
