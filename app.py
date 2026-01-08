from flask import Flask, render_template, request
import sqlite3
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
TEACHER_CODE = "1234"

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
        "credentials.json", scope
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url).sheet1

    headers = sheet.row_values(1)
    rows = sheet.get_all_records()
    return headers, rows

# ---------------- TEACHER ----------------
@app.route("/teacher", methods=["GET", "POST"])
def teacher():
    msg = ""
    if request.method == "POST":

        if request.form["code"] != TEACHER_CODE:
            msg = "❌ Invalid Teacher Code"
        else:
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

            subjects = [h.strip() for h in headers if h.strip() not in IGNORE_COLS]

            db = get_db()
            cur = db.cursor()

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
                        row[sub],
                        row["exam_name"],
                        row["academic_year"]
                    ))

            db.commit()
            msg = "✅ Result synced successfully"

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
            WHERE enrollment=? AND semester=? AND department=?
        """, (enrollment, semester, department))

        rows = cur.fetchall()

        if rows:
            info = dict(rows[0])
            for r in rows:
                subject = r["subject"].strip()
                marks[subject] = r["marks"]

    return render_template("student.html", marks=marks, info=info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
