import json
import unittest

from project.tests.base import BaseTestCase
from project.tests.utils import add_user, add_admin
from project import db
from project.api.models import User


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        # Add a test user, that we will login in with
        add_admin('test', 'test@test.com', 'test')
        with self.client:
            # Login with the test user
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            # Get the token.
            # User needs to be authenticated to make a post request to /users
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'josh',
                    'email': 'bolualawode@gmail.com',
                    'password': 'greaterthaneight'
                }),
                content_type='application/json',
                # Add the token to the request, for authentication
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('bolualawode@gmail.com was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        # Add a test user, that we will login in with
        add_admin('test', 'test@test.com', 'test')
        with self.client:
            # Login with the test user
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json',
            )
            # Get the token.
            # You need to be authenticated to make a post request to /users
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
                # Add the token to the request, for authentication
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have
        a username key.
        """
        # Add a test user, that we will login in with
        add_admin('test', 'test@test.com', 'test')
        with self.client:
            # Login with the test user
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json',
            )
            # Get the token.
            # You need to be authenticated to make a post request to /users
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'email': 'bolualawode@gmail.com',
                    'password': 'greaterthaneight'
                    }),
                content_type='application/json',
                # Add the token to the request, for authentication
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        # Add a test user, that we will login in with
        add_admin('test', 'test@test.com', 'test')
        with self.client:
            # Login with the test user
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json',
            )
            # Get the token.
            # You need to be authenticated to make a post request to /users
            token = json.loads(resp_login.data.decode())['auth_token']
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'josh',
                    'email': 'bolualawode@gmail.com',
                    'password': 'greaterthaneight'
                }),
                content_type='application/json',
                # Add the token to the request, for authentication
                headers={'Authorization': f'Bearer {token}'}
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'josh',
                    'email': 'bolualawode@gmail.com',
                    'password': 'greaterthaneight'
                }),
                content_type='application/json',
                # Add the token to the request, for authentication
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That email already exists.', data['message']
            )
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user('josh', 'bolualawode@gmail.com', 'greaterthaneight')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('josh', data['data']['username'])
            self.assertIn('bolualawode@gmail.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Ensure get all users behaves correctly."""
        add_user('josh', 'bolualawode@gmail.com', 'greaterthaneight')
        add_user('jondoe', 'jon@doe.com', 'greaterthaneight')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('josh', data['data']['users'][0]['username'])
            self.assertIn(
                'bolualawode@gmail.com', data['data']['users'][0]['email']
            )
            self.assertIn('jondoe', data['data']['users'][1]['username'])
            self.assertIn(
                'jon@doe.com', data['data']['users'][1]['email']
            )
            self.assertTrue(data['data']['users'][1]['active'])
            self.assertFalse(data['data']['users'][1]['admin'])
            self.assertIn('success', data['status'])

    def test_main_no_users(self):
        """
        Ensure the main route behvaes correctly when no users have
        been added to the database.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Users', response.data)
        self.assertIn(b'<p>No users!</p>', response.data)

    def test_main_with_users(self):
        """
        Ensure the main route behaves correctly when users have been
        added to the database.
        """
        add_user('josh', 'bolualawode@gmail.com', 'greaterthaneight')
        add_user('jondoe', 'jon@doe.com', 'greaterthaneight')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Users', response.data)
            self.assertNotIn(b'<p<No users!</p>', response.data)
            self.assertIn(b'josh', response.data)
            self.assertIn(b'jon', response.data)

    def test_main_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(username='josh',
                          email='bolualawode@gmail.com',
                          password='greaterthaneight'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Users', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'josh', response.data)

    def test_add_user_invalid_json_keys_no_password(self):
        """
        Ensure error is thrown if the JSON object does
        not have a password key.
        """
        # Add a test user, that we will login in with
        add_admin('test', 'test@test.com', 'test')
        with self.client:
            # Login with the test user
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            # Get the token.
            # User needs to be authenticated to make a post request to /users
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='josh',
                    email="bolualawode@gmail.com"
                )),
                content_type='application/json',
                # Add the token to the request, for authentication
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_inactive(self):
        add_user('test', 'test@test.com', 'test')
        # Update user
        user = User.query.filter_by(email='test@test.com').first()
        user.active = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'josh',
                    'email': 'g@never.com',
                    'password': 'test'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid auth token.')
            self.assertEqual(response.status_code, 401)

    def test_add_user_not_admin(self):
        # Add a test user, that we will login in with
        add_user('test', 'test@test.com', 'test')
        with self.client:
            # Login with the test user
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            # Get the token.
            # User needs to be authenticated to make a post request to /users
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'josh',
                    'email': 'bolualawode@gmail.com',
                    'password': 'greaterthaneight'
                }),
                content_type='application/json',
                # Add the token to the request, for authentication
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'You do not have permission to do that.'
            )
            self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
