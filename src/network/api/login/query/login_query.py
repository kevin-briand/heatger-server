"""API Login Blueprint"""
from flask import Blueprint, request

from src.network.api.login.useCase.login_request import LoginRequest

login_bp = Blueprint('login', __name__)


@login_bp.post("/login")
def login():
    """Login endpoint, return a token"""
    return LoginRequest.login(request.json)
