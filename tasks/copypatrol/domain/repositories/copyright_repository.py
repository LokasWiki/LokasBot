from abc import ABC, abstractmethod


class CopyrightRepository(ABC):
    @abstractmethod
    def count_open_cases(self, lang: str, project: str) -> int:
        """
        Counts the number of open cases for a given language and project.

        Args:
            lang (str): The language for which to count open cases.
            project (str): The project for which to count open cases.

        Returns:
            int: The count of open cases.
        """
        pass
