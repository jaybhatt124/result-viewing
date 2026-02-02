from flask import Flask, render_template, request
import sqlite3
import gspread
import os
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

# ---------------- LOAD ENV ----------------
load_dotenv()

TEACHER_CODE = os.getenv("TEACHER_CODE")
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")

# ---------------- APP ----------------
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# ---------------- DATABASE ----------------
def get_db():
    conn = sqlite3.connect("results.db")
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            enrollment TEXT,
            name TEXT,
            department TEXT,
            semester INTEGER,
            subject TEXT,
            marks INTEGER,
            exam_name TEXT,
            academic_year TEXT
        )
    """)
    return conn

# ---------------- GOOGLE SHEET ----------------
def read_sheet(sheet_url):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        GOOGLE_CREDENTIALS, scope
    )

    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url).sheet1

    headers = [h.strip().lower() for h in sheet.row_values(1)]
    rows = sheet.get_all_records()
    return headers, rows

# ---------------- TEACHER ----------------
@app.route("/teacher", methods=["GET", "POST"])
def teacher():
    msg = ""

    if request.method == "POST":
        code = request.form.get("code")

        # 🔐 Secure teacher code check
        if code != TEACHER_CODE:
            msg = "❌ Invalid Teacher Code"
            return render_template("teacher.html", msg=msg)

        try:
            semester = int(request.form["semester"])
            department = request.form["department"]
            sheet_url = request.form["sheet"]

            headers, rows = read_sheet(sheet_url)

            IGNORE_COLS = {
                "enrollment",
                "name",
                "department",
                "exam_name",
                "academic_year"
            }

            subjects = [h for h in headers if h not in IGNORE_COLS]

            db = get_db()
            cur = db.cursor()

            # 🔥 DELETE OLD RESULTS
            cur.execute("""
                DELETE FROM results
                WHERE department = ? AND semester = ?
            """, (department, semester))

            # 🔄 INSERT NEW RESULTS
            for row in rows:
                for sub in subjects:
                    cur.execute("""
                        INSERT INTO results
                        (enrollment, name, department, semester, subject, marks, exam_name, academic_year)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        row["enrollment"],
                        row["name"],
                        department,
                        semester,
                        sub,
                        row.get(sub, 0),
                        row["exam_name"],
                        row["academic_year"]
                    ))

            db.commit()
            msg = "✅ Result updated successfully"

        except Exception as e:
            msg = f"❌ Error: {str(e)}"

    return render_template("teacher.html", msg=msg)

# ---------------- STUDENT ----------------
@app.route("/", methods=["GET", "POST"])
def student():
    marks = {}
    info = {}

    if request.method == "POST":
        enrollment = request.form["enrollment"]
        semester = request.form["semester"]
        department = request.form["department"]

        db = get_db()
        cur = db.cursor()

        cur.execute("""
            SELECT * FROM results
            WHERE enrollment = ? AND semester = ? AND department = ?
        """, (enrollment, semester, department))

        rows = cur.fetchall()

        if rows:
            info = dict(rows[0])
            for r in rows:
                marks[r["subject"]] = r["marks"]

    return render_template("student.html", marks=marks, info=info)

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
