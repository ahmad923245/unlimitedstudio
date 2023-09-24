"""
WSGI config for wi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unlimitedstudio.settings')

application = get_wsgi_application()

from booking.socket import sio
import socketio
application = socketio.WSGIApp(sio, application)


import eventlet
import eventlet.wsgi
eventlet.wsgi.server(eventlet.listen(('', 8083)), application)

