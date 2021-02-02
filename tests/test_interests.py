"""Unit tests interests based publishing"""

import time
import unittest

import requests_mock

from pusher_push_notifications import (
    PushNotifications,
    PusherAuthError,
    PusherMissingInstanceError,
    PusherServerError,
    PusherValidationError,
    PusherBadResponseError,
)


class TestPushNotificationsInterests(unittest.TestCase):
    def test_publish_to_interests_should_make_correct_http_request(self):
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
            response = pn_client.publish_to_interests(
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
            '/publish_api/v1/instances/instance_id/publishes/interests',
        )
        self.assertDictEqual(
            headers,
            {
                'content-type': 'application/json',
                'content-length': '69',
                'authorization': 'Bearer SECRET_KEY',
                'x-pusher-library': 'pusher-push-notifications-python 2.0.1',
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

    def test_deprecated_alias_still_works(self):
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
            '/publish_api/v1/instances/instance_id/publishes/interests',
        )
        self.assertDictEqual(
            headers,
            {
                'content-type': 'application/json',
                'content-length': '69',
                'authorization': 'Bearer SECRET_KEY',
                'x-pusher-library': 'pusher-push-notifications-python 2.0.1',
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

    def test_publish_to_interests_should_fail_if_interests_not_list(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(TypeError) as e:
            pn_client.publish_to_interests(
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

    def test_publish_to_interests_should_fail_if_body_not_dict(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(TypeError) as e:
            pn_client.publish_to_interests(
                interests=['donuts'],
                publish_body=False,
            )
        self.assertIn('publish_body must be a dictionary', str(e.exception))

    def test_publish_to_interests_should_fail_if_no_interests_passed(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(ValueError) as e:
            pn_client.publish_to_interests(
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

    def test_publish_to_interests_should_succeed_if_100_interests_passed(self):
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
            pn_client.publish_to_interests(
                interests=['interest-' + str(i) for i in range(0, 100)],
                publish_body={
                    'apns': {
                        'aps': {
                            'alert': 'Hello World!',
                        },
                    },
                },
            )

    def test_publish_to_interests_should_fail_if_too_many_interests_passed(self):
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
                pn_client.publish_to_interests(
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

    def test_publish_to_interests_should_fail_if_interest_not_a_string(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(TypeError) as e:
            pn_client.publish_to_interests(
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

    def test_publish_to_interests_should_fail_if_interest_too_long(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(ValueError) as e:
            pn_client.publish_to_interests(
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

    def test_publish_to_interests_should_fail_if_interest_contains_invalid_chars(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(ValueError) as e:
            pn_client.publish_to_interests(
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
            pn_client.publish_to_interests(
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
            pn_client.publish_to_interests(
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

    def test_publish_to_interests_should_raise_on_http_4xx_error(self):
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
                pn_client.publish_to_interests(
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

    def test_publish_to_interests_should_raise_on_http_5xx_error(self):
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
                pn_client.publish_to_interests(
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

    def test_publish_to_interests_should_raise_on_http_401_error(self):
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
                pn_client.publish_to_interests(
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

    def test_publish_to_interests_should_raise_on_http_404_error(self):
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
                pn_client.publish_to_interests(
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


    def test_publish_to_interests_should_error_correctly_if_error_not_json(self):
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
                pn_client.publish_to_interests(
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

    def test_publish_to_interests_should_handle_not_json_success(self):
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
                pn_client.publish_to_interests(
                    interests=['donuts'],
                    publish_body={
                        'apns': {
                            'aps': {
                                'alert': 'Hello World!',
                            },
                        },
                    },
                )
            self.assertIn('The server returned a malformed response', str(e.exception))
