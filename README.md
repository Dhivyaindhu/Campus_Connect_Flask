 HEAD
# CampusConnect — Flask REST API

The real backend for the CampusConnect React project — companion to the
**Flask & REST APIs for CampusConnect** workbook. Replaces the earlier
json-server mock with a genuine Flask + SQLAlchemy + JWT API.

Tested end-to-end: GET/POST/PATCH/DELETE on `/clubs` and `/events`, real
JWT login, 401 on bad credentials, and CORS scoped to the React dev server.

## 0. Before you start — install Python

You need **Python 3.10 or later**. Check:


python3 --version

If missing, install from https://python.org (Windows/Mac) or your
package manager (Linux).


## 1. Unzip and enter the project folder

cd path/to/campusconnect-flask


## 2. Create and activate a virtual environment

**Mac/Linux:**

python3 -m venv venv
source venv/bin/activate

**Windows (Command Prompt):**
python -m venv venv
venv\Scripts\activate
```

Your terminal prompt should now show `(venv)` at the start of the line.

## 3. Install dependencies

pip install -r requirements.txt

## 4. Set up your environment file

cp .env.example .env

Windows Command Prompt:

copy .env.example .env

The defaults work as-is for local development — no editing required
unless you're deploying somewhere.

## 5. Seed the database

Creates `campusconnect.db` (SQLite) and fills it with starter clubs,
events, and a demo user:

python seed.py

You should see:
Seeded clubs and events.
Seeded demo user: student@campusconnect.edu / demo1234
Done.


## 6. Run the server

python app.py

 * Running on http://127.0.0.1:5000
Leave this running. Test it directly in your browser:
`http://localhost:5000/clubs`

## 7. Connect it to the React project

In the **React** project's `.env` file (from the earlier API Integration
project), change:

VITE_API_BASE_URL=http://localhost:4000


to:

VITE_API_BASE_URL=http://localhost:5000

Then run the React app as usual (`npm run dev`) — you no longer need
`npm run server` (json-server); this Flask API replaces it entirely, with
no changes needed to `clubsApi.js`, `eventsApi.js`, or `authApi.js`.

Log in with:
- **Email:** `student@campusconnect.edu`
- **Password:** `demo1234`

## Testing the API directly with curl

curl http://localhost:5000/clubs

curl -X POST http://localhost:5000/clubs -H "Content-Type: application/json" \
  -d "{\"name\":\"Chess Club\",\"category\":\"Games\",\"members\":15}"

curl -X POST http://localhost:5000/login -H "Content-Type: application/json" \
  -d "{\"email\":\"student@campusconnect.edu\",\"password\":\"demo1234\"}"

Copy the `token` from the login response, then use it on protected routes:

curl -X POST http://localhost:5000/events -H "Content-Type: application/json" \
  -H "Authorization: Bearer PASTE_TOKEN_HERE" \
  -d "{\"title\":\"New Event\",\"date\":\"2026-06-01\",\"seatsLeft\":20}"

## Using real migrations instead of seed.py's db.create_all()

`seed.py` calls `db.create_all()` directly for simplicity. For a project
that will keep evolving its models, switch to Flask-Migrate instead:
flask db init
flask db migrate -m "create club, event, user tables"
flask db upgrade

## Chapter → File Map

| Chapter | Concept | File(s) |
|---|---|---|
| 01–02 | What is Flask, first route | `app.py` |
| 03 | Routes, methods, request data | `routes/clubs.py`, `routes/events.py` |
| 04 | SQLAlchemy models | `models.py` |
| 05 | Migrations | see note above; `Migrate(app, db)` in `app.py` |
| 06 | Seeding & querying | `seed.py` |
| 07 | GET & POST endpoints | `routes/clubs.py` |
| 08 | Serialization | `to_dict()` methods in `models.py` |
| 09 | Blueprints | `routes/` folder, registered in `app.py` |
| 10 | PATCH, DELETE, validation | `routes/clubs.py`, `routes/events.py` |
| 11 | Error handling & status codes | `app.errorhandler` in `app.py` |
| 12 | CORS, JWT, connecting to React | `config.py`, `routes/auth.py`, `app.py` |

## Project structure
campusconnect-flask/
├─ app.py              # entry point — creates and configures the app
├─ config.py            # environment-driven settings
├─ models.py            # Club, Event, User (SQLAlchemy models)
├─ seed.py              # starter data script
├─ routes/
│  ├─ clubs.py          # /clubs endpoints
│  ├─ events.py         # /events endpoints (write ops require JWT)
│  └─ auth.py           # /login, /signup
├─ requirements.txt
├─ .env.example
└─ .gitignore
# Campus_Connect_Flask
Backend Web Server
eaabbbf84298dd2680ed82a6fd069835a6775dd1
