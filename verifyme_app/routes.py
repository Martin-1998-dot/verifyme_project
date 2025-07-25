from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def dashboard():
    return render_template('admin_dashboard.html')

@main.route('/admin/cars')
def cars():
    return render_template('admin_cars.html')

@main.route('/admin/houses')
def houses():
    return render_template('admin_houses.html')

@main.route('/admin/professions')
def professions():
    return render_template('admin_professions.html')

@main.route('/admin/companies')
def companies():
    return render_template('admin_companies.html')

@main.route('/admin/login')
def login():
    return render_template('admin_login.html')
