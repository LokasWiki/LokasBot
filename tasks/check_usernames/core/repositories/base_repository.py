from abc import ABC, abstractmethod


class BaseRepository(ABC):
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
