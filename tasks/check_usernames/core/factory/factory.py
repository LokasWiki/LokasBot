from pywikibot import config as _config

from tasks.check_usernames.core.connection.mysql_connection import MySQLBaseConnection
from tasks.check_usernames.core.connection.sqlite_connection import SQLiteBaseConnection
from tasks.check_usernames.core.persistence.mysql_persistence import MySQLPersistence
from tasks.check_usernames.core.persistence.sqlite_persistence import SQLitePersistence
from tasks.check_usernames.core.repositories.mysql_repository import MySQLRepository
from tasks.check_usernames.core.repositories.sqlite_repository import SQLiteRepository


class DatabaseFactory:
    def create_mysql_repository(self) -> MySQLRepository:
        connection = MySQLBaseConnection(
            host=_config.db_hostname_format.format("arwiki"),
            port=_config.db_port,
            database=_config.db_name_format.format("arwiki"),
            db_connect_file=_config.db_connect_file,
        )
        connection.connect()
        return MySQLRepository(
            persistence=MySQLPersistence(
                connection=connection
            )
        )

    def create_sqlite_memory_repository(self) -> SQLiteRepository:
        connection = SQLiteBaseConnection(
            # database_file="file::memory:?cache=shared",
            database_file="/home/lokas/PycharmProjects/pythonProject3/code/tasks/check_usernames/core/demo.db",
        )
        connection.connect()
        return SQLiteRepository(
            persistence=SQLitePersistence(
                connection=connection
            )
        )
