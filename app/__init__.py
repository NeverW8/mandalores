import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
if os.path.exists('.envrc'):
    load_dotenv('.envrc')
else:
    load_dotenv()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    return app


def init_app():
    app = create_app()
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))
            app.logger.info("Connected to the PostgreSQL database.")
        except Exception as e:
            app.logger.error(f"Failed to connect to the PostgreSQL database: {e}")
    return app
