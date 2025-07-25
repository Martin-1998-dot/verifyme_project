@admin.route('/add_company', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        name = request.form.get('name')
        registration_number = request.form.get('registration_number')

        if not name or not registration_number:
            flash('Please provide both company name and registration number.')
            return redirect(url_for('admin.add_company'))

        new_company = Company(name=name, registration_number=registration_number)
        db.session.add(new_company)
        db.session.commit()

        flash('Company added successfully!', 'success')
        return redirect(url_for('admin.view_companies'))

    # For GET request, pass company=None
    return render_template('add_company.html', company=None)
