from flask import Blueprint, render_template, request, redirect, url_for, flash
from verifyme_app import db
from verifyme_app.models.company import Company  # Adjust path if needed

admin = Blueprint('admin', __name__)

@admin.route('/admin/add_company', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        name = request.form['name']
        reg_number = request.form['registration_number']
        new_company = Company(name=name, registration_number=reg_number)
        db.session.add(new_company)
        db.session.commit()
        flash("✅ Company added successfully!", "success")
        return redirect(url_for('admin.add_company'))

    companies = Company.query.all()
    return render_template('add_company.html', companies=companies)
