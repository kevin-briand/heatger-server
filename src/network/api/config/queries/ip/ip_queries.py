"""Ip config Blueprint"""
from flask import Blueprint, request

from src.network.api.config.useCases.ip.ip_request import IpRequest

ip_bp = Blueprint('ip', __name__)


@ip_bp.get("/ip")
def get_ip():
    """Return a list of IpDto"""
    return IpRequest.get_all()


@ip_bp.post("/ip")
def post_ip():
    """Add an ip in list, return the updated list"""
    return IpRequest.add(request.json)


@ip_bp.delete("/ip/<ip>")
def delete_ip(ip: str):
    """remove an ip in list, return the updated list"""
    return IpRequest.remove(ip)
