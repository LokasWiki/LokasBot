import re
import wikitextparser as wtp


class PortalsMerge:
    def __init__(self, page, text, summary):
        self.page = page
        self.text = text
        self.summary = summary
        self.list_of_templates = [
            "صندوق بوابات",
            "Portal box",
            "مجموعة بوابات",
            "Portail",
            "وصلة بوابة",
            "صندوق بوابة",
            "Portal bar",
            "شب",
            "شريط بوابة",
            "شريط البوابات",
            "شريط بوابات",
            "بوابة",
            "Portal"
        ]
        self.list_of_needed_templates = [
            "مقالات بحاجة لشريط بوابات"
        ]

    def __call__(self):
        pass
