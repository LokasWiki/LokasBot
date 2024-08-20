from tasks.copypatrol.data.database import Database
from tasks.copypatrol.domain.repositories.copyright_repository import CopyrightRepository


class MySQLCopyrightRepository(CopyrightRepository):
    def __init__(self, database: Database):
        """
        Initializes the MySQLCopyrightRepository object with the given Database object.

        :param database: A Database object representing the database connection.
        :type database: Database
        """
        self.database = database

    def count_open_cases(self, lang: str, project: str) -> int:
        """
        Counts the number of open cases in the copyright_diffs table for a given language and project.

        Parameters:
            lang (str): The language of the cases.
            project (str): The project of the cases.

        Returns:
            int: The number of open cases.
        """
        query = 'SELECT COUNT(id) FROM copyright_diffs WHERE lang=%s AND project=%s AND status IS NULL'
        result = self.database.execute_query(query, (lang, project))
        return result[0] if result else 0
