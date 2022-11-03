from src.app import db


class Collaborators(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'note_id': self.note_id,
        }
