.. image:: https://travis-ci.org/pusher/push-notifications-python.svg?branch=master
   :target: https://travis-ci.org/pusher/push-notifications-python

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

  pn_client = PushNotifications(
      instance_id='YOUR_INSTANCE_ID_HERE',
      secret_key='YOUR_SECRET_KEY_HERE',
  )

Publishing a Notification
~~~~~~~~~~~~~~~~~~~~~~~~~

Once you have created your Beams PushNotifications instance you can publish a push notification to your registered & subscribed devices:

.. code::

  response = pn_client.publish(
      interests=['hello'],
      publish_body={'apns': {'aps': {'alert': 'Hello!'}}, 'fcm': {'notification': {'title': 'Hello', 'body': 'Hello, World!'}}}
  )

  print(response['publishId'])
