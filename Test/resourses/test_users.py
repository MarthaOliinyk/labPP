from src.models import Role, User
from unittest import TestCase, mock
from undecorated import undecorated
from src.resourses import create_user, get_user_by_id, get_user_statistic, delete_user_by_id, update_user


class TestUsers(TestCase):

    def setUp(self) -> None:
        self.user = User(
            username='username',
            first_name='first_name',
            last_name='last_name',
            email='email',
            password='password'
        )

        self.user_json_create = {
            'username': 'denshykk',
            'firstName': 'Denys',
            'lastName': 'Tykhonov',
            'email': 'denshykk@gmail.com',
            'password': 'whocares'
        }

        self.get_user_json = {
            'accountIds': [],
            'email': 'email',
            'first_name': 'first_name',
            'id': None,
            'last_name': 'last_name',
            'password': 'password',
            'roles': [],
            'username': 'username'
        }

        self.update_user_json = {
            'username': 'new',
            'firstName': 'new',
            'lastName': 'new'
        }

    @mock.patch('src.models.user.User.save_to_db')
    @mock.patch('src.models.role.Role.get_by_name')
    @mock.patch('src.models.user.User.get_by_username')
    @mock.patch('src.models.user.User.generate_hash')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_create_user(self, mock_request_parser, mock_generate_hash, mock_get_by_username, mock_get_by_name,
                         mock_save_to_db):
        mock_request_parser.return_value = self.user_json_create
        mock_generate_hash.return_value = 'password'
        mock_get_by_username.return_value = False
        mock_get_by_name.return_value = Role(id=1, name='user')
        mock_save_to_db.return_value = True

        result = create_user()

        self.assertEqual({
            "accountIds": [],
            "email": "denshykk@gmail.com",
            "first_name": "Denys",
            "id": None,
            "last_name": "Tykhonov",
            "password": "password",
            "roles": [
                "user"
            ],
            "username": "denshykk"
        }, result)
