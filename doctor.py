# ==========================================================
# DOCTOR ROUTES
# ==========================================================

from flask import render_template, redirect, session
from app_instance import app
from database import get_connection


# ==========================================================
# DOCTOR DASHBOARD
# ==========================================================

@app.route("/doctor")
def doctor():

    if session.get("user") != "doctor":
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    # Waiting patients
    cursor.execute("""
        SELECT id, token, name, age, department, status
        FROM patients
        WHERE status='Waiting'
        ORDER BY id
    """)
    waiting_patients = cursor.fetchall()

    # Current patient
    cursor.execute("""
        SELECT id, token, name, age, department, status
        FROM patients
        WHERE status='In Progress'
        LIMIT 1
    """)
    current_patient = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "doctor.html",
        patients=waiting_patients,
        current=current_patient
    )


# ==========================================================
# CALL PATIENT
# ==========================================================

@app.route("/call/<int:id>")
def call_patient(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE patients
        SET status='In Progress'
        WHERE id=%s
    """, (id,))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/doctor")


# ==========================================================
# COMPLETE PATIENT
# ==========================================================

@app.route("/complete/<int:id>")
def complete_patient(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE patients
        SET status='Completed'
        WHERE id=%s
    """, (id,))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/doctor")


# ==========================================================
# SKIP PATIENT
# ==========================================================

@app.route("/skip/<int:id>")
def skip_patient(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE patients
        SET status='Waiting'
        WHERE id=%s
    """, (id,))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/doctor")