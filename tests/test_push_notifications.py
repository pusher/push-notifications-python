"""Unit tests for Pusher Push Notifications Python server SDK"""

import unittest

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
        with self.assertRaises(TypeError):
            PushNotifications(
                instance_id=False,
                secret_key='1234',
            )

    def test_constructor_should_fail_if_secret_key_not_string(self):
        with self.assertRaises(TypeError):
            PushNotifications(
                instance_id='1234',
                secret_key=False,
            )

    def test_constructor_should_fail_if_endpoint_not_string(self):
        with self.assertRaises(TypeError):
            PushNotifications(
                instance_id='1234',
                secret_key='1234',
                endpoint=False,
            )

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
                'x-pusher-library': 'pusher-push-notifications-python 0.10.0',
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
        with self.assertRaises(TypeError):
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

    def test_publish_should_fail_if_body_not_dict(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(TypeError):
            pn_client.publish(
                interests=['donuts'],
                publish_body=False,
            )

    def test_publish_should_fail_if_no_interests_passed(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(ValueError):
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
            with self.assertRaises(ValueError):
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

    def test_publish_should_fail_if_interest_not_a_string(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(TypeError):
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

    def test_publish_should_fail_if_interest_too_long(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(ValueError):
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

    def test_publish_should_fail_if_interest_contains_invalid_chars(self):
        pn_client = PushNotifications(
            'INSTANCE_ID',
            'SECRET_KEY'
        )
        with self.assertRaises(ValueError):
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
        with self.assertRaises(ValueError):
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
            with self.assertRaises(PusherValidationError):
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
            with self.assertRaises(PusherServerError):
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
            with self.assertRaises(PusherAuthError):
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
            with self.assertRaises(PusherMissingInstanceError):
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
