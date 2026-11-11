from flask import Blueprint, jsonify
from models import DisasterReport
disasters_bp = Blueprint("disasters", __name__)

@disasters_bp.get("/disasters")
def list_disasters():
    rows = DisasterReport.query.order_by(DisasterReport.id.desc()).all()
    return jsonify(items=[{"id":r.id,"disaster_type":r.disaster_type,"title":r.title,"region":r.region,
        "published_date":r.published_date,"description":r.description,"is_sample":r.is_sample} for r in rows])
