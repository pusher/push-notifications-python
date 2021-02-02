"""Unit tests for Users features"""

import six
import time
import unittest

import jwt
import requests_mock

from pusher_push_notifications import (
    PushNotifications,
    PusherAuthError,
    PusherMissingInstanceError,
    PusherServerError,
    PusherValidationError,
    PusherBadResponseError,
)


class TestPushNotificationsUsers(unittest.TestCase):
    def test_generate_token_should_return_token(self):
        user_id = 'user-0001'
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )

        token_object = pn_client.generate_token(user_id)
        self.assertIsInstance(token_object, dict)

        token_string = token_object.get('token')
        self.assertIsInstance(token_string, six.string_types)

        self.assertTrue(len(token_string) > 0)

        decoded_token = jwt.decode(
            token_string,
            'SECRET_KEY',
            algorithms='HS256',
        )

        expected_issuer = 'https://INSTANCE_ID.pushnotifications.pusher.com'
        expected_subject = user_id

        self.assertEquals(decoded_token.get('iss'), expected_issuer)
        self.assertEquals(decoded_token.get('sub'), expected_subject)
        self.assertIsNotNone(decoded_token.get('exp'))
        self.assertTrue(decoded_token.get('exp') > time.time())

    def test_generate_token_should_fail_if_user_id_not_a_string(self):
        user_id = False
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(TypeError) as e:
            pn_client.generate_token(user_id)
        self.assertIn('user_id must be a string', str(e.exception))

    def test_generate_token_should_fail_if_user_id_too_long(self):
        user_id = 'A' * 165
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(ValueError) as e:
            pn_client.generate_token(user_id)
        self.assertIn('longer than the maximum of 164 chars', str(e.exception))

    def test_publish_to_users_should_make_correct_http_request(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with requests_mock.Mocker() as http_mock:
            http_mock.register_uri(
                requests_mock.ANY,
                requests_mock.ANY,
                status_code=200,
                json={
                    'publishId': '1234',
                },
            )
            response = pn_client.publish_to_users(
                user_ids=['alice'],
                publish_body={
                    'apns': {
                        'aps': {
                            'alert': 'Hello World!',
                        },
                    },
                },
            )
            req = http_mock.request_history[0]

        method = req.method
        path = req.path
        headers = dict(req._request.headers.lower_items())
        body = req.json()

        self.assertEqual(
            method,
            'POST',
        )
        self.assertEqual(
            path,
            '/publish_api/v1/instances/instance_id/publishes/users',
        )
        self.assertDictEqual(
            headers,
            {
                'content-type': 'application/json',
                'content-length': '64',
                'authorization': 'Bearer SECRET_KEY',
                'x-pusher-library': 'pusher-push-notifications-python 2.0.1',
                'host': 'instance_id.pushnotifications.pusher.com',
            },
        )
        self.assertDictEqual(
            body,
            {
                'users': ['alice'],
                'apns': {
                    'aps': {
                        'alert': 'Hello World!',
                    },
                },
            },
        )
        self.assertDictEqual(
            response,
            {
                'publishId': '1234',
            },
        )

    def test_publish_to_users_should_fail_if_user_ids_not_list(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(TypeError) as e:
            pn_client.publish_to_users(
                user_ids=False,
                publish_body={
                    'apns': {
                        'aps': {
                            'alert': 'Hello World!',
                        },
                    },
                },
            )
        self.assertIn('user_ids must be a list', str(e.exception))

    def test_publish_to_users_should_fail_if_body_not_dict(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(TypeError) as e:
            pn_client.publish_to_users(
                user_ids=['alice'],
                publish_body=False,
            )
        self.assertIn('publish_body must be a dictionary', str(e.exception))

    def test_publish_to_users_should_fail_if_no_users_passed(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(ValueError) as e:
            pn_client.publish_to_users(
                user_ids=[],
                publish_body={
                    'apns': {
                        'aps': {
                            'alert': 'Hello World!',
                        },
                    },
                },
            )
        self.assertIn('must target at least one user', str(e.exception))

    def test_publish_to_users_should_succeed_if_1000_users_passed(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with requests_mock.Mocker() as http_mock:
            http_mock.register_uri(
                requests_mock.ANY,
                requests_mock.ANY,
                status_code=200,
                json={
                    'publishId': '1234',
                },
            )
            pn_client.publish_to_users(
                user_ids=['user-' + str(i) for i in range(0, 1000)],
                publish_body={
                    'apns': {
                        'aps': {
                            'alert': 'Hello World!',
                        },
                    },
                },
            )

    def test_publish_should_fail_if_too_many_user_ids_passed(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with requests_mock.Mocker() as http_mock:
            http_mock.register_uri(
                requests_mock.ANY,
                requests_mock.ANY,
                status_code=200,
                json={
                    'publishId': '1234',
                },
            )
            with self.assertRaises(ValueError) as e:
                pn_client.publish_to_users(
                    user_ids=['user-' + str(i) for i in range(0, 1001)],
                    publish_body={
                        'apns': {
                            'aps': {
                                'alert': 'Hello World!',
                            },
                        },
                    },
                )
            self.assertIn(
                'Number of user ids (1001) exceeds maximum',
                str(e.exception),
            )

    def test_publish_to_users_should_fail_if_user_id_not_a_string(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(TypeError) as e:
            pn_client.publish_to_users(
                user_ids=[False],
                publish_body={
                    'apns': {
                        'aps': {
                            'alert': 'Hello World!',
                        },
                    },
                },
            )
        self.assertIn('User id False is not a string', str(e.exception))

    def test_publish_to_users_should_fail_if_user_id_too_long(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(ValueError) as e:
            pn_client.publish_to_users(
                user_ids=['A'*165],
                publish_body={
                    'apns': {
                        'aps': {
                            'alert': 'Hello World!',
                        },
                    },
                },
            )
        self.assertIn('longer than the maximum of 164 chars', str(e.exception))

    def test_publish_to_users_should_raise_on_http_4xx_error(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with requests_mock.Mocker() as http_mock:
            http_mock.register_uri(
                requests_mock.ANY,
                requests_mock.ANY,
                status_code=400,
                json={'error': 'Invalid request', 'description': 'blah'},
            )
            with self.assertRaises(PusherValidationError) as e:
                pn_client.publish_to_users(
                    user_ids=['alice'],
                    publish_body={
                        'apns': {
                            'aps': {
                                'alert': 'Hello World!',
                            },
                        },
                    },
                )
            self.assertIn('Invalid request: blah', str(e.exception))

    def test_publish_to_users_should_raise_on_http_5xx_error(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with requests_mock.Mocker() as http_mock:
            http_mock.register_uri(
                requests_mock.ANY,
                requests_mock.ANY,
                status_code=500,
                json={'error': 'Server error', 'description': 'blah'},
            )
            with self.assertRaises(PusherServerError) as e:
                pn_client.publish_to_users(
                    user_ids=['alice'],
                    publish_body={
                        'apns': {
                            'aps': {
                                'alert': 'Hello World!',
                            },
                        },
                    },
                )
            self.assertIn('Server error: blah', str(e.exception))

    def test_publish_to_users_should_raise_on_http_401_error(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with requests_mock.Mocker() as http_mock:
            http_mock.register_uri(
                requests_mock.ANY,
                requests_mock.ANY,
                status_code=401,
                json={'error': 'Auth error', 'description': 'blah'},
            )
            with self.assertRaises(PusherAuthError) as e:
                pn_client.publish_to_users(
                    user_ids=['alice'],
                    publish_body={
                        'apns': {
                            'aps': {
                                'alert': 'Hello World!',
                            },
                        },
                    },
                )
            self.assertIn('Auth error: blah', str(e.exception))

    def test_publish_to_users_should_raise_on_http_404_error(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with requests_mock.Mocker() as http_mock:
            http_mock.register_uri(
                requests_mock.ANY,
                requests_mock.ANY,
                status_code=404,
                json={'error': 'Instance not found', 'description': 'blah'},
            )
            with self.assertRaises(PusherMissingInstanceError) as e:
                pn_client.publish_to_users(
                    user_ids=['alice'],
                    publish_body={
                        'apns': {
                            'aps': {
                                'alert': 'Hello World!',
                            },
                        },
                    },
                )
            self.assertIn('Instance not found: blah', str(e.exception))

    def test_publish_to_users_should_error_correctly_if_error_not_json(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with requests_mock.Mocker() as http_mock:
            http_mock.register_uri(
                requests_mock.ANY,
                requests_mock.ANY,
                status_code=500,
                text='<notjson></notjson>',
            )
            with self.assertRaises(PusherServerError) as e:
                pn_client.publish_to_users(
                    user_ids=['alice'],
                    publish_body={
                        'apns': {
                            'aps': {
                                'alert': 'Hello World!',
                            },
                        },
                    },
                )
            self.assertIn('Unknown error: no description', str(e.exception))

    def test_publish_to_users_should_handle_not_json_success(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with requests_mock.Mocker() as http_mock:
            http_mock.register_uri(
                requests_mock.ANY,
                requests_mock.ANY,
                status_code=200,
                text='<notjson></notjson>',
            )
            with self.assertRaises(PusherBadResponseError) as e:
                pn_client.publish_to_users(
                    user_ids=['alice'],
                    publish_body={
                        'apns': {
                            'aps': {
                                'alert': 'Hello World!',
                            },
                        },
                    },
                )
            self.assertIn('The server returned a malformed response', str(e.exception))

    def test_delete_user_should_make_correct_http_request(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with requests_mock.Mocker() as http_mock:
            http_mock.register_uri(
                requests_mock.ANY,
                requests_mock.ANY,
                status_code=200,
                json='',
            )
            pn_client.delete_user('alice')
            req = http_mock.request_history[0]

        method = req.method
        path = req.path
        headers = dict(req._request.headers.lower_items())

        self.assertEqual(
            method,
            'DELETE',
        )
        self.assertEqual(
            path,
            '/customer_api/v1/instances/instance_id/users/alice',
        )
        self.assertDictEqual(
            headers,
            {
                'content-length': '0',
                'authorization': 'Bearer SECRET_KEY',
                'x-pusher-library': 'pusher-push-notifications-python 2.0.1',
                'host': 'instance_id.pushnotifications.pusher.com',
            },
        )

    def test_delete_user_should_fail_if_user_id_not_a_string(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(TypeError) as e:
            pn_client.delete_user(False)
        self.assertIn('user_id must be a string', str(e.exception))

    def test_delete_user_should_fail_if_user_id_too_long(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(ValueError) as e:
            pn_client.delete_user('A'*165)
        self.assertIn('longer than the maximum of 164 chars', str(e.exception))

    def test_delete_user_should_raise_on_http_4xx_error(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with requests_mock.Mocker() as http_mock:
            http_mock.register_uri(
                requests_mock.ANY,
                requests_mock.ANY,
                status_code=400,
                json={'error': 'Invalid request', 'description': 'blah'},
            )
            with self.assertRaises(PusherValidationError) as e:
                pn_client.delete_user('user-0001')
            self.assertIn('Invalid request: blah', str(e.exception))

    def test_delete_user_should_raise_on_http_5xx_error(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with requests_mock.Mocker() as http_mock:
            http_mock.register_uri(
                requests_mock.ANY,
                requests_mock.ANY,
                status_code=500,
                json={'error': 'Server error', 'description': 'blah'},
            )
            with self.assertRaises(PusherServerError) as e:
                pn_client.delete_user('user-0001')
            self.assertIn('Server error: blah', str(e.exception))

    def test_delete_user_should_raise_on_http_401_error(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with requests_mock.Mocker() as http_mock:
            http_mock.register_uri(
                requests_mock.ANY,
                requests_mock.ANY,
                status_code=401,
                json={'error': 'Auth error', 'description': 'blah'},
            )
            with self.assertRaises(PusherAuthError) as e:
                pn_client.delete_user('user-0001')
            self.assertIn('Auth error: blah', str(e.exception))

    def test_delete_user_should_raise_on_http_404_error(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with requests_mock.Mocker() as http_mock:
            http_mock.register_uri(
                requests_mock.ANY,
                requests_mock.ANY,
                status_code=404,
                json={'error': 'Instance not found', 'description': 'blah'},
            )
            with self.assertRaises(PusherMissingInstanceError) as e:
                pn_client.delete_user('user-0001')
            self.assertIn('Instance not found: blah', str(e.exception))

    def test_delete_user_should_error_correctly_if_error_not_json(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with requests_mock.Mocker() as http_mock:
            http_mock.register_uri(
                requests_mock.ANY,
                requests_mock.ANY,
                status_code=500,
                text='<notjson></notjson>',
            )
            with self.assertRaises(PusherServerError) as e:
                pn_client.delete_user('user-0001')
            self.assertIn('Unknown error: no description', str(e.exception))

    def test_delete_user_should_not_error_on_not_json_success(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with requests_mock.Mocker() as http_mock:
            http_mock.register_uri(
                requests_mock.ANY,
                requests_mock.ANY,
                status_code=200,
                text='<notjson></notjson>',
            )
            pn_client.delete_user('alice')
