from flask import Blueprint, request, jsonify, session
from database import db
from models.user import LeaveRequest
from datetime import datetime

leave = Blueprint("leave", __name__)

@leave.post("/leave/request")
def request_leave():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"})
    data = request.get_json()
    req = LeaveRequest(
        employee_id=user_id,
        start_date=datetime.strptime(data["start_date"], "%Y-%m-%d"),
        end_date=datetime.strptime(data["end_date"], "%Y-%m-%d"),
        type=data["type"]
    )
    db.session.add(req)
    db.session.commit()
    return jsonify({"message": "Leave request submitted"})


@leave.get("/leave/my")
def my_leave_requests():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"})
    requests = LeaveRequest.query.filter_by(employee_id=user_id).all()
    return jsonify([
        {
            "id": r.id,
            "start": str(r.start_date),
            "end": str(r.end_date),
            "type": r.type,
            "status": r.status
        }
        for r in requests
    ])
