from tasks.copypatrol.domain.repositories.copyright_repository import CopyrightRepository


class GetOpenCases:
    def __init__(self, repository: CopyrightRepository):
        """
        Initializes a new instance of the class.

        :param repository: An instance of the CopyrightRepository class.
        :type repository: CopyrightRepository
        """
        self.repository = repository

    def execute(self, lang: str, project: str) -> int:
        """
        Executes the count_open_cases method of the repository with the given language and project parameters.

        :param lang: A string representing the language for which to count open cases.
        :type lang: str
        :param project: A string representing the project for which to count open cases.
        :type project: str
        :return: An integer representing the count of open cases.
        :rtype: int
        """
        return self.repository.count_open_cases(lang, project)
