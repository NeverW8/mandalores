from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def create_app():
    from .app import app
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
