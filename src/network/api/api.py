import os

from flask import Flask
from flask_cors import CORS
from waitress import serve

from src.network.api.config.queries.ip_queries import ip_bp
from src.network.api.config.queries.prog_queries import prog_bp
from src.network.api.consts import CLASSNAME
from src.network.api.login.login import login_bp
from src.network.api.middleware.middleware import Middleware
from src.shared.logs.logs import Logs

BLUEPRINTS = [prog_bp, login_bp, ip_bp]


class Api:
    def __init__(self):
        app = Flask(__name__, instance_relative_config=True)
        Logs.info(CLASSNAME, 'init')

        for bp in BLUEPRINTS:
            app.register_blueprint(bp)

        this_files_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(this_files_dir)
        app.wsgi_app = Middleware(app.wsgi_app)
        CORS(app)

        self.application = app

    def start(self):
        Logs.info(CLASSNAME, 'Started')
        serve(self.application, host='0.0.0.0', port=5000, url_prefix='/')

    def start_debug(self):
        Logs.info(CLASSNAME, 'Started')
        self.application.run(host='0.0.0.0')
