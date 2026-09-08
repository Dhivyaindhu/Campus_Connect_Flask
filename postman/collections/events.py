# Same pattern as clubs.py, applied to the events resource.
# Workbook Chapter 12 — @jwt_required() protects the write endpoints,
# matching the React app's expectation that creating/deleting needs login.

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Event

events_bp = Blueprint("events", __name__)


@events_bp.route("/events", methods=["GET"])
def list_events():
    events = Event.query.all()
    return jsonify([e.to_dict() for e in events])


@events_bp.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    return jsonify(event.to_dict())


@events_bp.route("/events", methods=["POST"])
@jwt_required()
def create_event():
    data = request.get_json() or {}
    required = ["title", "date"]
    missing = [f for f in required if f not in data or not str(data[f]).strip()]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    event = Event(
        title=data["title"],
        date=data["date"],
        seats_left=data.get("seatsLeft", data.get("capacity", 0)),
        club_id=data.get("clubId"),
    )
    db.session.add(event)
    db.session.commit()
    return jsonify(event.to_dict()), 201


@events_bp.route("/events/<int:event_id>", methods=["PATCH"])
@jwt_required()
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    data = request.get_json() or {}

    if "title" in data:
        event.title = data["title"]
    if "date" in data:
        event.date = data["date"]
    if "seatsLeft" in data:
        event.seats_left = data["seatsLeft"]

    db.session.commit()
    return jsonify(event.to_dict())


@events_bp.route("/events/<int:event_id>", methods=["DELETE"])
@jwt_required()
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return "", 204
