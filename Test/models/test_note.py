from unittest import TestCase, mock
from src.models import Note


class TestAccount(TestCase):

    def test_to_json(self):
        note = Note(id=1, text='text', user_id=1)
        expected_json = {'collaborators': [],
                         'create_date': None,
                         'id': 1,
                         'last_edit_date': None,
                         'last_edit_user_id': None,
                         'tags': [],
                         'text': 'text',
                         'user_id': 1}

        result = note.to_json()

        self.assertEqual(expected_json, result)

    @mock.patch('src.app.db.session.commit')
    @mock.patch('src.app.db.session.add')
    def test_save_to_db(self, mock_add, mock_commit):
        account = Note(id=1, text='text', user_id=1)

        mock_add.return_value = None
        mock_commit.return_value = None

        Note.save_to_db(account)

        mock_add.assert_called_once_with(account)
        mock_commit.assert_called_once_with()

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_id(self, mock_query_property_getter):
        account = Note(id=1, text='text', user_id=1)
        mock_query_property_getter.return_value.filter_by.return_value.first.return_value = account

        result = Note.get_note_by_id(1)

        self.assertEqual(account, result)

    @mock.patch('src.app.db.session.commit')
    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    @mock.patch('src.models.note.Note.get_note_by_id')
    def test_delete_by_id(self, mock_get_note_by_id, mock_query_property_getter, mock_commit):
        account = Note(id=1, text='text', user_id=1)
        mock_get_note_by_id.return_value = account
        mock_query_property_getter.return_value.filter_by.return_value.delete.return_value = None
        mock_commit.return_value = None

        result = Note.delete_note_by_id(1)

        self.assertEqual(account.to_json(), result)
        mock_get_note_by_id.assert_called_once_with(1)
        mock_query_property_getter.return_value.filter_by.assert_called_once_with(id=1)
        mock_query_property_getter.return_value.filter_by.return_value.delete.assert_called_once_with()
        mock_commit.assert_called_once_with()

    @mock.patch('src.models.note.Note.get_note_by_id')
    def test_delete_by_id_not_found(self, mock_get_by_id):
        mock_get_by_id.return_value = None

        result = Note.delete_note_by_id(1)

        self.assertEqual(({'errors': [{'message': 'Note with such id does not exist.',
                                       'source': "Field 'noteId' in path parameters."}],
                           'traceId': result[0].get('traceId')}, 404), result)
        mock_get_by_id.assert_called_once_with(1)
