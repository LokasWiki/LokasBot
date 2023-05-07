import copy

import wikitextparser as wtp

from core.utils.helpers import prepare_str


class RemovePortal:
    def __init__(self, page_text, portal):
        self.page_text = page_text
        self.portal = portal
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
        self.tem_text = copy.deepcopy(self.page_text)

    def start_remove(self):
        parsed = wtp.parse(self.page_text)
        for template in self.list_of_templates:
            for template_page in parsed.templates:
                temp_template = copy.deepcopy(template_page)
                if prepare_str(template_page.name) == prepare_str(template):
                    for arg in template_page.arguments:
                        try:
                            if prepare_str(arg.value) == prepare_str(self.portal):
                                temp_template = str(temp_template).replace(str(arg), "")
                        except:
                            pass
                self.tem_text = str(self.tem_text).replace(str(template_page), str(temp_template))

#
# site = pywikibot.Site()
# page_name = "الشعبية (خرطوم بحري)"
# page = pywikibot.Page(site, page_name)
# obj = RemovePortal(page.text, "الخرطوم بحري")
# obj.start_remove()
# print(obj.tem_text)
