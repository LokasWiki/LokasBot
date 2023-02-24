from tasks.webcite.modules.cites.cite import BaseCite


class PressRelease(BaseCite):
    """Class representing a {{استشهاد ببيان صحفي}} template"""
    def __init__(self, template):
        super().__init__(template)

