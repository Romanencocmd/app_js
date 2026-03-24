from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_session import Session
from routes.auth import auth
from routes.employee import employee
from routes.attendance import attendance
from routes.leave import leave
from routes.business_trip import trip
from routes.schedule import schedule
from routes.holiday import holiday
from routes.company import company
from routes.excuse import excuse
from database import db
import os


app = Flask(__name__)


UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
CORS(
    app,
    supports_credentials=True,
    origins=["http://localhost:3000"],
    allow_headers=["Content-Type"],
    expose_headers=["Content-Type"],
)

Session(app)
db.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(employee)
app.register_blueprint(attendance)
app.register_blueprint(leave)
app.register_blueprint(trip)
app.register_blueprint(excuse)
app.register_blueprint(schedule)
app.register_blueprint(holiday)
app.register_blueprint(company)


@app.get("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
