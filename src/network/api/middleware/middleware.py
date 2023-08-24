"""Api Middleware"""
from flask import Response
from werkzeug.wrappers import Request

from src.localStorage.persistence.persistence import Persistence


class Middleware:
    """WSGI middleware"""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        if request.method == 'OPTIONS' or self.check_auth(request):
            return self.app(environ, start_response)
        response = Response('Token is not valid !', status=401)
        return response(environ, start_response)

    @staticmethod
    def check_auth(request):
        """used for control if the token is valid"""
        auth = request.headers.get('Authorization', None)
        if request.path == '/login':
            return True
        if not auth:
            return False
        if auth != Persistence().get_api_token():
            return False
        return True
