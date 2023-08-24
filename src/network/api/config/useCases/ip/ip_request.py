"""Ip Requests"""
import json
from typing import Optional

from src.localStorage.config.config import Config
from src.localStorage.errors.local_storage_error import LocalStorageError
from src.localStorage.jsonEncoder.json_encoder import JsonEncoder
from src.network.api.errors.api_error import ApiError
from src.network.api.errors.empty_data_error import EmptyDataError
from src.network.api.errors.not_found_error import NotFoundError
from src.network.dto.ip_dto import IpDto


class IpRequest:
    """Ip requests class, return a json list of IpDto"""
    @staticmethod
    def get_all():
        """return all IpDto"""
        try:
            return json.dumps(Config().get_config().network.ip, cls=JsonEncoder)
        except LocalStorageError as exc:
            raise ApiError(str(exc)) from exc

    @staticmethod
    def add(data: str):
        """add a new IpDto in list, return list of all IpDto"""
        if not data:
            raise EmptyDataError()
        try:
            Config().add_ip(IpDto.object_to_ip_dto(data))
            return IpRequest.get_all()
        except LocalStorageError as exc:
            raise ApiError(str(exc)) from exc

    @staticmethod
    def remove(ip: str):
        """remove an IpDto in list, return list of all IpDto"""
        try:
            result_ip: Optional[IpDto] = None
            for ip_in_config in Config().get_config().network.ip:
                if ip_in_config.ip == ip:
                    result_ip = ip_in_config
                    break
            if result_ip is None:
                raise NotFoundError(ip)
            Config().remove_ip(result_ip)
            return IpRequest.get_all()
        except LocalStorageError as exc:
            raise ApiError(str(exc)) from exc
