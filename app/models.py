from datetime import datetime
from app import db


class SoundClip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    start_time = db.Column(db.String(8), nullable=False)
    stop_time = db.Column(db.String(8), nullable=False)
    status = db.Column(db.String(50), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String(255))

    def __repr__(self):
        return f'<SoundClip {self.id}>'
