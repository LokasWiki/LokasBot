from abc import ABC, abstractmethod


class BaseRepository(ABC):

    @abstractmethod
    def createUserTable(self):
        pass

    @abstractmethod
    def selectAllUsers(self, query: str, params=None):
        """
        Executes a SELECT query and returns the results.

        :param query: The SQL query to execute.
        :type query: str
        :param params: Optional parameters to be substituted in the query.
        :type params: Union[None, tuple]

        :return: The results of the query.
        :rtype: Any
        """
        pass

    @abstractmethod
    def deleteAllUsers(self):
        """
        Deletes all users from the database.
        """
        pass
