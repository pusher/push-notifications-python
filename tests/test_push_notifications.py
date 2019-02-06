"""Unit tests for Pusher Push Notifications Python server SDK"""

import unittest

from pusher_push_notifications import (
    PushNotifications,
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
