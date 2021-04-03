from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'not-so-secret-007'
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:pgsuper007@localhost:5432/cars_api"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #get rid of annoying warning

    db.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
