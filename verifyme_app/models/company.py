from verifyme_app.extensions import db

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    registration_number = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Company {self.name}>'
