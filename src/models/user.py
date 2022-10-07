from src.app import db
from src.models.collaborators import Collaborators


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(50), nullable=False)
    notes = db.relationship('Note', backref='user', lazy=True)
    collaborators = db.relationship('Note', secondary=Collaborators, lazy='subquery',
                                    backref=db.backref('users', lazy=True))
