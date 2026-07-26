from abc import ABC

from tasks.check_usernames.core.persistence.base_persistence import BasePersistence
from tasks.check_usernames.core.repositories.base_repository import BaseRepository


class MySQLRepository(BaseRepository, ABC):
    def __init__(self, persistence: BasePersistence):
        self.persistence = persistence

    def selectAllUsers(self, query: str, params=None):
        return self.persistence.select(query, params)

    def createUserTable(self):
        pass

    def deleteAllUsers(self):
        pass
