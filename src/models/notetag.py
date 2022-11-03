from src.app import db


class NoteTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))

    def to_json(self):
        return {
            'id': self.id,
            'tag_id': self.tag_id,
            'note_id': self.note_id,
        }
