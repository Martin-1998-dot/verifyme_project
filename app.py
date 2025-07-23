from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'verifyme.db')

@app.route('/admin/professions', methods=['GET', 'POST'])
def admin_professions():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if request.method == 'POST':
        id_number = request.form['id_number']
        license_number = request.form.get('license_number', '')
        c.execute("INSERT INTO profession_ids (id_number, license_number) VALUES (?, ?)", (id_number, license_number))
        conn.commit()

    c.execute("SELECT id_number, license_number FROM profession_ids")
    professions = c.fetchall()
    conn.close()

    return render_template('admin_professions.html', professions=professions)

# Keep this line at the end of your app.py
if __name__ == '__main__':
    app.run(debug=True)
