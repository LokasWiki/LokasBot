"""
This module contains the News class, which represents a {{استشهاد بقائمة بريدية}} template.
"""

from tasks.webcite.modules.cites.module import BaseCite


class MailingList(BaseCite):
    """Class representing a {{استشهاد بقائمة بريدية}} template"""
    def __init__(self, template):
        super().__init__(template)
