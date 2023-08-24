from src.network.api.dto.api_dto import ApiDto


def api_dto_fixture() -> ApiDto:
    return ApiDto("admin", "password")
