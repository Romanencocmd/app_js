class Config:
    SECRET_KEY = "supersecretkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_TYPE = "filesystem"
    SESSION_COOKIE_NAME = "session"
    SESSION_COOKIE_HTTPONLY = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"

    UPLOAD_FOLDER = "uploads"
    CORS_ORIGINS = ["http://localhost:3000"]
