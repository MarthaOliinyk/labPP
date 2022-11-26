from src.app import app, auth
from src.models import Tag
from src.models import Note
from src.models import User
from datetime import datetime
from flask_restful import reqparse
from werkzeug.exceptions import NotFound
from src.utils.exception_wrapper import handle_server_exception
from src.utils.exception_wrapper import handle_error_format


@app.route('/note/create', methods=['POST'])
@auth.login_required()
@handle_server_exception
def create_note():
    parser = reqparse.RequestParser()

    parser.add_argument('text', help='username cannot be blank', required=True)
    parser.add_argument('tags', type=str, action='append', help='Tags cannot be left blank', required=True)
    parser.add_argument('userId', help='fullname cannot be blank', required=True)

    data = parser.parse_args()
    text = data['text']
    user_id = data['userId']

    user = User.get_by_id(user_id)

    if not user:
        return handle_error_format('User with such id does not exist.',
                                   'Field \'userId\' in path parameters.'), 404

    tags = []
    for name in data['tags']:
        tag = Tag.get_by_name(name)
        tags.append(tag)

    note = Note(
        text=text,
        create_date=datetime.now(),
        user_id=user_id,
        last_edit_user_id=user_id
    )

    for tag in tags:
        note.tags.append(tag)

    note.users.append(user)
    note.save_to_db()

    return Note.to_json(note)


@app.route('/note', methods=['GET'])
@handle_server_exception
def get_notes():
    tag = reqparse.request.args.get('tag', default=None, type=str)
    page = reqparse.request.args.get('page', default=1, type=int)
    limit = reqparse.request.args.get('limit', default=5, type=int)

    try:
        if tag:
            tag_entity = Tag.get_by_name(tag)
            notes = Note.query.join(Note.tags).filter(Tag.id.in_([tag_entity.id])).paginate(page=page, per_page=limit)
        else:
            notes = Note.query.paginate(page=page, per_page=limit)
        return {
            'items': [Note.to_json(note) for note in notes],
            'page': page,
            'limit': limit
        }
    except NotFound:
        return handle_error_format('There aren\'t any records on this page.', 'Field \'page\' in query parameters.'), 404


@app.route('/note/<noteId>', methods=['GET'])
@handle_server_exception
def get_note_by_id(noteId: int):
    note = Note.get_note_by_id(noteId)

    if not note:
        return handle_error_format('Note with such id does not exist.',
                                   'Field \'noteId\' in path parameters.'), 404

    return Note.to_json(note)


@app.route('/note/<noteId>', methods=['PUT'])
@auth.login_required()
@handle_server_exception
def update_note_by_id(noteId: int):
    parser = reqparse.RequestParser()

    parser.add_argument('text', help='username cannot be blank', required=True)
    parser.add_argument('tags', type=int, action='append', help='Tags cannot be left blank', required=True)
    parser.add_argument('users', type=int, action='append', help='Users cannot be left blank', required=True)
    parser.add_argument('lastEditDate', type=str, help='lastEditDate cannot be blank', required=True)
    parser.add_argument('lastEditUserId', help='lastEditUserId cannot be blank', required=True)

    data = parser.parse_args()
    text = data['text']
    last_edit_date = data['lastEditDate']
    last_edit_user_id = data['lastEditUserId']

    tags = []
    for tag_id in data['tags']:
        tag = Tag.get_by_id(tag_id)
        tags.append(tag)

    users = []
    for user_id in data['users']:
        user = User.get_by_id(user_id)

        if not user:
            return handle_error_format('User with such id does not exist.',
                                       'Field \'users\' in path parameters.'), 404

        users.append(user)

    note = Note.get_note_by_id(noteId)

    if not note:
        return handle_error_format('Note with such id does not exist.',
                                   'Field \'noteId\' in path parameters.'), 404

    if not User.get_by_id(last_edit_user_id):
        return handle_error_format('User with such id does not exist.',
                                   'Field \'last_edit_user_id\' in path parameters.'), 404

    note.text = text
    note.last_edit_date = last_edit_date
    note.last_edit_user_id = last_edit_user_id
    note.tags = tags
    note.users = users
    Note.save_to_db(note)

    return Note.to_json(note)


@app.route('/note/<noteId>', methods=['DELETE'])
@auth.login_required()
@handle_server_exception
def delete_note_by_id(noteId: int):
    return Note.delete_note_by_id(noteId)
