from flask import Blueprint, request, jsonify
from database import db
from models.user import Holiday
from datetime import datetime

holiday = Blueprint("holiday", __name__)

@holiday.post("/holiday/add")
def add_holiday():
    data = request.get_json()
    h = Holiday(
        company_id=data["company_id"],
        date=datetime.strptime(data["date"], "%Y-%m-%d"),
        name=data["name"]
    )
    db.session.add(h)
    db.session.commit()
    return jsonify({"message": "Holiday added"})
