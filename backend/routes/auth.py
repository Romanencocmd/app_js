from flask import Blueprint, request, jsonify, session
from routes.schedule import create_default_schedule
from database import db
from models.user import User, WorkSchedule
from models.user import Attendance, LeaveRequest, ShiftCalendar
from utils.email_service import send_verification_email
from datetime import datetime, timedelta
import random

auth = Blueprint("auth", __name__)


@auth.post("/register")
def register():
    data = request.get_json()
    email = data["email"]
    username = data["username"]
    password = data["password"]
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"})
    user = User(email=email, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    code = str(random.randint(100000, 999999))
    user.verification_code = code
    db.session.commit()
    send_verification_email(email, code)
    return jsonify({"message": "Verification code sent"})

@auth.post("/verify")
def verify():
    data = request.get_json()
    email = data["email"]
    code = data["code"]
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"})
    if user.verification_code == code:
        user.is_verified = True
        user.verification_code = None
        db.session.commit()
        return jsonify({"message": "Email verified successfully"})
    return jsonify({"error": "Invalid verification code"})

@auth.post("/login")
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email=email).first()
    if not user or user.password != password:
        return jsonify({"error": "Invalid credentials"})
    if not user.is_verified:
        return jsonify({"error": "Email not verified"})
    session["user_id"] = user.id
    return jsonify({"message": "Logged in"})


@auth.get("/dashboard")
def dashboard():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"})
    user = User.query.get(user_id)
    return jsonify({
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "avatar": user.avatar
    })

@auth.post("/set-company")
def set_company():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    data = request.get_json()
    company_id = data.get("company_id")
    if not company_id:
        return jsonify({"error": "company_id is required"})
    user.company_id = company_id
    db.session.commit()
    create_default_schedule(company_id)
    return jsonify({"message": "Company saved"})


@auth.post("/get-schedule")
def get_schedule():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    if not user.company_id:
        return jsonify({"schedule": "No company selected"})
    schedules = WorkSchedule.query.filter_by(company_id=user.company_id).all()
    if not schedules:
        return jsonify({"schedule": "No schedule found"})
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    text = "Work schedule:\n"
    for s in schedules:
        text += f"{weekdays[s.weekday]}: {s.start_time} - {s.end_time}\n"
    return jsonify({"schedule": text})


@auth.post("/get-shift-calendar")
def get_shift_calendar():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    if not user.company_id:
        return jsonify({"calendar": []})
    today = datetime.today()
    year = today.year
    month = today.month
    ShiftCalendar.query.filter_by(employee_name=user.username, month=month, year=year).delete()
    next_month = today.replace(day=28) + timedelta(days=4)
    last_day = (next_month - timedelta(days=next_month.day)).day
    calendar = []
    for day in range(1, last_day + 1):
        date = datetime(year, month, day)

        if user.company_id == 1: 
            shift = "09:00 - 18:00" if day % 2 == 0 else "12:00 - 21:00"
        elif user.company_id == 2: 
            shift = "17:00 - 23:00" if day % 2 == 0 else "14:00 - 23:00"
        else:
            shift = "Unknown"

        entry = ShiftCalendar(employee_name=user.username, day=day, weekday=date.strftime("%A"), shift=shift, month=month, year=year)
        db.session.add(entry)
        calendar.append({
            "day": day,
            "weekday": date.strftime("%A"),
            "shift": shift
        })
    db.session.commit()
    return jsonify({"calendar": calendar})


@auth.post("/request-leave")
def request_leave():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    leave = LeaveRequest(employee_name=user.username, request_date=datetime.utcnow())
    db.session.add(leave)
    db.session.commit()
    return jsonify({"message": "Leave request saved"})


@auth.post("/check-in")
def check_in():
    user_id = session.get("user_id")
    now = datetime.utcnow()
    user = User.query.get(user_id)
    attendance = Attendance(employee_name=user.username, date=now.date(), check_in_time=now.time())
    db.session.add(attendance)
    db.session.commit()
    return jsonify({"message": "Checked in"})


@auth.post("/absent")
def mark_absent():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    attendance = Attendance(employee_name=user.username, check_in=None, check_out=None)
    attendance.is_absent = True
    db.session.add(attendance)
    db.session.commit()
    return jsonify({"message": "Marked as absent"})

@auth.post("/late")
def mark_late():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    attendance = Attendance(employee_name=user.username, check_in=datetime.utcnow(), check_out=None)
    if attendance.check_in.time() > datetime.strptime("09:00", "%H:%M").time():
        attendance.is_late = True
    db.session.add(attendance)
    db.session.commit()
    return jsonify({"message": "Marked as late"})

@auth.post("/check-out")
def check_out():
    user_id = session.get("user_id")
    now = datetime.utcnow()
    user = User.query.get(user_id)
    attendance = Attendance.query.filter_by(employee_name=user.username, date=now.date()).first()
    if not attendance:
        return jsonify({"error": "No check-in found"})
    attendance.check_out_time = now.time()  
    db.session.commit()
    return jsonify({"message": "Checked out"})


@auth.post("/logout")
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logged out"})
