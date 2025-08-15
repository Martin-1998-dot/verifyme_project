from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# In-memory storage for each category
data_store = {
    "company": [],
    "profession": [],
    "stand": [],
    "house": [],
    "dna": [],
    "ancestral": []
}

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    category = request.args.get('category', '')
    if request.method == 'POST':
        category_post = request.form['category']
        entry = {k: v for k, v in request.form.items() if k != 'category'}
        data_store[category_post].append(entry)
        return redirect(f"/?category={category_post}")

    return render_template('dashboard.html', data_store=data_store, selected_category=category)

if __name__ == '__main__':
    app.run(debug=True)
