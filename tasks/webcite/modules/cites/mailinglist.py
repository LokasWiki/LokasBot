from tasks.webcite.modules.cites.cite import BaseCite


class MailingList(BaseCite):
    """Class representing a {{استشهاد بقائمة بريدية}} template"""
    def __init__(self, template):
        super().__init__(template)
