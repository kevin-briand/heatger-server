import json
from typing import Optional

from flask import abort, Blueprint, request

from src.localStorage.config import Config
from src.localStorage.jsonEncoder.file_encoder import FileEncoder
from src.network.dto.ip_dto import IpDto

ip_bp = Blueprint('ip', __name__)


@ip_bp.get("/ip")
def get_ip():
    try:
        return json.dumps(Config().get_config().network.ip, cls=FileEncoder)
    except TypeError:
        abort(404)


@ip_bp.post("/ip")
def post_ip():
    if request.json is not None:
        try:
            Config().add_ip(IpDto.object_to_ip_dto(request.json))
            return json.dumps(Config().get_config().network.ip, cls=FileEncoder)
        except TypeError:
            abort(404)


@ip_bp.delete("/ip/<ip>")
def delete_ip(ip: str):
    result_ip: IpDto = Optional[None]
    for ip_in_config in Config().get_config().network.ip:
        if ip_in_config.ip == ip:
            result_ip = ip_in_config
            break
    if result_ip is None:
        abort(404)

    Config().remove_ip(result_ip)
    return json.dumps(Config().get_config().network.ip, cls=FileEncoder)
