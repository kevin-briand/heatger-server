from src.shared.enum.mode import Mode
from src.shared.enum.state import State
from src.zone.dto.zone_persistence_dto import ZonePersistenceDto


def zone_persistence_dto_fixture(zone_id: str) -> ZonePersistenceDto:
    return ZonePersistenceDto(zone_id, State.ECO, Mode.AUTO)
