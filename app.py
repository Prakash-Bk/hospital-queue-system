# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/register")
# def register():
#     return render_template("register.html")

# @app.route("/queue")
# def queue():
#     return render_template("queue.html")

# @app.route("/doctor")
# def doctor():
#     return render_template("doctor.html")

# @app.route("/admin")
# def admin():
#     return render_template("admin.html")

# @app.route("/login")
# def login():
#     return render_template("login.html")

# if __name__ == "__main__":
#     app.run(debug=True)



# from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, session,Response
import sqlite3
import csv #for excel sheet to export all data
from datetime import datetime#for data time 

app = Flask(__name__)
app.secret_key = "hospital123"

# Create database and table
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            phone TEXT,
            department TEXT,
            symptoms TEXT,
            status TEXT,
            date_time TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()
#for time database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE patients ADD COLUMN date_time TEXT")
except sqlite3.OperationalError:
    pass

conn.commit()
conn.close()


@app.route("/")
def home():
    return render_template("index.html")


# @app.route("/register")
# def register():
#     return render_template("register.html")
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        department = request.form["department"]
        symptoms = request.form["symptoms"]
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM patients")

        count = cursor.fetchone()[0]

        token = f"A{count + 1:03d}"
        date_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")#for date_time
        
        cursor.execute("""
INSERT INTO patients
(token, name, age, gender, phone, department, symptoms, status,date_time)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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

        print("Patient Token:", token)
        

        # print("Name:", name)
        # print("Age:", age)
        # print("Gender:", gender)
        # print("Phone:", phone)
        # print("Department:", department)
        # print("Symptoms:", symptoms)
        
        conn.commit()
        conn.close()

        # return redirect("/queue") ata samma chai jaba register hunthoe direct queue page khulthoe tara
        # aba yoe naya code ley register garna bittikai patient lai token print garna lai option dine vo 
        # queue ma enter hunu vanda paila
        return render_template(
       "token.html",
         token=token,
         name=name,
         department=department,
         date_time=date_time
) 

    return render_template("register.html")


# @app.route("/queue")
# def queue():
#     return render_template("queue.html")
@app.route("/queue")
def queue():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT token, name, age, department, status
        FROM patients
        WHERE status='Waiting'
    """)

    patients = cursor.fetchall()

    conn.close()

    return render_template("queue.html", patients=patients)


# @app.route("/doctor")
# def doctor():
#     return render_template("doctor.html")
@app.route("/doctor")
def doctor():
    if session.get("user") != "doctor":
        return redirect("/login")

    conn = sqlite3.connect("database.db")
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

    conn.close()

    return render_template(
        "doctor.html",
        patients=waiting_patients,
        current=current_patient
    )

#call  section
@app.route("/call/<int:id>")
def call_patient(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE patients
        SET status = 'In Progress'
        WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()

    return redirect("/doctor")
#call function section 
@app.route("/complete/<int:id>")
def complete_patient(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE patients
        SET status = 'Completed'
        WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()

    return redirect("/doctor")

@app.route("/skip/<int:id>")
def skip_patient(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE patients
        SET status = 'Waiting'
        WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()

    return redirect("/doctor")


# @app.route("/admin")
# def admin():
#     return render_template("admin.html")

@app.route("/admin")
def admin():
    if session.get("user") != "admin":
        return redirect("/login")
    

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    search = request.args.get("search", "")
    
    if search:

     cursor.execute("""
        SELECT id, token, name, age,  department, status,date_time
        FROM patients
        WHERE token LIKE ?
        OR name LIKE ?
        OR phone LIKE ?
        ORDER BY id
     """, (
        "%" + search + "%",
        "%" + search + "%",
        "%" + search + "%"
      ))

    else:

     cursor.execute("""
        SELECT id, token, name, age,  phone,department, symptoms, status,date_time
        FROM patients
        ORDER BY id
    """)

    patients = cursor.fetchall()

    

    # Total Patients
    cursor.execute("SELECT COUNT(*) FROM patients")
    total = cursor.fetchone()[0]

    # Waiting Patients
    cursor.execute("SELECT COUNT(*) FROM patients WHERE status='Waiting'")
    waiting = cursor.fetchone()[0]

    # In Progress Patients
    cursor.execute("SELECT COUNT(*) FROM patients WHERE status='In Progress'")
    progress = cursor.fetchone()[0]

    # Completed Patients
    cursor.execute("SELECT COUNT(*) FROM patients WHERE status='Completed'")
    completed = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "admin.html",
        patients=patients,
        total=total,
        waiting=waiting,
        progress=progress,
        completed=completed
    )
    
@app.route("/delete/<int:id>")
def delete_patient(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM patients WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/admin")

@app.route("/reset")
def reset_queue():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM patients")

    conn.commit()
    conn.close()

    return redirect("/admin")


@app.route("/export")
def export_csv():

    if session.get("user") != "admin":
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT token, name, age, gender, phone,
               department, symptoms, status, date_time
        FROM patients
    """)

    patients = cursor.fetchall()
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


# @app.route("/login")
# def login():
#     return render_template("login.html")
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # if username == "admin" and password == "admin123":
        #     return redirect("/admin")

        # elif username == "doctor" and password == "doctor123":
        #     return redirect("/doctor")
        if username == "admin" and password == "admin123":

              session["user"] = "admin"

              return redirect("/admin")

        elif username == "doctor" and password == "doctor123":

              session["user"] = "doctor"

              return redirect("/doctor")

        else:
            return "Invalid Username or Password"

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

if __name__ == "__main__":
     app.run(debug=True)
    # app.run(host="0.0.0.0", port=5000, debug=True)



    
    

