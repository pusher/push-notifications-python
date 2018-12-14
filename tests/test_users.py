"""Unit tests for Users features"""

import six
import time
import unittest

import jwt

from pusher_push_notifications import (
    PushNotifications,
)


class TestPushNotificationsUsers(unittest.TestCase):
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
