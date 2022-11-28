from unittest import TestCase
from src.models import NoteTag


class TestAccount(TestCase):

    def test_to_json(self):
        note_tag = NoteTag(id=1, tag_id=1, note_id=1)
        expected_json = {'id': 1, 'note_id': 1, 'tag_id': 1}

        result = note_tag.to_json()

        self.assertEqual(expected_json, result)
