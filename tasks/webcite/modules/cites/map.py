from tasks.webcite.modules.cites.cite import BaseCite


class CiteMap(BaseCite):
    """Class representing a {{استشهاد بخريطة}} template"""
    def __init__(self, template):
        super().__init__(template)

