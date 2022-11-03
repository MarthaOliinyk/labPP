from src.app import db


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    notes = db.relationship('Note', secondary='note_tag', back_populates='tags', lazy='joined')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    @classmethod
    def get_all(cls):
        try:
            tags = Tag.query.all()
            return tags
        except AttributeError:
            return {'error': f'There aren\'t any tags available'}, 404

    @classmethod
    def get_by_id(cls, id):
        tag = Tag.query.filter_by(id=id).first()
        if not tag:
            return {'error': 'No such tag'}, 404
        return tag

    @classmethod
    def get_by_name(cls, name):
        tag = Tag.query.filter_by(name=name).first()

        if not tag:
            new_tag = Tag(name=name)

            db.session.add(new_tag)
            db.session.commit()

            return new_tag

        return tag
