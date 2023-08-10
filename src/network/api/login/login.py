"""API Login Blueprint"""
import json
from uuid import uuid4

from flask import Blueprint, request, Response, abort

from src.localStorage.config.config import Config
from src.localStorage.persistence.persistence import Persistence

login_bp = Blueprint('login', __name__)


@login_bp.post("/login")
def login():
    """Login endpoint, return a token"""
    if request.json is not None:
        user = request.json
        api = Config().get_config().api
        if api.username == user['username'] and api.password == user['password']:
            Persistence().set_api_token(str(uuid4()))
            return json.dumps(Persistence().get_api_token())
        resp = Response(response="wrong username/password", status=401, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return abort(400)
