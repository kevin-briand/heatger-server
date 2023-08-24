"""API Client"""
import os

from flask import Flask, jsonify
from flask_cors import CORS
from waitress import serve

from src.network.api.config.queries.ip.ip_queries import ip_bp
from src.network.api.config.queries.prog.prog_queries import prog_bp
from src.network.api.consts import CLASSNAME
from src.network.api.errors.api_error import ApiError
from src.network.api.login.query.login_query import login_bp
from src.network.api.middleware.middleware import Middleware
from src.shared.logs.logs import Logs

BLUEPRINTS = [prog_bp, login_bp, ip_bp]


class Api:
    """API Class"""
    def __init__(self):
        app = Flask(__name__, instance_relative_config=True)
        Logs.info(CLASSNAME, 'init')

        for bp in BLUEPRINTS:
            app.register_blueprint(bp)

        this_files_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(this_files_dir)
        app.wsgi_app = Middleware(app.wsgi_app)
        CORS(app)
        app.register_error_handler(ApiError, self.api_error)

        self.application = app

    def start(self):
        """Start API server with waitress"""
        Logs.info(CLASSNAME, 'Started')
        serve(self.application, host='0.0.0.0', port=5000, url_prefix='/')

    def start_debug(self):
        """Start flask API server"""
        Logs.info(CLASSNAME, 'Started')
        self.application.run(host='0.0.0.0')

    @staticmethod
    def api_error(error: ApiError):
        """Return a json version of exception"""
        return jsonify(error.to_dict()), error.status_code
