from tasks.webcite.modules.cites.cite import BaseCite


class PressRelease(BaseCite):
    def __init__(self, template):
        super().__init__(template)

