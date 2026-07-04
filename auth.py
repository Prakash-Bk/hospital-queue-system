# ==========================================================
# AUTHENTICATION ROUTES
# ==========================================================

from flask import render_template, request, redirect, session
from app_instance import app

# ==========================================================
# LOGIN
# ==========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "Admin@2026!":
            session["user"] = "admin"
            return redirect("/admin")

        elif username == "doctor" and password == "Doctor@2026!":
            session["user"] = "doctor"
            return redirect("/doctor")

        else:
            return "Invalid Username or Password"

    return render_template("login.html")


# ==========================================================
# LOGOUT
# ==========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")