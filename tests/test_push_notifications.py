"""Unit tests for Pusher Push Notifications Python server SDK"""

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
)


class TestPushNotifications(unittest.TestCase):
    def test_constructor_should_accept_valid_params(self):
        PushNotifications(
            instance_id='1234',
            secret_key='1234',
        )

    def test_constructor_should_fail_if_instance_id_not_string(self):
        with self.assertRaises(TypeError) as e:
            PushNotifications(
                instance_id=False,
                secret_key='1234',
            )
        self.assertIn('instance_id must be a string', str(e.exception))

    def test_constructor_should_fail_if_instance_id_empty_string(self):
        with self.assertRaises(ValueError) as e:
            PushNotifications(
                instance_id='',
                secret_key='1234',
            )
        self.assertIn('instance_id cannot be the empty string', str(e.exception))

    def test_constructor_should_fail_if_secret_key_not_string(self):
        with self.assertRaises(TypeError) as e:
            PushNotifications(
                instance_id='1234',
                secret_key=False,
            )
        self.assertIn('secret_key must be a string', str(e.exception))

    def test_constructor_should_fail_if_secret_key_empty_string(self):
        with self.assertRaises(ValueError) as e:
            PushNotifications(
                instance_id='1234',
                secret_key='',
            )
        self.assertIn('secret_key cannot be the empty string', str(e.exception))

    def test_constructor_should_fail_if_endpoint_not_string(self):
        with self.assertRaises(TypeError) as e:
            PushNotifications(
                instance_id='1234',
                secret_key='1234',
                endpoint=False,
            )
        self.assertIn('endpoint must be a string', str(e.exception))

    def test_constructor_should_set_endpoint_default(self):
        pn_client = PushNotifications(
            instance_id='INSTANCE_ID',
            secret_key='1234',
        )
        self.assertEqual(
            pn_client.endpoint,
            'instance_id.pushnotifications.pusher.com',
        )

    def test_constructor_should_accept_endpoint_override(self):
        pn_client = PushNotifications(
            instance_id='INSTANCE_ID',
            secret_key='1234',
            endpoint='example.com/push',
        )
        self.assertEqual(
            pn_client.endpoint,
            'example.com/push',
        )

    def test_publish_should_make_correct_http_request(self):
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
            response = pn_client.publish(
                interests=['donuts'],
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
            '/publish_api/v1/instances/instance_id/publishes',
        )
        self.assertDictEqual(
            headers,
            {
                'content-type': 'application/json',
                'content-length': '69',
                'authorization': 'Bearer SECRET_KEY',
                'x-pusher-library': 'pusher-push-notifications-python 1.0.2',
                'host': 'instance_id.pushnotifications.pusher.com',
            },
        )
        self.assertDictEqual(
            body,
            {
                'interests': ['donuts'],
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

    def test_publish_should_fail_if_interests_not_list(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(TypeError) as e:
            pn_client.publish(
                interests=False,
                publish_body={
                    'apns': {
                        'aps': {
                            'alert': 'Hello World!',
                        },
                    },
                },
            )
        self.assertIn('interests must be a list', str(e.exception))

    def test_publish_should_fail_if_body_not_dict(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(TypeError) as e:
            pn_client.publish(
                interests=['donuts'],
                publish_body=False,
            )
        self.assertIn('publish_body must be a dictionary', str(e.exception))

    def test_publish_should_fail_if_no_interests_passed(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(ValueError) as e:
            pn_client.publish(
                interests=[],
                publish_body={
                    'apns': {
                        'aps': {
                            'alert': 'Hello World!',
                        },
                    },
                },
            )
        self.assertIn('must target at least one interest', str(e.exception))

    def test_publish_should_succeed_if_100_interests_passed(self):
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
            pn_client.publish(
                interests=['interest-' + str(i) for i in range(0, 100)],
                publish_body={
                    'apns': {
                        'aps': {
                            'alert': 'Hello World!',
                        },
                    },
                },
            )

    def test_publish_should_fail_if_too_many_interests_passed(self):
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
                pn_client.publish(
                    interests=['interest-' + str(i) for i in range(0, 101)],
                    publish_body={
                        'apns': {
                            'aps': {
                                'alert': 'Hello World!',
                            },
                        },
                    },
                )
            self.assertIn('Number of interests (101) exceeds maximum', str(e.exception))

    def test_publish_should_fail_if_interest_not_a_string(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(TypeError) as e:
            pn_client.publish(
                interests=[False],
                publish_body={
                    'apns': {
                        'aps': {
                            'alert': 'Hello World!',
                        },
                    },
                },
            )
        self.assertIn('Interest False is not a string', str(e.exception))

    def test_publish_should_fail_if_interest_too_long(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(ValueError) as e:
            pn_client.publish(
                interests=['A'*200],
                publish_body={
                    'apns': {
                        'aps': {
                            'alert': 'Hello World!',
                        },
                    },
                },
            )
        self.assertIn('longer than the maximum of 164 chars', str(e.exception))

    def test_publish_should_fail_if_interest_contains_invalid_chars(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(ValueError) as e:
            pn_client.publish(
                interests=['bad:interest'],
                publish_body={
                    'apns': {
                        'aps': {
                            'alert': 'Hello World!',
                        },
                    },
                },
            )
        self.assertIn('"bad:interest" contains a forbidden character', str(e.exception))

        with self.assertRaises(ValueError) as e:
            pn_client.publish(
                interests=['bad|interest'],
                publish_body={
                    'apns': {
                        'aps': {
                            'alert': 'Hello World!',
                        },
                    },
                },
            )
        self.assertIn('"bad|interest" contains a forbidden character', str(e.exception))

        with self.assertRaises(ValueError) as e:
            pn_client.publish(
                interests=['bad(interest)'],
                publish_body={
                    'apns': {
                        'aps': {
                            'alert': 'Hello World!',
                        },
                    },
                },
            )
        self.assertIn('"bad(interest)" contains a forbidden character', str(e.exception))

    def test_publish_should_raise_on_http_4xx_error(self):
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
                pn_client.publish(
                    interests=['donuts'],
                    publish_body={
                        'apns': {
                            'aps': {
                                'alert': 'Hello World!',
                            },
                        },
                    },
                )
            self.assertIn('Invalid request: blah', str(e.exception))

    def test_publish_should_raise_on_http_5xx_error(self):
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
                pn_client.publish(
                    interests=['donuts'],
                    publish_body={
                        'apns': {
                            'aps': {
                                'alert': 'Hello World!',
                            },
                        },
                    },
                )
            self.assertIn('Server error: blah', str(e.exception))

    def test_publish_should_raise_on_http_401_error(self):
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
                pn_client.publish(
                    interests=['donuts'],
                    publish_body={
                        'apns': {
                            'aps': {
                                'alert': 'Hello World!',
                            },
                        },
                    },
                )
            self.assertIn('Auth error: blah', str(e.exception))

    def test_publish_should_raise_on_http_404_error(self):
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
                pn_client.publish(
                    interests=['donuts'],
                    publish_body={
                        'apns': {
                            'aps': {
                                'alert': 'Hello World!',
                            },
                        },
                    },
                )
            self.assertIn('Instance not found: blah', str(e.exception))


    def test_publish_should_error_correctly_if_error_not_json(self):
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
                pn_client.publish(
                    interests=['donuts'],
                    publish_body={
                        'apns': {
                            'aps': {
                                'alert': 'Hello World!',
                            },
                        },
                    },
                )
            self.assertIn('Unknown error: no description', str(e.exception))

    def test_authenticate_user_should_return_token(self):
        user_id = 'user-0001'
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )

        token_string = pn_client.authenticate_user(user_id)

        self.assertIsInstance(token_string, six.string_types)
        self.assertTrue(len(token_string) > 0)

        decoded_token = jwt.decode(
            token_string,
            'SECRET_KEY',
            algorithm='HS256',
        )

        expected_issuer = 'https://INSTANCE_ID.pushnotifications.pusher.com'
        expected_subject = user_id

        self.assertEquals(decoded_token.get('iss'), expected_issuer)
        self.assertEquals(decoded_token.get('sub'), expected_subject)
        self.assertIsNotNone(decoded_token.get('exp'))
        self.assertTrue(decoded_token.get('exp') > time.time())


    def test_authenticate_user_should_fail_if_user_id_not_a_string(self):
        user_id = False
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(ValueError) as e:
            pn_client.authenticate_user(user_id)
        self.assertIn('user_id must be a string', str(e.exception))

    def test_authenticate_user_should_fail_if_user_id_too_long(self):
        user_id = 'A' * 165
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(ValueError) as e:
            pn_client.authenticate_user(user_id)
        self.assertIn('longer than the maximum of 164 chars', str(e.exception))
