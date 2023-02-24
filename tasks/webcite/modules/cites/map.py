"""
This module contains the News class, which represents a {{استشهاد بخريطة}} template.
"""

from tasks.webcite.modules.cites.module import BaseCite


class CiteMap(BaseCite):
    """Class representing a {{استشهاد بخريطة}} template"""

    def __init__(self, template):
        super().__init__(template)
