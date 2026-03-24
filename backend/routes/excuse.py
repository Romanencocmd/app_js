from flask import Blueprint, request, jsonify, session
from database import db
from models.user import ExcuseRequest
from datetime import datetime

excuse = Blueprint("excuse", __name__)

@excuse.post("/excuse/request")
def request_excuse():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"})
    data = request.get_json()
    req = ExcuseRequest(
        employee_id=user_id,
        date=datetime.strptime(data["date"], "%Y-%m-%d"),
        reason=data["reason"]
    )
    db.session.add(req)
    db.session.commit()
    return jsonify({"message": "Excuse request submitted"})
