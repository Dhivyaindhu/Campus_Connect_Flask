# Workbook Chapter 12 — configuration read from environment variables
# (mirrors the React project's .env pattern from the API workbook)

import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'campusconnect.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-secret-change-me")
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "https://campus-connect-react-mu.vercel.app/").split(",")
