from flask import Flask
from verifyme_app.extensions import db
from verifyme_app.routes.admin_routes import admin

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///verifyme.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(admin, url_prefix='/admin')

    @app.route('/')
    def home():
        return "Hello, Flask is working!"

    return app
