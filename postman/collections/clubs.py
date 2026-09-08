# Workbook Chapter 07 — GET & POST
# Workbook Chapter 09 — Blueprints
# Workbook Chapter 10 — PATCH, DELETE, validation
# Workbook Chapter 11 — consistent error responses

from flask import Blueprint, request, jsonify
from models import db, Club

clubs_bp = Blueprint("clubs", __name__)


@clubs_bp.route("/clubs", methods=["GET"])
def list_clubs():
    clubs = Club.query.all()
    return jsonify([c.to_dict() for c in clubs])


@clubs_bp.route("/clubs/<int:club_id>", methods=["GET"])
def get_club(club_id):
    club = Club.query.get_or_404(club_id)
    return jsonify(club.to_dict())


@clubs_bp.route("/clubs", methods=["POST"])
def create_club():
    data = request.get_json() or {}
    required = ["name", "category"]
    missing = [f for f in required if f not in data or not str(data[f]).strip()]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    club = Club(
        name=data["name"],
        category=data["category"],
        members=data.get("members", 0),
        description=data.get("description", ""),
    )
    db.session.add(club)
    db.session.commit()
    return jsonify(club.to_dict()), 201


@clubs_bp.route("/clubs/<int:club_id>", methods=["PATCH"])
def update_club(club_id):
    club = Club.query.get_or_404(club_id)
    data = request.get_json() or {}

    if "name" in data:
        club.name = data["name"]
    if "category" in data:
        club.category = data["category"]
    if "members" in data:
        club.members = data["members"]
    if "description" in data:
        club.description = data["description"]

    db.session.commit()
    return jsonify(club.to_dict())


@clubs_bp.route("/clubs/<int:club_id>", methods=["DELETE"])
def delete_club(club_id):
    club = Club.query.get_or_404(club_id)
    db.session.delete(club)
    db.session.commit()
    return "", 204
