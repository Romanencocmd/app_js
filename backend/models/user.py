from database import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))
    position_id = db.Column(db.Integer, db.ForeignKey("position.id"))
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255))
    role = db.Column(db.String(20), default="employee") 
    is_verified = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6))
    hire_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    attendance = db.relationship("Attendance", backref="employee", lazy=True)
    leave_requests = db.relationship("LeaveRequest", backref="employee", lazy=True)
    excuse_requests = db.relationship("ExcuseRequest", backref="employee", lazy=True)
    business_trips = db.relationship("BusinessTrip", backref="employee", lazy=True)

class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    employees = db.relationship("User", backref="position", lazy=True)

class WorkSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    weekday = db.Column(db.Integer, nullable=False) 
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

class LeaveRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(120), db.ForeignKey("user.username"), nullable=False)
    request_date = db.Column(db.Date, nullable=False)   

class Holiday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(120), nullable=False)

class ExcuseRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(120), db.ForeignKey("user.username"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.String(255), nullable=False)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    positions = db.relationship("Position", backref="department", lazy=True)
    employees = db.relationship("User", backref="department", lazy=True)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255))
    timezone = db.Column(db.String(50), default="UTC")
    departments = db.relationship("Department", backref="company", lazy=True)
    employees = db.relationship("User", backref="company", lazy=True)

class BusinessTrip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(120), db.ForeignKey("user.username"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    destination = db.Column(db.String(255), nullable=False)
    purpose = db.Column(db.String(255), nullable=False)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(120), db.ForeignKey("user.username"), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    check_in_time = db.Column(db.Time)
    check_out_time = db.Column(db.Time)
    is_late = db.Column(db.Boolean, default=False)
    is_absent = db.Column(db.Boolean, default=False)

class ShiftCalendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(120), db.ForeignKey("user.username"), nullable=False)
    day = db.Column(db.Integer, nullable=False)
    weekday = db.Column(db.String(20), nullable=False)
    shift = db.Column(db.String(20), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)

