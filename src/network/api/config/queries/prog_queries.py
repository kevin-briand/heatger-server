"""Prog API blueprint"""
import json
from typing import Optional

from flask import abort, Blueprint, request

from src.localStorage.config import Config
from src.localStorage.jsonEncoder.file_encoder import FileEncoder
from src.zone.dto.horaire_dto import HoraireDto

prog_bp = Blueprint('prog', __name__)


@prog_bp.get("/prog/<zone>")
def get_prog(zone=None):
    """return an array of prog corresponding of zone"""
    try:
        return json.dumps(getattr(Config().get_config(), zone).prog, cls=FileEncoder)
    except AttributeError:
        abort(404)


@prog_bp.post("/prog/<zone>")
def post_prog(zone=None):
    """add a list of prog in the zone, return an array of prog corresponding of zone"""
    if request.json is not None:
        try:
            Config().add_horaires(zone, HoraireDto.array_to_horaire(request.json))
            return json.dumps(getattr(Config().get_config(), zone).prog, cls=FileEncoder)
        except AttributeError:
            abort(404)
    abort(400)


@prog_bp.delete("/prog/<zone>/<value>")
def delete_prog(zone, value: str):
    """remove prog of zone, return an array of prog corresponding of zone"""
    try:
        prog = getattr(Config().get_config(), zone).prog
        result_horaire: Optional[HoraireDto] = None
        for horaire in prog:
            if horaire.to_value() == int(value):
                result_horaire = horaire
                break
        if result_horaire is None:
            abort(404)
        Config().remove_horaire(zone, result_horaire)
        return json.dumps(getattr(Config().get_config(), zone).prog, cls=FileEncoder)
    except AttributeError:
        abort(404)


@prog_bp.delete("/prog/<zone>")
def delete_all_prog(zone):
    """remove all prog of zone, return an array of prog corresponding of zone"""
    try:
        Config().remove_all_horaire(zone)
        return json.dumps(getattr(Config().get_config(), zone).prog, cls=FileEncoder)
    except AttributeError:
        abort(404)
