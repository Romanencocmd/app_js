import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_TYPE = "filesystem"
    SESSION_COOKIE_NAME = "session"
    SESSION_COOKIE_HTTPONLY = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"

    UPLOAD_FOLDER = "uploads"
    CORS_ORIGINS = ["http://localhost:3000"]
