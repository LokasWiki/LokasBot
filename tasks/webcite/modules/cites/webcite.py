from tasks.webcite.modules.cites.cite import BaseCite


class WebBaseCite(BaseCite):
    """Class representing a {{استشهاد ويب}} template"""
    def __init__(self, template):
        super().__init__(template)