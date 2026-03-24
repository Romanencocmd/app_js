from flask import Blueprint, request, jsonify, session
from database import db
from models.user import User
import os
from werkzeug.utils import secure_filename
from flask import current_app

employee = Blueprint("employee", __name__)

@employee.post("/upload-avatar")
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
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)
    user = User.query.get(user_id)
    user.avatar = f"/uploads/{filename}"
    db.session.commit()
    return jsonify({"avatar": user.avatar})


@employee.get("/dashboard")
def dashboard():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"})
    user = User.query.get(user_id)
    return jsonify({
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "avatar": user.avatar,
        "role": user.role,
    })
