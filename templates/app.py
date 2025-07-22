@app.route('/admin/houses', methods=['GET', 'POST'])
@admin_required
def admin_houses():
    conn = sqlite3.connect('verifyme.db')
    cur = conn.cursor()

    if request.method == 'POST':
        stand_number = request.form.get('stand_number')
        owner_id = request.form.get('owner_id')
        location = request.form.get('location')

        if stand_number and owner_id and location:
            try:
                cur.execute("INSERT INTO properties (stand_number, owner_id, location) VALUES (?, ?, ?)",
                            (stand_number, owner_id, location))
                conn.commit()
            except sqlite3.IntegrityError:
                # Handle duplicate stand_number or other constraints
                pass

    cur.execute("SELECT * FROM properties")
    houses = cur.fetchall()
    conn.close()
    return render_template('admin_houses.html', houses=houses)
