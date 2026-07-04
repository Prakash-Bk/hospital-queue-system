# ==========================================================
# ADMIN ROUTES
# ==========================================================

from flask import render_template, request, redirect, session, jsonify, Response
from app_instance import app
from database import get_connection


# ==========================================================
# ADMIN DASHBOARD
# ==========================================================

@app.route("/admin")
def admin():

    if session.get("user") != "admin":
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    search = request.args.get("search", "")

    if search:

        cursor.execute("""
            SELECT id, token, name, age, phone, department,
                   symptoms, status, date_time
            FROM patients
            WHERE token ILIKE %s
               OR name ILIKE %s
               OR phone ILIKE %s
            ORDER BY id
        """, (
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%"
        ))

    else:

        cursor.execute("""
            SELECT id, token, name, age, phone,
                   department, symptoms, status, date_time
            FROM patients
            ORDER BY id
        """)

    patients = cursor.fetchall()

    # Statistics
    cursor.execute("SELECT COUNT(*) FROM patients")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM patients WHERE status='Waiting'")
    waiting = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM patients WHERE status='In Progress'")
    progress = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM patients WHERE status='Completed'")
    completed = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return render_template(
        "admin.html",
        patients=patients,
        total=total,
        waiting=waiting,
        progress=progress,
        completed=completed
    )


# ==========================================================
# SEARCH PATIENTS
# ==========================================================

@app.route("/search_patients")
def search_patients():

    if session.get("user") != "admin":
        return jsonify([])

    search = request.args.get("search", "")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, token, name, age, phone,
               department, symptoms, status, date_time
        FROM patients
        WHERE token ILIKE %s
           OR name ILIKE %s
           OR phone ILIKE %s
        ORDER BY id
    """, (
        "%" + search + "%",
        "%" + search + "%",
        "%" + search + "%"
    ))

    patients = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(patients)


# ==========================================================
# DELETE PATIENT
# ==========================================================

@app.route("/delete/<int:id>")
def delete_patient(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE id=%s",
        (id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/admin")


# ==========================================================
# RESET QUEUE
# ==========================================================

@app.route("/reset")
def reset_queue():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM patients")

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/admin")


# ==========================================================
# EXPORT CSV
# ==========================================================

@app.route("/export")
def export_csv():

    if session.get("user") != "admin":
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT token, name, age, gender, phone,
               department, symptoms, status, date_time
        FROM patients
    """)

    patients = cursor.fetchall()

    cursor.close()
    conn.close()

    def generate():
        yield "Token,Name,Age,Gender,Phone,Department,Symptoms,Status,Date & Time\n"

        for patient in patients:
            yield ",".join(map(str, patient)) + "\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=patients.csv"
        }
    )