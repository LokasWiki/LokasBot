class PageEntity:
    def __init__(self, title: str, text: str, summary: str):
        """
        Initializes a new instance of the `PageEntity` class.

        Args:
            title (str): The title of the page.
            text (str): The text content of the page.
            summary (str): A summary of the page.

        Returns:
            None
        """
        self.title = title
        self.text = text
        self.summary = summary
