from flask import Blueprint, request, jsonify
from database import db
from models.user import Company
from models.user import Department
from models.user import Position

company = Blueprint("company", __name__)

@company.post("/company/create")
def create_company():
    data = request.get_json()
    c = Company(
        name=data["name"],
        address=data.get("address"),
        timezone=data.get("timezone", "UTC")
    )
    db.session.add(c)
    db.session.commit()
    return jsonify({"message": "Company created", "id": c.id})


@company.post("/department/create")
def create_department():
    data = request.get_json()
    d = Department(
        company_id=data["company_id"],
        name=data["name"]
    )
    db.session.add(d)
    db.session.commit()
    return jsonify({"message": "Department created"})


@company.post("/position/create")
def create_position():
    data = request.get_json()
    p = Position(
        department_id=data["department_id"],
        name=data["name"]
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({"message": "Position created"})
