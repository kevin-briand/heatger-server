from src.localStorage.persistence.persistence import Persistence
from test.helpers.fixtures.localStorage.persistence.persistence_dto_fixture import persistence_dto_fixture
from test.helpers.patchs.local_storage_patch import LocalStoragePatch


class PersistencePatch(LocalStoragePatch):
    _datas = None

    @classmethod
    def start_patch(cls, test):
        cls._datas = persistence_dto_fixture()
        Persistence._initialized = False
        super().start_patch(test)
        Persistence()
