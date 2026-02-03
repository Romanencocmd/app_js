from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import os 
from werkzeug.utils import secure_filename
import smtplib 
from email.mime.text import MIMEText 
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"

CORS(
    app,
    supports_credentials=True,
    origins=["http://localhost:3000"],
    allow_headers=["Content-Type"],
    expose_headers=["Content-Type"]
)

UPLOAD_FOLDER = "uploads" 
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
Session(app)


db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6), nullable=True)


@app.post("/register")
def register():
    data = request.get_json()
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"})
 
    user = User(email=email, username=username, password=password, is_verified=False)
    db.session.add(user)
    db.session.commit()

    code = str(random.randint(100000, 999999))
    user.verification_code = code
    db.session.commit()
    send_verification_email(email, code)

    return jsonify({"message": "Verification code sent"})

def send_verification_email(email, code): 
    msg = MIMEText(f"Your verification code is: {code}")
    msg["Subject"] = "Registration Verification Code"
    msg["From"] = "noreply@nexly.com"
    msg["To"] = email
    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 587) as server:
        server.login("f91be611769ede", "46e0e1dd095b70")
        server.send_message(msg)


@app.post("/verify") 
def verify(): 
    data = request.get_json() 
    email = data.get("email") 
    code = data.get("code") 
    user = User.query.filter_by(email=email).first() 
    if not user: 
        return jsonify({"error": "User not found"})
    
    if user.verification_code == code: 
        user.is_verified = True 
        user.verification_code = None 
        db.session.commit() 
        return jsonify({"message": "Email verified successfully"})
    
    return jsonify({"error": "Invalid verification code"})
    

@app.post("/login")
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or user.password != password:
        return jsonify({"error": "Invalid credentials"})

    session["user_id"] = user.id 
    return jsonify({"message": "Logged in"})


@app.post("/logout")
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logged out"})

@app.post("/upload-avatar") 
def upload_avatar(): 
    if "avatar" not in request.files: 
        return jsonify({"error": "No file"}) 
    
    file = request.files["avatar"] 
    if file.filename == "": 
        return jsonify({"error": "Empty filename"})
         
    user_id = session.get("user_id") 
    if not user_id: 
        return jsonify({"error": "Unauthorized"})
    
    filename = secure_filename(file.filename) 
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename) 
    file.save(filepath) 
    
    user = User.query.get(user_id) 
    user.avatar = f"/uploads/{filename}" 
    db.session.commit() 

    return jsonify({"avatar": user.avatar})

@app.get("/uploads/<path:filename>") 
def uploaded_file(filename): 
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.get("/dashboard")
def me():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"})

    user = User.query.get(user_id)
    return jsonify({
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "avatar": user.avatar,
    })


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)