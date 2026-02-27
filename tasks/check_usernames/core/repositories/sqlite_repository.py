from abc import ABC
from typing import List

from tasks.check_usernames.core.models.user import User
from tasks.check_usernames.core.persistence.base_persistence import BasePersistence
from tasks.check_usernames.core.repositories.base_repository import BaseRepository


class SQLiteRepository(BaseRepository, ABC):
    def __init__(self, persistence: BasePersistence):
        self.persistence = persistence

    def selectAllUsers(self, query: str, params=None):
        pass

    def createUserTable(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_name TEXT NOT NULL UNIQUE,
            created_at DATETIME NOT NULL,
            status INTEGER
        )
        """
        self.persistence.execute(query=query)

    def deleteAllUsers(self):
        query = "DELETE FROM users"
        self.persistence.delete(query=query)

    def saveUsers(self, users: List[User]):
        for user in users:
            query = """ INSERT INTO users 
            (user_name, created_at, status)
             VALUES 
             ('{}', '{}', {})
            """.format(user.user_name, user.created_at, user.status)
            self.persistence.execute(query=query)
