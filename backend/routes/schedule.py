from flask import Blueprint
from database import db
from models.user import WorkSchedule
from datetime import time

schedule = Blueprint("schedule", __name__)

def create_default_schedule(company_id):
    existing = WorkSchedule.query.filter_by(company_id=company_id).first()
    if existing:
        return 

    if company_id == 1:
        default = [
            (0, "08:00", "16:00"),
            (1, "08:00", "16:00"),
            (2, "08:00", "16:00"),
            (3, "08:00", "16:00"),
            (4, "08:00", "16:00"),
        ]

    elif company_id == 2:
        default = [
            (0, "17:00", "23:00"),
            (1, "17:00", "23:00"),
            (2, "17:00", "23:00"),
            (3, "17:00", "23:00"),
            (4, "17:00", "23:00"),
        ]

    else:
        return  

    for weekday, start, end in default:
        ws = WorkSchedule(
            company_id=company_id,
            weekday=weekday,
            start_time=time.fromisoformat(start),
            end_time=time.fromisoformat(end)
        )
        db.session.add(ws)
    db.session.commit()

