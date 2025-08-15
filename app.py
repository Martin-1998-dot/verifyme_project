<<<<<<< HEAD
from verifyme_app import create_app

app = create_app()

=======
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DB_NAME = "app_data.db"

# Helper to get DB connection
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ------------------ COMPANIES ------------------
@app.route("/companies")
def view_companies():
    conn = get_db_connection()
    companies = conn.execute("SELECT * FROM companies").fetchall()
    conn.close()
    return render_template("admin.html", data=companies, table="companies")

@app.route("/companies/add", methods=["POST"])
def add_company():
    name = request.form["name"]
    reg_number = request.form["registration_number"]
    status = request.form["status"]
    conn = get_db_connection()
    conn.execute("INSERT INTO companies (name, registration_number, status) VALUES (?, ?, ?)",
                 (name, reg_number, status))
    conn.commit()
    conn.close()
    return redirect("/companies")

@app.route("/companies/delete/<int:id>")
def delete_company(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM companies WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/companies")

# ------------------ RUN APP ------------------
>>>>>>> 5385e3a (Initial commit: FastAPI company dashboard)
if __name__ == "__main__":
    app.run(debug=True)
