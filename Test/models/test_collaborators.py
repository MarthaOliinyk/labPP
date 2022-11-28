from unittest import TestCase
from src.models import Collaborators


class TestAccount(TestCase):

    def test_to_json(self):
        collaborators = Collaborators(id=1, user_id=1, note_id=1)
        expected_json = {'id': 1, 'user_id': 1, 'note_id': 1}

        result = collaborators.to_json()

        self.assertEqual(expected_json, result)
