from unittest import TestCase, mock
from src.models import Tag


class TestAccount(TestCase):

    def test_to_json(self):
        tag = Tag(id=1, name="text")
        expected_json = {'id': 1, 'name': 'text'}

        result = tag.to_json()

        self.assertEqual(expected_json, result)

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_id(self, mock_query_property_getter):
        tag = Tag(id=1, name="text")
        mock_query_property_getter.return_value.filter_by.return_value.first.return_value = tag

        result = Tag.get_by_id(1)

        self.assertEqual(tag, result)

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_name(self, mock_query_property_getter):
        tag = Tag(id=1, name="text")
        mock_query_property_getter.return_value.filter_by.return_value.first.return_value = tag

        result = Tag.get_by_name("text")

        self.assertEqual(tag, result)

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_non_existing_name(self, mock_query_property_getter):
        tag = Tag(id=1, name="text")
        mock_query_property_getter.return_value.filter_by.return_value.first.return_value = tag

        result = Tag.get_by_name("tag")

        self.assertEqual(tag, result)

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_all(self, mock_query_property_getter):
        mock_query_property_getter.return_value = {'error': f'There aren\'t any tags available'}

        expected = ({'error': f'There aren\'t any tags available'}, 404)

        result = Tag.get_all()

        self.assertEqual(expected, result)
