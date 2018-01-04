Pusher Push Notifications Python server SDK
===========================================

Installation
------------
The Pusher Notifications Python server SDK is available on PyPi
`here <http://www.python.org/>`_.

You can install this SDK by using
`pip <https://pip.pypa.io/en/stable/installing/`_:

.. code:: bash

    $ pip install pusher_push_notifications


Usage
-----

Configuring the SDK for Your Instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use your instance id and secret (you can get these from the
`dashboard <https://dash.pusher.com>`_) to create a PushNotifications instance:

.. code:: python

  import PushNotifications from pusher_push_notifications

  pn_client = PushNotifications(
      instance_id='YOUR_INSTANCE_ID_HERE',
      secret_key='YOUR_SECRET_KEY_HERE',
  )

Publishing a Notification
~~~~~~~~~~~~~~~~~~~~~~~~~

Once you have created your PushNotifications instance you can publish a push notification to your registered & subscribed devices:
.. code:: python

  response = pn_client.publish({'interests': ['hello'], 'apns': {'aps': {'alert': 'Hello!'}}})

  print(response['publishId'])
