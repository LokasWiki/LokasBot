from abc import ABC, abstractmethod


class BasePersistence(ABC):
    @abstractmethod
    def select(self, query: str, params=None):
        """
        Executes a SELECT query and returns the result as a list of rows.

        Parameters:
            query (str): The SQL query string to execute.
            params (tuple or dict, optional): Parameters for the query (default: None).

        Returns:
            list: A list of rows returned by the query.
        """
        pass

    @abstractmethod
    def select_one(self, query: str, params=None):
        """
        Executes a SELECT query and returns a single row.

        Parameters:
            query (str): The SQL query string to execute.
            params (tuple or dict, optional): Parameters for the query (default: None).

        Returns:
            tuple or None: A single row returned by the query or None if no rows are found.
        """
        pass

    @abstractmethod
    def delete(self, query: str, params=None):
        """
        Executes a DELETE query.

        Parameters:
            query (str): The SQL query string to execute.
            params (tuple or dict, optional): Parameters for the query (default: None).
        """
        pass

    @abstractmethod
    def update(self, query: str, params=None):
        """
        Executes an UPDATE query.

        Parameters:
            query (str): The SQL query string to execute.
            params (tuple or dict, optional): Parameters for the query (default: None).
        """
        pass
