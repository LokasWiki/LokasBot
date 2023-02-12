import re
import wikitextparser as wtp

from core.utils.disambiguation import Disambiguation


class PortalsBar:
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
        disambiguation = Disambiguation(self.page.title(), self.text)
        if disambiguation.check("or"):
            return self.text, self.summary
        #  if true start remove template
        # if false start add template if not found and remove Portals templates
        if not self.check():
            self.add_template()
        else:
            self.remove_template()
        return self.text, self.summary

    def add_template(self):
        """
        This method adds the {{مقالات بحاجة لشريط بوابات}} template to the page if it doesn't already exist.
        """
        parsed = wtp.parse(self.text)
        template_found = False
        for needed_templated in self.list_of_needed_templates:
            for template in parsed.templates:
                if needed_templated.lower() == template.normal_name().lower():
                    template_found = True
                    break

        is_edited = False

        if not template_found:
            template_name = "{{مقالات بحاجة لشريط بوابات}}"
            category_template = '[[تصنيف:'
            if category_template in self.text:
                text = self.text.replace(category_template, template_name + '\n' + category_template, 1)
            else:
                text = self.text + '\n' + template_name
            self.text = text
            is_edited = True

        if is_edited or self.remove_Portals_templates():
            self.summary += "، أضاف وسم مقالات بحاجة لشريط بوابات"

    def remove_Portals_templates(self):
        parsed = wtp.parse(self.text)
        is_edited = False
        for needed_templated in self.list_of_templates:
            for template in parsed.templates:
                if needed_templated.lower() == template.normal_name().lower():
                    self.text = self.text.replace(str(template), "")
                    is_edited = True
        return is_edited

    def remove_template(self):
        """
           This method removes the {{مقالات بحاجة لشريط بوابات}} template from the page if it exists.
           """
        new_text = self.text
        parsed = wtp.parse(self.text)
        is_edited = False
        for needed_templated in self.list_of_needed_templates:
            for template in parsed.templates:
                if needed_templated.lower() == template.normal_name().lower():
                    new_text = self.text.replace(str(template), "")
                    is_edited = True

        if new_text != self.text and is_edited:
            self.text = new_text
            self.summary += "، حذف وسم مقالات بحاجة لشريط بوابات"

    def check(self):
        parsed = wtp.parse(self.text)
        template_found = False
        exclude_list = [
            "نمط",
            "حد",
            "قد",
            "عرض",
            "فاصل"
        ]
        for needed_templated in self.list_of_templates:
            for template in parsed.templates:
                if needed_templated.lower() == template.normal_name().lower():
                    # to remove the نمط argument {{شريط بوابات|نمط=قائمة|كيمياء|فيزياء}}
                    arguments = [arg for arg in template.arguments if arg.name.strip().lower() not in exclude_list]
                    for argument in arguments:
                        if len(str(argument.value).strip()) > 1 :
                            template_found = True
                    break
        return template_found
