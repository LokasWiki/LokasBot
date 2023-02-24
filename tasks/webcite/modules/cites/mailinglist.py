from tasks.webcite.modules.cites.cite import BaseCite


class MailingList(BaseCite):
    def __init__(self, template):
        super().__init__(template)
