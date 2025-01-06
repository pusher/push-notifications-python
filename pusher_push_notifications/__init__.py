"""Pusher Push Notifications Python server SDK"""

import copy
import datetime
import json
import os
import re
import time
import warnings

import jwt
import requests
import six
from six.moves import urllib

SDK_VERSION = '2.0.2'

INTEREST_MAX_LENGTH = 164
INTEREST_REGEX = re.compile('^(_|-|=|@|,|\\.|;|[A-Z]|[a-z]|[0-9])*$')
MAX_NUMBER_OF_INTERESTS = 100

USER_ID_MAX_LENGTH = 164
AUTH_TOKEN_DURATION = datetime.timedelta(days=1)
MAX_NUMBER_OF_USER_IDS = 1000


class PusherError(Exception):
    """Base class for all Pusher push notifications errors"""


class PusherValidationError(PusherError, ValueError):
    """Error thrown when the Push Notifications publish body is invalid"""


class PusherAuthError(PusherError, ValueError):
    """Error thrown when the Push Notifications secret key is incorrect"""


class PusherMissingInstanceError(PusherError, KeyError):
    """Error thrown when the instance id used does not exist"""


class PusherServerError(PusherError, Exception):
    """Error thrown when the Push Notifications service has an internal server
    error
    """

class PusherBadResponseError(PusherError, Exception):
    """Error thrown when the server returns a response the library cannot
    understand
    """


def _handle_http_error(response_body, status_code):
    error_string = '{}: {}'.format(
        response_body.get('error', 'Unknown error'),
        response_body.get('description', 'no description'),
    )
    if status_code == 401:
        raise PusherAuthError(error_string)
    if status_code == 404:
        raise PusherMissingInstanceError(error_string)
    if 400 <= status_code < 500:
        raise PusherValidationError(error_string)
    if 500 <= status_code < 600:
        raise PusherServerError(error_string)


def _make_url(scheme, host, path):
    return urllib.parse.urlunparse([
        scheme,
        host,
        path,
        None,
        None,
        None,
    ])


def _get_proxies_from_env():
    return {
        'http': os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy'),
        'https': os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy'),
    }


class PushNotifications(object):
    """Pusher Push Notifications API client
    This client class can be used to publish notifications to the Pusher
    Push Notifications service"""

    def __init__(self, instance_id, secret_key, endpoint=None):
        if not isinstance(instance_id, six.string_types):
            raise TypeError('instance_id must be a string')
        if instance_id == '':
            raise ValueError('instance_id cannot be the empty string')

        if not isinstance(secret_key, six.string_types):
            raise TypeError('secret_key must be a string')
        if secret_key == '':
            raise ValueError('secret_key cannot be the empty string')

        if (endpoint is not None
                and not isinstance(endpoint, six.string_types)):
            raise TypeError('endpoint must be a string')

        self.instance_id = instance_id
        self.secret_key = secret_key
        self._endpoint = endpoint

        session = requests.Session()
        # We've had multiple support requests about this library not working
        # on PythonAnywhere (a popular python deployment platform)
        # They require that proxy servers be loaded from the environment when
        # making requests (on their free plan).
        # This reintroduces the proxy support that is the default in requests
        # anyway.
        session.proxies = _get_proxies_from_env()
        self.session = session


    @property
    def endpoint(self):
        """Property method to calculate the correct Pusher API host"""
        default_endpoint = '{}.pushnotifications.pusher.com'.format(
            self.instance_id,
        ).lower()
        return self._endpoint or default_endpoint

    def _make_request(self, method, path, path_params, body=None):
        path_params = {
            name: urllib.parse.quote(value)
            for name, value in path_params.items()
        }
        path = path.format(**path_params)
        url = _make_url(scheme='https', host=self.endpoint, path=path)

        request = requests.Request(
            method,
            url,
            json=body,
            headers={
                'host': self.endpoint,
                'authorization': 'Bearer {}'.format(self.secret_key),
                'x-pusher-library': 'pusher-push-notifications-python {}'.format(
                    SDK_VERSION,
                )
            },
        )

        response = self.session.send(request.prepare())

        if response.status_code != 200:
            try:
                error_body = response.json()
            except ValueError:
                error_body = {}
            _handle_http_error(error_body, response.status_code)

        try:
            response_body = response.json()
        except ValueError:
            response_body = None

        return response_body

    def publish(self, interests, publish_body):
        """Publish the given publish_body to the specified interests.

        Args:
            interests (list): List of interests that the publish body should
                be sent to.
            publish_body (dict): Dict containing the body of the push
                notification publish request.
                (see https://pusher.com/docs/beams/)

        Returns:
            A dict containing the publish response from the Pusher Push
            Notifications service.
            (see https://pusher.com/docs/beams/)

        Raises:
            PusherAuthError: if the secret_key is incorrect
            PusherMissingInstanceError: if the instance_id is incorrect
            PusherServerError: if the Push Notifications service returns
                an error
            PusherValidationError: if the publish_body is invalid
            TypeError: if interests is not a list
            TypeError: if publish_body is not a dict
            TypeError: if any interest is not a string
            ValueError: if len(interests) < 1
            ValueError: if len(interests) > 100
            ValueError: if any interest length is greater than the max
            ValueError: if any interest contains a forbidden character

        .. deprecated::
            Use :func:`publish_to_interests` instead.
        """
        warnings.warn(
            "publish method is deprecated. Please use publish_to_interests.",
            DeprecationWarning
        )
        return self.publish_to_interests(interests, publish_body)

    def publish_to_interests(self, interests, publish_body):
        """Publish the given publish_body to the specified interests.

        Args:
            interests (list): List of interests that the publish body should
                be sent to.
            publish_body (dict): Dict containing the body of the push
                notification publish request.
                (see https://pusher.com/docs/beams/)

        Returns:
            A dict containing the publish response from the Pusher Push
            Notifications service.
            (see https://pusher.com/docs/beams/)

        Raises:
            PusherAuthError: if the secret_key is incorrect
            PusherMissingInstanceError: if the instance_id is incorrect
            PusherServerError: if the Push Notifications service returns
                an error
            PusherValidationError: if the publish_body is invalid
            TypeError: if interests is not a list
            TypeError: if publish_body is not a dict
            TypeError: if any interest is not a string
            ValueError: if len(interests) < 1
            ValueError: if len(interests) > 100
            ValueError: if any interest length is greater than the max
            ValueError: if any interest contains a forbidden character

        """
        if not isinstance(interests, list):
            raise TypeError('interests must be a list')
        if not isinstance(publish_body, dict):
            raise TypeError('publish_body must be a dictionary')
        if not interests:
            raise ValueError('Publishes must target at least one interest')
        if len(interests) > MAX_NUMBER_OF_INTERESTS:
            raise ValueError(
                'Number of interests ({}) exceeds maximum of {}'.format(
                    len(interests),
                    MAX_NUMBER_OF_INTERESTS,
                ),
            )
        for interest in interests:
            if not isinstance(interest, six.string_types):
                raise TypeError(
                    'Interest {} is not a string'.format(interest)
                )
            if len(interest) > INTEREST_MAX_LENGTH:
                raise ValueError(
                    'Interest "{}" is longer than the maximum of {} chars'.format(
                        interest,
                        INTEREST_MAX_LENGTH,
                    )
                )
            if not INTEREST_REGEX.match(interest):
                raise ValueError(
                    'Interest "{}" contains a forbidden character. '.format(
                        interest,
                    )
                    + 'Allowed characters are: ASCII upper/lower-case letters, '
                    + 'numbers or one of _=@,.;-'
                )

        publish_body = copy.deepcopy(publish_body)
        publish_body['interests'] = interests

        response_body = self._make_request(
            method='POST',
            path='/publish_api/v1/instances/{instance_id}/publishes/interests',
            path_params={
                'instance_id': self.instance_id,
            },
            body=publish_body,
        )

        if response_body is None:
            raise PusherBadResponseError(
                'The server returned a malformed response',
            )

        return response_body

    def publish_to_users(self, user_ids, publish_body):
        """Publish the given publish_body to the specified users.

        Args:
            user_ids (list): List of ids of users that the publish body should
                be sent to.
            publish_body (dict): Dict containing the body of the push
                notification publish request.
                (see https://pusher.com/docs/beams/)

        Returns:
            A dict containing the publish response from the Pusher Push
            Notifications service.
            (see https://pusher.com/docs/beams/)

        Raises:
            PusherAuthError: if the secret_key is incorrect
            PusherMissingInstanceError: if the instance_id is incorrect
            PusherServerError: if the Push Notifications service returns
                an error
            PusherValidationError: if the publish_body is invalid
            TypeError: if user_ids is not a list
            TypeError: if publish_body is not a dict
            TypeError: if any user id is not a string
            ValueError: if len(user_ids) < 1
            ValueError: if len(user_ids) is greater than the max
            ValueError: if any user id length is greater than the max

        """
        if not isinstance(user_ids, list):
            raise TypeError('user_ids must be a list')
        if not isinstance(publish_body, dict):
            raise TypeError('publish_body must be a dictionary')
        if not user_ids:
            raise ValueError('Publishes must target at least one user')
        if len(user_ids) > MAX_NUMBER_OF_USER_IDS:
            raise ValueError(
                'Number of user ids ({}) exceeds maximum of {}'.format(
                    len(user_ids),
                    MAX_NUMBER_OF_USER_IDS,
                ),
            )
        for user_id in user_ids:
            if not isinstance(user_id, six.string_types):
                raise TypeError(
                    'User id {} is not a string'.format(user_id)
                )
            if len(user_id) > USER_ID_MAX_LENGTH:
                raise ValueError(
                    'User id "{}" is longer than the maximum of {} chars'.format(
                        user_id,
                        USER_ID_MAX_LENGTH,
                    )
                )

        publish_body = copy.deepcopy(publish_body)
        publish_body['users'] = user_ids

        response_body = self._make_request(
            method='POST',
            path='/publish_api/v1/instances/{instance_id}/publishes/users',
            path_params={
                'instance_id': self.instance_id,
            },
            body=publish_body,
        )

        if response_body is None:
            raise PusherBadResponseError(
                'The server returned a malformed response',
            )

        return response_body

    def generate_token(self, user_id):
        """Generate an auth token which will allow devices to associate
        themselves with the given user id

        Args:
            user_id (string): user id for which the token will be valid

        Returns:
            Beams token wrapped in dictionary for json serialization (dict)

        Raises:
            TypeError: if user_id is not a string
            ValueError: is user_id is longer than the maximum of 164 chars

        """
        if not isinstance(user_id, six.string_types):
            raise TypeError('user_id must be a string')
        if len(user_id) > USER_ID_MAX_LENGTH:
            raise ValueError('user_id longer than the maximum of 164 chars')

        issuer = 'https://{}.pushnotifications.pusher.com'.format(self.instance_id)

        now = datetime.datetime.utcnow()
        expiry_datetime = now + AUTH_TOKEN_DURATION
        expiry_timestamp = int(time.mktime(expiry_datetime.timetuple()))

        token = jwt.encode(
            {
                'iss': issuer,
                'sub': user_id,
                'exp': expiry_timestamp,
            },
            self.secret_key,
            algorithm='HS256',
        )
        token = six.ensure_text(token)

        return {
            'token': token,
        }

    def delete_user(self, user_id):
        """Remove the user with the given ID (and all of their devices) from
        the Pusher Beams database. The user will no longer receive any
        notifications. This action cannot be undone.

        Args:
            user_id (string): id of the user to be deleted

        Returns:
            None

        Raises:
            TypeError: if user_id is not a string
            ValueError: is user_id is longer than the maximum of 164 chars

        """
        if not isinstance(user_id, six.string_types):
            raise TypeError('user_id must be a string')
        if len(user_id) > USER_ID_MAX_LENGTH:
            raise ValueError('user_id longer than the maximum of 164 chars')

        self._make_request(
            method='DELETE',
            path='/customer_api/v1/instances/{instance_id}/users/{user_id}',
            path_params={
                'instance_id': self.instance_id,
                'user_id': user_id,
            },
        )
