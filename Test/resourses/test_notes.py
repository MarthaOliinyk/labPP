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

        self.note2 = Note(
            text='text',
            user_id=2,
        )

        self.user_role = Role(
            id=1,
            name='user'
        )

        self.admin_role = Role(
            id=2,
            name='admin'
        )

        self.user.notes.append(self.note)
        self.user.roles.append(self.user_role)
        self.note.tags.append(self.tag)
        self.note2.tags.append(self.tag)

    @mock.patch('src.models.Note.save_to_db')
    @mock.patch('src.models.user.User.get_by_id')
    def test_create_note(self, mock_get_by_id, mock_save_to_db):
        mock_get_by_id.return_value = self.user
        mock_save_to_db.return_value = True

        undecorated_create_note = undecorated(create_note)
        result = undecorated_create_note()

        self.assertEqual({'balance': 0, 'id': None, 'user_id': 1}, result)

    @mock.patch('src.models.user.User.get_by_id')
    def test_create_account_with_invalid_user(self, mock_get_by_id):
        mock_get_by_id.return_value = None

        undecorated_create_note = undecorated(create_note)
        result = undecorated_create_note()

        self.assertEqual(({'errors': [{'message': 'User with such id does not exist.',
                                       'source': "Field 'userId' in path parameters."}],
                           'traceId': result[0].get('traceId')}, 404), result)


