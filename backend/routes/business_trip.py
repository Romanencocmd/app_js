from flask import Blueprint, request, jsonify, session
from database import db
from models.user import BusinessTrip
from datetime import datetime

trip = Blueprint("trip", __name__)

@trip.post("/trip/request")
def request_trip():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"})
    data = request.get_json()
    req = BusinessTrip(
        employee_id=user_id,
        start_date=datetime.strptime(data["start_date"], "%Y-%m-%d"),
        end_date=datetime.strptime(data["end_date"], "%Y-%m-%d"),
        destination=data["destination"],
        purpose=data["purpose"]
    )
    db.session.add(req)
    db.session.commit()
    return jsonify({"message": "Business trip request submitted"})
