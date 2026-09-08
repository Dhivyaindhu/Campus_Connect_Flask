# Workbook Chapter 04 — SQLAlchemy ORM & Models
# Workbook Chapter 08 — to_dict() controls the exact JSON shape sent to React

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(60), nullable=False)
    members = db.Column(db.Integer, default=0)
    description = db.Column(db.Text, default="")

    events = db.relationship("Event", backref="club", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "members": self.members,
            "description": self.description,
        }


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    seats_left = db.Column(db.Integer, default=0)
    club_id = db.Column(db.Integer, db.ForeignKey("club.id"), nullable=True)

    def to_dict(self):
        # Keys here are camelCase on purpose — the React app's eventsApi.js
        # reads event.seatsLeft, event.clubId directly. Renaming happens
        # once, here, so nothing on the frontend needs to change.
        return {
            "id": self.id,
            "title": self.title,
            "date": self.date,
            "seatsLeft": self.seats_left,
            "clubId": self.club_id,
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}
