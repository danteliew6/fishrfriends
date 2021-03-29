from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#included the db elemments but have yet to do anything wthem
db= SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'WELCOMETOFISHCYCLE'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    #part of the blueprint this allows us to call pages over multiple categories 
    from .page import page
    from .auth import auth


    app.register_blueprint(page, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
