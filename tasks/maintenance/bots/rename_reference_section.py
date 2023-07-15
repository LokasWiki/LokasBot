import copy

import wikitextparser as wtp

from core.utils.helpers import prepare_str


class RenameReferenceSection:
    def __init__(self, page, text, summary):
        self.page = page
        self.text = text
        self.sections_name = [
            "مراجع",
        ]
        self.all_sections_level = [2]
        self.new_sections_name = "المراجع"
        self.parsed = wtp.parse(self.text)
        self.summary = summary

    def __call__(self):

        if self.check():
            self.rename_section()
        return self.text, self.summary

    def rename_section(self):
        """
        this method rename the section name if name is in self.sections_name to self.new_sections_name
        """
        add_summary = False
        for section in self.parsed.sections:
            for section_name in self.sections_name:
                if prepare_str(section_name) == prepare_str(section.title) and section.level in self.all_sections_level:
                    temp_section = copy.deepcopy(section)
                    temp_section.title = self.new_sections_name
                    self.text = self.text.replace(section.string, temp_section.string)
                    if not add_summary:
                        self.summary += "، ضبط اسم قسم المراجع"
                        add_summary = True

    def check(self):
        found = False
        for section in self.parsed.sections:
            for section_name in self.sections_name:
                if prepare_str(section_name) == prepare_str(section.title) and section.level in self.all_sections_level:
                    found = True
                    break
        return found
