from tasks.webcite.modules.cites.cite import BaseCite


class News(BaseCite):
    """Class representing a {{استشهاد بخبر}} template"""
    def __init__(self, template):
        super().__init__(template)
