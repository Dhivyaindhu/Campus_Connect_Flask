# Workbook Chapter 06 — Seeding and Querying Data
# Run once to populate a fresh database with starter data.

from app import app
from models import db, Club, Event, User

with app.app_context():
    db.create_all()

    if not Club.query.first():
        robotics = Club(name="Robotics Club", category="Tech", members=42,
                         description="Building autonomous bots for the annual Tirupur Robotics Meet.")
        literary = Club(name="Literary Circle", category="Arts", members=28,
                         description="Weekly readings, open mics, and a termly anthology.")
        dance = Club(name="Dance Crew", category="Cultural", members=35,
                     description="Contemporary and classical fusion performances.")
        sports = Club(name="Sports Committee", category="Sports", members=60,
                      description="Organizes inter-department tournaments all year.")

        db.session.add_all([robotics, literary, dance, sports])
        db.session.commit()

        db.session.add_all([
            Event(title="Hackathon 2026", date="2026-03-14", seats_left=12, club_id=robotics.id),
            Event(title="Open Mic Night", date="2026-03-20", seats_left=0, club_id=literary.id),
            Event(title="Annual Dance Showcase", date="2026-04-02", seats_left=5, club_id=dance.id),
        ])
        db.session.commit()
        print("Seeded clubs and events.")
    else:
        print("Clubs already exist — skipping club/event seed.")

    if not User.query.filter_by(email="student@campusconnect.edu").first():
        demo_user = User(name="Indhupriya", email="student@campusconnect.edu")
        demo_user.set_password("demo1234")
        db.session.add(demo_user)
        db.session.commit()
        print("Seeded demo user: student@campusconnect.edu / demo1234")
    else:
        print("Demo user already exists — skipping.")

    print("Done.")
