"""
This module contains the News class, which represents a {{استشهاد بخبر}} template.
"""
from tasks.webcite.modules.cites.module import BaseCite


class News(BaseCite):
    """Class representing a {{استشهاد بخبر}} template"""
    def __init__(self, template):
        super().__init__(template)
