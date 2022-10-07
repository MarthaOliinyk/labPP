from src.app import db
from src.models.collaborators import Collaborators
from src.models.notetag import NoteTag


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(404))
    create_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_edit_date = db.Column(db.DateTime, nullable=False)
    last_edit_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    collaborators = db.relationship('User', secondary=Collaborators, lazy='subquery',
                                    backref=db.backref('notes', lazy=True))
    tags = db.relationship('Tag', secondary=NoteTag, lazy='subquery',
                           backref=db.backref('notes', lazy=True))
