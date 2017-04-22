"""
WSGI config for ask_remizov project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from cgi import parse_qs

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ask_remizov.settings")

application = get_wsgi_application()


def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    args = parse_qs(environ['QUERY_STRING'])
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    yield ('Hello world\n' + str(environ['REQUEST_METHOD']) + ' '
          + str(environ['PATH_INFO']) + ' ' + str(environ['SERVER_PROTOCOL']) + '\n' + str(args))

