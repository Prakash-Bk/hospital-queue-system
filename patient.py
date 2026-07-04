# ==========================================================
# PATIENT ROUTES
# ==========================================================

from flask import render_template, request
from app_instance import app
from database import get_connection
from datetime import datetime
@app.route("/")
def home():
    
    return render_template("index.html")


# ==========================================================
# PATIENT REGISTRATION
# ==========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        department = request.form["department"]
        symptoms = request.form["symptoms"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM patients")
        count = cursor.fetchone()[0]

        token = f"A{count + 1:03d}"
        date_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")
        
        print("Age from form:", age)
        print(type(age))
        

        cursor.execute("""
            INSERT INTO patients
            (token, name, age, gender, phone, department, symptoms, status, date_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            token,
            name,
            age,
            gender,
            phone,
            department,
            symptoms,
            "Waiting",
            date_time
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return render_template(
            "token.html",
            token=token,
            name=name,
            department=department,
            date_time=date_time
        )

    return render_template("register.html")


# ==========================================================
# QUEUE PAGE
# ==========================================================

@app.route("/queue")
def queue():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT token, name, age, department, status
        FROM patients
        WHERE status='Waiting'
        ORDER BY id
    """)

    patients = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("queue.html", patients=patients)