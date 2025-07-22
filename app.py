from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Admin: View Professions
@app.route('/admin/professions')
def view_professions():
    conn = sqlite3.connect('verifyme.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM profession")
    professions = cur.fetchall()
    conn.close()
    return render_template('admin_professions.html', professions=professions)

# Admin: View Companies
@app.route('/admin/companies')
def view_companies():
    conn = sqlite3.connect('verifyme.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM companies")
    companies = cur.fetchall()
    conn.close()
    return render_template('admin_companies.html', companies=companies)

# Admin: View Houses
@app.route('/admin/houses')
def view_houses():
    conn = sqlite3.connect('verifyme.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM houses")
    houses = cur.fetchall()
    conn.close()
    return render_template('admin_houses.html', houses=houses)

# Home route (optional for testing)
@app.route('/')
def home():
    return '<h1>VerifyMe Admin Panel</h1><p>Go to /admin/professions, /admin/companies, or /admin/houses</p>'

if __name__ == '__main__':
    app.run(debug=True)
