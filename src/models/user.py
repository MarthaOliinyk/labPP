from src.app import db
from src.models import Note
from passlib.hash import pbkdf2_sha256 as sha256
from src.utils.exception_wrapper import handle_error_format


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    notes = db.relationship('Note', secondary='collaborators', backref='users')

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password_hash': self.password_hash,
            'notes': [note.id for note in self.notes],
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash_):
        return sha256.verify(password, hash_)

    @classmethod
    def get_by_username(cls, username):
        return User.query.filter_by(username=username).first()

    @classmethod
    def get_by_id(cls, userId):
        return User.query.filter_by(id=userId).first()

    @classmethod
    def delete_by_id(cls, userId):
        try:
            user = User.get_by_id(userId)

            for note in user.notes:
                Note.delete_note_by_id(note.id)

            user_json = User.to_json(user)
            User.query.filter_by(id=userId).delete()
            db.session.commit()
            return user_json
        except AttributeError:
            return handle_error_format('User with such id does not exist.',
                                       'Field \'userId\' in path parameters.'), 404
