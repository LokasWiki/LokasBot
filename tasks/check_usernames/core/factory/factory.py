from pywikibot import config as _config

from tasks.check_usernames.core.connection.mysql_connection import MySQLBaseConnection
from tasks.check_usernames.core.persistence.mysql_persistence import MySQLPersistence
from tasks.check_usernames.core.repositories.mysql_repository import MySQLRepository


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
