"""Prog API blueprint"""
import json
from typing import Optional

from flask import abort, Blueprint, request

from src.localStorage.config.config import Config
from src.localStorage.config.errors.config_error import ConfigError
from src.localStorage.jsonEncoder.json_encoder import JsonEncoder
from src.zone.dto.schedule_dto import ScheduleDto

prog_bp = Blueprint('prog', __name__)


@prog_bp.get("/prog/<zone>")
def get_prog(zone=None):
    """return an array of prog corresponding of zone"""
    try:
        return json.dumps(getattr(Config().get_config(), zone).prog, cls=JsonEncoder)
    except ConfigError:
        abort(404)
    except AttributeError:
        abort(404)


@prog_bp.post("/prog/<zone>")
def post_prog(zone=None):
    """add a list of prog in the zone, return an array of prog corresponding of zone"""
    if request.json is not None:
        try:
            Config().add_schedules(zone, ScheduleDto.from_array(request.json))
            return json.dumps(getattr(Config().get_config(), zone).prog, cls=JsonEncoder)
        except ConfigError:
            abort(404)
        except AttributeError:
            abort(404)
    abort(400)


@prog_bp.delete("/prog/<zone>/<value>")
def delete_prog(zone, value: str):
    """remove prog of zone, return an array of prog corresponding of zone"""
    try:
        prog = getattr(Config().get_config(), zone).prog
        result_schedule: Optional[ScheduleDto] = None
        for horaire in prog:
            if horaire.to_value() == int(value):
                result_schedule = horaire
                break
        if result_schedule is None:
            abort(404)
        Config().remove_schedule(zone, result_schedule)
        return json.dumps(getattr(Config().get_config(), zone).prog, cls=JsonEncoder)
    except ConfigError:
        abort(404)
    except AttributeError:
        abort(404)


@prog_bp.delete("/prog/<zone>")
def delete_all_prog(zone):
    """remove all prog of zone, return an array of prog corresponding of zone"""
    try:
        Config().remove_all_schedule(zone)
        return json.dumps(getattr(Config().get_config(), zone).prog, cls=JsonEncoder)
    except ConfigError:
        abort(404)
