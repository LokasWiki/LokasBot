"""
This module contains the News class, which represents a {{استشهاد بمجموعة أخبار}} template.
"""

from tasks.webcite.modules.cites.module import BaseCite


class Newsgroup(BaseCite):
    """Class representing a {{استشهاد بمجموعة أخبار}} template"""

    def __init__(self, template):
        super().__init__(template)
