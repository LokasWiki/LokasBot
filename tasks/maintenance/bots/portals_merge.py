import logging

import pywikibot
import wikitextparser as wtp

from core.utils.helpers import prepare_str
from core.utils.lua_to_python import get_lue_table, LuaToPython, portal_aliases_file_name


class PortalsMerge:
    def __init__(self, page, text, summary, ltp=None):
        self.page = page
        self.text = text
        self.tem_text = text
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
        self.change_summary = True

        if ltp is None:
            self.ltp = LuaToPython(get_lue_table(portal_aliases_file_name))
        else:
            self.ltp = ltp

    def __call__(self):
        print("starts")
        if self.ignore():
            return self.text, self.summary

        if self.check():
            self.merge_in_one_template()
            if self.change_summary:
                self.summary += "، فحص بوابات"
        return self.text, self.summary

    def merge_in_one_template(self):
        new_template_option_string = ""
        temp_template_option_string = ""

        list_option = []
        number_of_valid_portal = 0

        for template in self.list_of_template_found:
            self.text = self.text.replace(str(template), "")
            # for test
            tem_arguments = [arg for arg in template.arguments if arg.name.strip().lower()]
            for t_argument in tem_arguments:
                temp_template_option_string += str(t_argument).lower().strip()
            # for merge
            arguments = [arg for arg in template.arguments if arg.name.strip().lower() not in self.exclude_list]
            for arg in arguments:
                temp_arg = str(arg).lower().strip().replace(" ", "")
                if "|نمط=" in temp_arg:
                    new_template_option_string += str(arg).lower().strip()
                else:
                    if len(str(arg).lower().strip()) > 1:
                        status, name = self.check_portal(arg.value)
                        if status:
                            number_of_valid_portal += 1
                            list_option.append(f"|{name}")

        for argument in list(set(list_option)):
            new_template_option_string += str(argument)

        new_template = "{{شريط بوابات" + new_template_option_string + "}}"
        temp_template = "{{شريط بوابات" + temp_template_option_string + "}}"

        if len(new_template) == len(temp_template) and len(self.list_of_template_found) == 1 and \
                prepare_str(self.list_of_template_found[0].normal_name()) == prepare_str("شريط بوابات"):
            self.text = self.tem_text
            self.change_summary = False
        elif number_of_valid_portal:
            self.add_portal(new_template)

    def check_portal(self, portal_name):
        portal_page = pywikibot.Page(self.page.site, f"بوابة:{portal_name}")
        name = portal_name
        status = False

        try:
            if portal_page.exists():
                if portal_page.namespace() == 100:
                    if portal_page.isRedirectPage():
                        target_page = portal_page.getRedirectTarget()
                        if target_page.exists():
                            if target_page.namespace() == 100:
                                status = True
                                name = target_page.title(with_ns=False)
                    else:
                        status = True
                        name = portal_page.title(with_ns=False)
        except Exception as e:
            logging.exception(e)

        if not status:
            search_staus = self.ltp.search(portal_name)
            if search_staus is not None:
                status = True
                name = search_staus
        return status, name

    def add_portal(self, template_name):

        stub_template = '{{بذرة'
        if stub_template in self.text:
            text = self.text.replace(stub_template, template_name + '\n' + stub_template, 1)
        else:
            category_template = '[[تصنيف:'
            if category_template in self.text:
                text = self.text.replace(category_template, template_name + '\n' + category_template, 1)
            else:
                text = self.text + '\n' + template_name
        self.text = text

    def check(self):
        parsed = wtp.parse(self.text)
        templates_found_number = 0
        for needed_templated in self.list_of_templates:
            for template in parsed.templates:
                if prepare_str(needed_templated) == prepare_str(template.normal_name()):
                    self.list_of_template_found.append(template)
                    templates_found_number += 1

        return bool(templates_found_number)

    def ignore(self):
        parsed = wtp.parse(self.text)
        found = False
        for template in parsed.templates:
            if prepare_str("لا لصيانة البوابات") == prepare_str(template.normal_name()):
                found = True
                break
        return found
