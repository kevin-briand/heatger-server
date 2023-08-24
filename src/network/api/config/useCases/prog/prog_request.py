"""Prog requests"""
import json
from typing import Optional

from src.localStorage.config.config import Config
from src.localStorage.errors.local_storage_error import LocalStorageError
from src.localStorage.jsonEncoder.json_encoder import JsonEncoder
from src.network.api.errors.api_error import ApiError
from src.network.api.errors.empty_data_error import EmptyDataError
from src.network.api.errors.not_found_error import NotFoundError
from src.zone.dto.schedule_dto import ScheduleDto


class ProgRequest:
    """Prog requests class, return a json list of ScheduleDto"""
    @staticmethod
    def get_by_zone_id(zone_id: str):
        """return all ScheduleDto"""
        ProgRequest.__is_zone_exist(zone_id)
        try:
            return json.dumps(getattr(Config().get_config(), zone_id).prog, cls=JsonEncoder)
        except LocalStorageError as exc:
            raise ApiError(str(exc)) from exc

    @staticmethod
    def add(zone_id: str, data: list):
        """add a new ScheduleDto in list, return list of all ScheduleDto"""
        ProgRequest.__is_zone_exist(zone_id)
        if not data:
            raise EmptyDataError()
        try:
            Config().add_schedules(zone_id, ScheduleDto.from_array(data))
            return ProgRequest.get_by_zone_id(zone_id)
        except LocalStorageError as exc:
            raise ApiError(str(exc)) from exc

    @staticmethod
    def remove(zone_id: str, data: str):
        """remove an ScheduleDto in zone, return a list of all ScheduleDto in zone"""
        ProgRequest.__is_zone_exist(zone_id)
        try:
            prog = getattr(Config().get_config(), zone_id).prog
            result_schedule: Optional[ScheduleDto] = None
            for schedule in prog:
                if schedule.to_value() == int(data):
                    result_schedule = schedule
                    break
            if result_schedule is None:
                raise NotFoundError(f"{data} in {zone_id}")
            Config().remove_schedule(zone_id, result_schedule)
            return ProgRequest.get_by_zone_id(zone_id)
        except LocalStorageError as exc:
            raise ApiError(str(exc)) from exc

    @staticmethod
    def remove_all(zone_id: str):
        """remove all ScheduleDto in zone, return an empty list"""
        ProgRequest.__is_zone_exist(zone_id)
        try:
            Config().remove_all_schedule(zone_id)
            return ProgRequest.get_by_zone_id(zone_id)
        except LocalStorageError as exc:
            raise ApiError(str(exc)) from exc

    @staticmethod
    def __is_zone_exist(zone_id: str):
        """if the zone doesn't exist raise a NotFoundError"""
        if not hasattr(Config().get_config(), zone_id):
            raise NotFoundError("zone")
