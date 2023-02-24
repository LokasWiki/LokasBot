from tasks.webcite.modules.cites.cite import BaseCite


class Newsgroup(BaseCite):
    """Class representing a {{استشهاد بمجموعة أخبار}} template"""
    def __init__(self, template):
        super().__init__(template)

