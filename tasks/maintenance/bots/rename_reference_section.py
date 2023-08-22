'''
لا يوجد توافق حول تشغيل هذا البوت، لذلك لا يجب إضافته إلي البوت الأساسي بأي شكل من الأشكال قبل طلب توافق مرة أخري 
رابط النقاش   https://w.wiki/7Efz
'''
import copy

import wikitextparser as wtp

from core.utils.helpers import prepare_str


class RenameReferenceSection:
    """
    A class for renaming the "References" section in a MediaWiki page.

    Attributes:
        page (pywikibot.Page): The page to be edited.
        text (str): The text of the page to be edited.
        sections_name (list): A list of section names to be renamed.
        all_sections_level (list): A list of section levels to be renamed.
        new_sections_name (str): The new name for the section.
        parsed (wikitextparser.WikiText): The parsed wikitext of the page.
        summary (str): The edit summary for the page.
    """

    def __init__(self, page, text, summary):
        """
        Initializes a RenameReferenceSection object.

        Args:
            page (pywikibot.Page): The page to be edited.
            text (str): The text of the page to be edited.
            summary (str): The edit summary for the page.
        """
        # The page to be edited
        self.page = page
        # The text of the page to be edited
        self.text = text
        # A list of section names to be renamed
        self.sections_name = [
            "مراجع",
        ]
        # A list of section levels to be renamed
        self.all_sections_level = [2]
        # The new name for the section
        self.new_sections_name = "المراجع"
        # The parsed wikitext of the page
        self.parsed = wtp.parse(self.text)
        # The edit summary for the page
        self.summary = summary

    def __call__(self):
        """
        Renames the "References" section in the page if it exists.

        Returns:
            tuple: A tuple containing the edited text and the edit summary.
        """
        if self.check():
            self.rename_section()
        return self.text, self.summary

    def rename_section(self):
        """
        Renames the "References" section in the page to the new name.
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
        """
        Checks if the "References" section exists in the page.

        Returns:
            bool: True if the section exists, False otherwise.
        """
        found = False
        for section in self.parsed.sections:
            for section_name in self.sections_name:
                if prepare_str(section_name) == prepare_str(section.title) and section.level in self.all_sections_level:
                    found = True
                    break
        return found
