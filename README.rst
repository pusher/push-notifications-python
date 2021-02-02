.. image:: https://github.com/pusher/push-notifications-python/workflows/CI/badge.svg
   :target: https://github.com/pusher/push-notifications-python/actions?query=branch%3Amaster
.. image:: https://codecov.io/gh/pusher/push-notifications-python/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/pusher/push-notifications-python

Pusher Beams Python server SDK
==============================
Full documentation for this SDK can be found `here <https://docs.pusher.com/beams/reference/server-sdk-python>`__

Installation
------------
The Pusher Beams Python server SDK is available on PyPi
`here <https://pypi.python.org/pypi/pusher_push_notifications/>`__.

You can install this SDK by using
`pip <https://pip.pypa.io/en/stable/installing/>`__:

.. code::

    $ pip install pusher_push_notifications


Usage
-----

Configuring the SDK for Your Instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use your instance id and secret (you can get these from the
`dashboard <https://dash.pusher.com/beams>`__) to create a Beams PushNotifications instance:

.. code::

  from pusher_push_notifications import PushNotifications

  beams_client = PushNotifications(
      instance_id='YOUR_INSTANCE_ID_HERE',
      secret_key='YOUR_SECRET_KEY_HERE',
  )

Publishing to Device Interests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can broadcast notifications to groups of subscribed devices using `Device Interests <https://docs.pusher.com/beams/concepts/device-interests>`__:

.. code::

  response = beams_client.publish_to_interests(
      interests=['hello'],
      publish_body={
          'apns': {
              'aps': {
                  'alert': 'Hello!'
              }
          },
          'fcm': {
              'notification': {
                  'title': 'Hello',
                  'body': 'Hello, World!'
              }
          }
      }
  )

  print(response['publishId'])

Publishing to Authenticated Users
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Securely send notifications to individual users of your application using `Authenticated Users <https://docs.pusher.com/beams/concepts/authenticated-users>`__:

.. code::

  response = beams_client.publish_to_users(
      user_ids=['user-0001'],
      publish_body={
          'apns': {
              'aps': {
                  'alert': 'Hello!'
              }
          },
          'fcm': {
              'notification': {
                  'title': 'Hello',
                  'body': 'Hello, World!'
              }
          }
      }
  )

  print(response['publishId'])
