import datetime
from unittest import TestCase, mock
from undecorated import undecorated
from src.models import User, Note, Role, Tag
from src.resourses import delete_note_by_id, update_note_by_id, get_note_by_id, get_notes, create_note


class TestAccounts(TestCase):

    def setUp(self) -> None:
        self.user = User(
            username='username',
            first_name='first_name',
            last_name='last_name',
            email='email',
            password='password'
        )

        self.tag = Tag(
            id=1,
            name="text"
        )

        self.note = Note(
            text='text',
            user_id=1,
        )

        self.user_role = Role(
            id=1,
            name='user'
        )

        self.admin_role = Role(
            id=2,
            name='admin'
        )

        self.note_json_create = {
            "text": "Cool text",
            "tags": ["text"],
            "userId": 1
        }

        self.note_json_update = {
            "text": "Changed text",
            "tags": ["text", "new tag"],
            "users": [1, 2],
            "lastEditUserId": 1
        }

        self.user.notes.append(self.note)
        self.user.roles.append(self.user_role)
        self.note.tags.append(self.tag)

    @mock.patch('src.models.Note.save_to_db')
    @mock.patch('src.models.Tag.get_by_name')
    @mock.patch('src.models.user.User.get_by_id')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_create_note(self, mock_request_parser, mock_get_by_id, mock_get_by_name, mock_save_to_db):
        mock_request_parser.return_value = self.note_json_create
        mock_get_by_id.return_value = self.user
        mock_get_by_name.return_value = self.tag
        mock_save_to_db.return_value = True

        expected = {'collaborators': [None],
                    'create_date': datetime.datetime.now(),
                    'id': None,
                    'last_edit_date': None,
                    'last_edit_user_id': 1,
                    'tags': [{'id': 1, 'name': 'text'}],
                    'text': 'Cool text',
                    'user_id': 1}

        undecorated_create_note = undecorated(create_note)
        result = undecorated_create_note()

        self.assertEqual(expected, result)

    @mock.patch('src.models.Note.save_to_db')
    @mock.patch('src.models.Tag.get_by_name')
    @mock.patch('src.models.user.User.get_by_id')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_create_note_with_invalid_user(self, mock_request_parser, mock_get_by_id, mock_get_by_name,
                                           mock_save_to_db):
        mock_request_parser.return_value = self.note_json_create
        mock_get_by_id.return_value = None
        mock_get_by_name.return_value = self.tag
        mock_save_to_db.return_value = True

        undecorated_create_note = undecorated(create_note)
        result = undecorated_create_note()

        self.assertEqual(({'errors': [{'message': 'User with such id does not exist.',
                                       'source': "Field 'userId' in path parameters."}],
                           'traceId': result[0].get('traceId')}, 404), result)

    @mock.patch('src.models.Note.save_to_db')
    @mock.patch('src.models.Note.get_note_by_id')
    def test_get_note_by_id(self, mock_get_by_id, mock_save_to_db):
        mock_get_by_id.return_value = self.note
        mock_save_to_db.return_value = True

        expected = {'collaborators': [None],
                    'create_date': None,
                    'id': None,
                    'last_edit_date': None,
                    'last_edit_user_id': None,
                    'tags': [{'id': 1, 'name': 'text'}],
                    'text': 'text',
                    'user_id': 1}

        undecorated_get_account_by_id = undecorated(get_note_by_id)
        result = undecorated_get_account_by_id(1)

        self.assertEqual(expected, result)

    @mock.patch('src.models.Note.get_note_by_id')
    @mock.patch('src.models.Note.save_to_db')
    @mock.patch('src.models.Tag.get_by_id')
    @mock.patch('src.models.user.User.get_by_id')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_update_note_by_id(self, mock_request_parser, mock_user_get_by_id,
                               mock_tag_get_by_id, mock_save_to_db, mock_get_note_by_id):
        mock_request_parser.return_value = self.note_json_update
        mock_user_get_by_id.return_value = self.note
        mock_tag_get_by_id.return_value = self.tag
        mock_save_to_db.return_value = True
        mock_get_note_by_id.return_value = self.note

        expected = {'collaborators': [None],
                    'create_date': None,
                    'id': None,
                    'last_edit_date': datetime.datetime.now(),
                    'last_edit_user_id': 1,
                    'tags': [{'id': 1, 'name': 'text'}],
                    'text': 'Changed text',
                    'user_id': 1}

        undecorated_update_account_by_id = undecorated(update_note_by_id)
        result = undecorated_update_account_by_id(1)

        self.assertEqual(expected, result)

    @mock.patch('src.models.Note.delete_note_by_id')
    @mock.patch('src.models.Note.get_note_by_id')
    @mock.patch('src.models.Role.get_by_name')
    @mock.patch('src.models.User.get_by_username')
    @mock.patch('flask_httpauth.HTTPAuth.current_user')
    def test_delete_article_by_id(self, mock_current_user, mock_get_by_username, mock_get_by_name, mock_get_by_id,
                                  mock_delete_by_id):
        mock_current_user.return_value = 'username'
        mock_get_by_username.return_value = self.user
        mock_get_by_name.return_value = self.admin_role
        mock_get_by_id.return_value = self.note
        mock_delete_by_id.return_value = self.note.to_json()

        expected = {'collaborators': [None],
                    'create_date': None,
                    'id': None,
                    'last_edit_date': None,
                    'last_edit_user_id': None,
                    'tags': [{'id': 1, 'name': 'text'}],
                    'text': 'text',
                    'user_id': 1}

        undecorated_delete_account_by_id = undecorated(delete_note_by_id)
        result = undecorated_delete_account_by_id(1)

        self.assertEqual(expected, result)
