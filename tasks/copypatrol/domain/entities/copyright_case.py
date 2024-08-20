class CopyrightCase:
    def __init__(self, id, lang, project, status):
        """
        Initializes a new instance of the CopyrightCase class.

        Parameters:
            id (int): The ID of the copyright case.
            lang (str): The language of the copyright case.
            project (str): The project of the copyright case.
            status (str): The status of the copyright case.
        """
        self.id = id
        self.lang = lang
        self.project = project
        self.status = status
