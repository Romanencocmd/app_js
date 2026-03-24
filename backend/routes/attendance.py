from flask import Blueprint, jsonify, session
from database import db
from models.user import Attendance
from models.user import User
from models.user import WorkSchedule
from datetime import datetime, date

attendance = Blueprint("attendance", __name__)

@attendance.post("/check-in")
def check_in():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"})
    today = date.today()
    record = Attendance.query.filter_by(employee_id=user_id, date=today).first()
    if record and record.check_in_time:
        return jsonify({"error": "Already checked in"})
    now = datetime.now().time()
    schedule = WorkSchedule.query.filter_by(
        company_id=User.query.get(user_id).company_id,
        weekday=today.weekday()
    ).first()
    is_late = False
    if schedule and now > schedule.start_time:
        is_late = True
    new_record = Attendance(
        employee_id=user_id,
        date=today,
        check_in_time=now,
        is_late=is_late
    )
    db.session.add(new_record)
    db.session.commit()
    return jsonify({"message": "Checked in", "late": is_late})


@attendance.post("/check-out")
def check_out():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"})
    today = date.today()
    record = Attendance.query.filter_by(employee_id=user_id, date=today).first()
    if not record:
        return jsonify({"error": "You didn't check in"})
    if record.check_out_time:
        return jsonify({"error": "Already checked out"})
    record.check_out_time = datetime.now().time()
    db.session.commit()
    return jsonify({"message": "Checked out"})


@attendance.get("/report/today")
def report_today():
    today = date.today()
    records = Attendance.query.filter_by(date=today).all()
    result = []
    for r in records:
        result.append({
            "employee_id": r.employee_id,
            "check_in": str(r.check_in_time),
            "check_out": str(r.check_out_time),
            "late": r.is_late,
            "absent": r.is_absent
        })
    return jsonify(result)
