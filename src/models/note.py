from src.app import db
import src.models as models
from datetime import datetime
from src.utils.exception_wrapper import handle_error_format


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(404))
    create_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_edit_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    last_edit_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag', secondary='note_tag', back_populates='notes', cascade="all", lazy='dynamic')

    def to_json(self):
        return {
            'id': self.id,
            'text': self.text,
            'create_date': self.create_date,
            'user_id': self.user_id,
            'last_edit_date': self.last_edit_date,
            'last_edit_user_id': self.last_edit_user_id,
            'collaborators': [user.id for user in self.users],
            'tags': [models.Tag.to_json(tag) for tag in self.tags]
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_note_by_id(cls, note_id):
        return cls.query.filter_by(id=note_id).first()

    @classmethod
    def delete_note_by_id(cls, note_id):
        note = Note.get_note_by_id(note_id)

        if not note:
            return handle_error_format('Note with such id does not exist.',
                                       'Field \'noteId\' in path parameters.'), 404

        note_json = Note.to_json(note)

        for user in note.users:
            user.notes.remove(note)

        for tag in note.tags:
            tag.notes.remove(note)

        cls.query.filter_by(id=note_id).delete()
        db.session.commit()
        return note_json
