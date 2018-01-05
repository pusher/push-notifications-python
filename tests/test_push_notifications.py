"""Unit tests for Pusher Push Notifications Python server SDK"""

import unittest

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
