from src.localStorage.config.config import Config
from test.helpers.fixtures.localStorage.config.config_dto_fixture import config_dto_fixture
from test.helpers.patchs.local_storage_patch import LocalStoragePatch


class ConfigPatch(LocalStoragePatch):
    _datas = None

    @classmethod
    def start_patch(cls, test):
        cls._datas = config_dto_fixture()
        Config._initialized = False
        super().start_patch(test)
        Config()
