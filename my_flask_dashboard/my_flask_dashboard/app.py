from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# In-memory database for demo
companies = [
    {"name": "M&M Holding", "reg_no": "Lc12345", "status": "Active"}
]

# Dashboard route
@app.route('/')
def dashboard():
    return render_template('dashboard.html', companies=companies)

# Add company route
@app.route('/add_company', methods=['POST'])
def add_company():
    name = request.form['name']
    reg_no = request.form['registration_number']
    companies.append({"name": name, "reg_no": reg_no, "status": "Active"})
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
