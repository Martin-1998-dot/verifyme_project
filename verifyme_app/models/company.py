from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True)
    registered = db.Column(db.String(100))
    date_added = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Company {self.name}>"

