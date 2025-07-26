from flask import Blueprint, render_template, request, redirect, url_for
from verifyme_app import db
from verifyme_app.models import Company

admin_companies_bp = Blueprint('admin_companies', __name__)

@admin_companies_bp.route('/add_company', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        name = request.form['name']
        reg_number = request.form['registration_number']
        status = request.form['status']

        new_company = Company(name=name, registration_number=reg_number, status=status)
        db.session.add(new_company)
        db.session.commit()

        return redirect(url_for('admin_companies.list_companies'))

    return render_template('admin_add_company.html')


@admin_companies_bp.route('/companies')
def list_companies():
    companies = Company.query.all()
    return render_template('admin_companies.html', companies=companies)

