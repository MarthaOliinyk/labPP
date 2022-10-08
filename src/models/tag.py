from src.app import db
from src.models.notetag import NoteTag


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    tags = db.relationship('Note', secondary=NoteTag, lazy='subquery',
                           backref=db.backref('tags', lazy=True))
