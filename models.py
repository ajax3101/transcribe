from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from datetime import datetime

db = SQLAlchemy()

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    duration = db.Column(db.Integer, nullable=True)
    mode = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<File {self.name}>'
