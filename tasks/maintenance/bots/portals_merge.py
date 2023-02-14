import re

import pywikibot
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
        self.exclude_list = [
            "حد",
            "قد",
            "عرض",
            "فاصل"
        ]
        self.list_of_template_found = []

    def __call__(self):
        if self.check():
            self.merge_in_one_template()
        return self.text, self.summary

    def merge_in_one_template(self):
        new_template_option_string = ""
        list_option = []
        number_of_valid_portal = 0
        for template in self.list_of_template_found:
            self.text = self.text.replace(str(template), "")
            arguments = [arg for arg in template.arguments if arg.name.strip().lower() not in self.exclude_list]
            for arg in arguments:
                temp_arg = str(arg).lower().strip().replace(" ", "")
                if "|نمط=" in temp_arg:
                    new_template_option_string += str(arg).lower().strip()
                else:
                    if self.check_portal(arg.value):
                        number_of_valid_portal +=1
                        list_option.append(str(arg).lower().strip())

        for argument in list(set(list_option)):
            new_template_option_string += str(argument)

        new_template = "{{شريط بوابات" + new_template_option_string + "}}"
        if number_of_valid_portal:
            self.add_portal(new_template)

    def check_portal(self, portal_name):
        portal_page = pywikibot.Page(self.page.site, portal_name)
        status = False
        if portal_page.exists() and portal_page.namespace() == 100:
            if portal_page.isRedirectPage():
                target_page = portal_page.getRedirectTarget()
                if target_page.exists() and target_page.namespace() == 100:
                    status = True
            else:
                status = True
        return status

    def add_portal(self, template_name):
        category_template = '[[تصنيف:'
        if category_template in self.text:
            text = self.text.replace(category_template, template_name + '\n' + category_template, 1)
        else:
            text = self.text + '\n' + template_name
        self.text = text
        self.summary += "، فحص بوابات"

    def check(self):
        parsed = wtp.parse(self.text)
        templates_found_number = 0
        for needed_templated in self.list_of_templates:
            for template in parsed.templates:
                if needed_templated.lower() == template.normal_name().lower():
                    self.list_of_template_found.append(template)
                    templates_found_number += 1

        return bool(templates_found_number)
