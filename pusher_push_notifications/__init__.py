"""Pusher Push Notifications Python server SDK"""

import six


class PushNotifications(object):
    """Pusher Push Notifications API client
    This client class can be used to publish notifications to the Pusher
    Push Notifications service"""

    def __init__(self, instance_id, secret_key):
        if not isinstance(instance_id, six.string_types):
            raise TypeError('instance_id must be a string')
        if not isinstance(secret_key, six.string_types):
            raise TypeError('secret_key must be a string')
