"""Prog API blueprint"""
from flask import Blueprint, request

from src.network.api.config.useCases.prog.prog_request import ProgRequest

prog_bp = Blueprint('prog', __name__)


@prog_bp.get("/prog/<zone_id>")
def get_prog(zone_id: str):
    """return an array of prog corresponding of zone"""
    print("get")
    return ProgRequest.get_by_zone_id(zone_id)


@prog_bp.post("/prog/<zone_id>")
def post_prog(zone_id=None):
    """add a list of prog in the zone, return an array of prog corresponding of zone"""
    return ProgRequest.add(zone_id, request.json)


@prog_bp.delete("/prog/<zone_id>/<value>")
def delete_prog(zone_id: str, value: str):
    """remove prog of zone, return an array of prog corresponding of zone"""
    return ProgRequest.remove(zone_id, value)


@prog_bp.delete("/prog/<zone_id>")
def delete_all_prog(zone_id: str):
    """remove all prog of zone, return an array of prog corresponding of zone"""
    return ProgRequest.remove_all(zone_id)
