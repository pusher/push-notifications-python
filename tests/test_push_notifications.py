"""Unit tests for Pusher Push Notifications Python server SDK"""

import unittest

import requests_mock

from pusher_push_notifications import PushNotifications


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
            )
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
                'x-pusher-library': 'pusher-push-notifications-python 0.9.0',
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
