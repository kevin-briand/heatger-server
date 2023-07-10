from werkzeug.wrappers import Request, Response

from src.localStorage.persistence import Persistence
from src.network.api.consts import API_TOKEN


class Middleware:
    """Simple WSGI middleware"""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        if request.method == 'OPTIONS' or self.check_auth(request):
            return self.app(environ, start_response)

        res = Response(u'Authorization failed', mimetype='text/plain', status=401)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res(environ, start_response)

    @staticmethod
    def check_auth(request):
        auth = request.headers.get('Authorization', None)
        if request.path == '/login':
            return True
        if not auth:
            return False
        elif auth != Persistence().get_value(API_TOKEN):
            return False
        return True
