from abc import ABC, abstractmethod


class BaseConnection(ABC):
    """
    Abstract base class for connection operations with databases and APIs.
    This interface provides methods for connecting, disconnecting, and checking the connection status.

    Implementations of this interface can be used with MySQL, SQLite, or other databases,
    as well as with API setups.
    """

    @abstractmethod
    def connect(self):
        """
        Connects to the database or API.

        Raises:
            ConnectionError: If the connection fails.
        """
        pass

    @abstractmethod
    def disconnect(self):
        """
        Disconnects from the database or API.
        """
        pass

    @abstractmethod
    def check(self):
        """
        Checks the connection status.

        Returns:
            bool: True if the connection is active, False otherwise.
        """
        pass
