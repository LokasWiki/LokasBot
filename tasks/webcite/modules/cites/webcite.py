"""
This module contains the News class, which represents a {{استشهاد ويب}} template.
"""

from tasks.webcite.modules.cites.module import BaseCite


class WebCite(BaseCite):
    """Class representing a {{استشهاد ويب}} template"""

    def __init__(self, template):
        super().__init__(template)
