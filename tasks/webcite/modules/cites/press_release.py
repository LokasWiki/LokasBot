"""
This module contains the News class, which represents a {{استشهاد ببيان صحفي}} template.
"""

from tasks.webcite.modules.cites.module import BaseCite


class PressRelease(BaseCite):
    """Class representing a {{استشهاد ببيان صحفي}} template"""

    def __init__(self, template):
        super().__init__(template)
