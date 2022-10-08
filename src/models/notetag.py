from src.app import db


class NoteTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))
