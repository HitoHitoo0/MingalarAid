# MingalarAid

A responsive disaster-relief coordination demo for Myanmar, based on the supplied Figma PDF.

## Features
- Responsive Home, About, Disaster Updates, Request Assistance, Donation, Volunteer and Login/Register sections.
- Dark / Light mode (saved in browser local storage).
- Flask JSON APIs.
- MySQL persistence through SQLAlchemy + PyMySQL.
- User registration/login with hashed passwords and session cookies.
- Assistance request submission and reference number.
- Volunteer application submission and reference number.
- Demo donation record and demo receipt. **No payment gateway or real money transfer is connected.**
- Sample disaster reports clearly marked as historical/demo content, not real-time alerts.

## Project structure
```text
MingalarAid/
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   ├── js/app.js
│   └── assets/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   └── routes/
├── database/
│   ├── schema.sql
│   └── sample_data.sql
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Run locally

### 1. Requirements
Install Python 3.10+ and MySQL Server 8.0+. Make sure MySQL is running.

### 2. Create the database
The Flask app auto-creates all tables and seeds sample disaster reports on startup, but the database itself must exist first:
```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS mingalaraid CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```
Alternatively, run `database/schema.sql` manually if you prefer.

### 3. Set up Python environment
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```
Open `.env` and set `DATABASE_URL` with your MySQL credentials. The format is:
```
mysql+pymysql://root:YOUR_PASSWORD@127.0.0.1:3306/mingalaraid
```
If your MySQL root has no password, leave it empty: `mysql+pymysql://root:@127.0.0.1:3306/mingalaraid`. Change `SECRET_KEY` to a long random value. Do not upload `.env` to GitHub.

### 4. Start the app
```bash
python backend/app.py
```
Open http://127.0.0.1:5000

The frontend is served by Flask, so the API requests use the same origin — no CORS configuration needed for local development

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | API health check |
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | Login |
| POST | `/api/auth/logout` | Logout |
| GET | `/api/auth/me` | Current session |
| GET | `/api/disasters` | List sample reports |
| POST | `/api/assistance` | Submit assistance request |
| POST | `/api/volunteers` | Submit volunteer application |
| POST | `/api/donations/demo` | Record demo donation |

## Important notes
- Disaster report cards are sample/historical records. This project does not connect to a verified real-time disaster data feed.
- Demo donations only create a database record with `DEMO_ONLY` status. They do not process payments.
- This is a university project starter, not a monitored emergency response service. Do not enter sensitive identity or banking information.
- Before any public deployment, set secure environment variables, restrict CORS, add CSRF protection and rate limiting, validate uploads if added, use HTTPS, and review privacy/security requirements.
- Database tables are auto-created by Flask-SQLAlchemy on startup (`db.create_all()`). Sample disaster reports are also seeded automatically. The `database/schema.sql` and `sample_data.sql` files are provided for reference or manual setup.
