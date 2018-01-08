"""Pusher Push Notifications Python server SDK"""

import requests
import six

SDK_VERSION = '0.9.0'


class PushNotifications(object):
    """Pusher Push Notifications API client
    This client class can be used to publish notifications to the Pusher
    Push Notifications service"""

    def __init__(self, instance_id, secret_key, endpoint=None):
        if not isinstance(instance_id, six.string_types):
            raise TypeError('instance_id must be a string')
        if not isinstance(secret_key, six.string_types):
            raise TypeError('secret_key must be a string')
        if (endpoint is not None
                and not isinstance(endpoint, six.string_types)):
            raise TypeError('endpoint must be a string')

        self.instance_id = instance_id
        self.secret_key = secret_key
        self._endpoint = endpoint

    @property
    def endpoint(self):
        """Property method to calculate the correct Pusher API host"""
        default_endpoint = '{}.pushnotifications.pusher.com'.format(
            self.instance_id,
        ).lower()
        return self._endpoint or default_endpoint

    def publish(self, interests, publish_body):
        """Publish the given publish_body to the specified interests.

        Args:
            interests (list): List of interests that the publish body should
                be sent to.
            publish_body (dict): Dict containing the body of the push
            notification publish request.
            (see https://docs.pusher.com/push-notifications)

        Returns:
            A dict containing the publish response from the Pusher Push
            Notifications service.
            (see https://docs.pusher.com/push-notifications)

        Raises:
            TypeError: if interests is not a list
            TypeError: if publish_body is not a dict
        """
        if not isinstance(interests, list):
            raise TypeError('interests must be a list')
        if not isinstance(publish_body, dict):
            raise TypeError('publish_body must be a dictionary')

        publish_body['interests'] = interests

        session = requests.Session()
        request = requests.Request(
            'POST',
            'https://{}/publish_api/v1/instances/{}/publishes'.format(
                self.endpoint,
                self.instance_id,
            ),
            json=publish_body,
            headers={
                'host': self.endpoint,
                'authorization': 'Bearer {}'.format(self.secret_key),
                'x-pusher-library': 'pusher-push-notifications-python {}'.format(
                    SDK_VERSION,
                )
            },
        )
        session.send(request.prepare())
