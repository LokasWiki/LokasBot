import re
from datetime import datetime
import wikitextparser as wtp
import pywikibot
import hashlib


class Options:
    def __init__(self, page: pywikibot.Page, template_name: str = "أرشفة آلية"):
        """
        Initializes the object with the given `page` and `template_name`.

        Parameters:
            page (pywikibot.Page): The page object.
            template_name (str, optional): The name of the template. Defaults to "أرشفة آلية".

        Returns:
            None
        """
        self.template_name = template_name
        self.page = page
        self.option = ('قسم', '3', None)
        self._get_params()

    def _get_template(self):
        """
        Retrieves the template with the specified name from the page's wikitext.

        Returns:
            wtp.Template or None: The template object if found, None otherwise.
        """
        text = self.page.get()
        templates = wtp.parse(text).templates
        for t in templates:
            if t.name == self.template_name:
                return t
        return None

    def _get_params(self):
        """
        Retrieves the parameters from the template.

        Returns:
            tuple or None: A tuple containing the values of the template arguments if the template has exactly three arguments,
                           or None if the template is not found or has a different number of arguments.
        """
        template = self._get_template()
        if template is None:
            return None

        arguments = template.arguments
        if len(arguments) == 3:
            self.option = (arguments[0].value, arguments[1].value, arguments[2].value)




class Section:
    def __init__(self, title, content):
        self.title = title.strip()
        self.content = content
        self.id = self._generate_id()

    def _generate_id(self):
        content_hash = hashlib.sha1(self.content.encode('utf-8')).hexdigest()
        return f"{self.title}_{content_hash}"


class Archiver:
    def __init__(self, page: pywikibot.Page):
        """
        Initializes a Archiver object.
        Args:
            page (pywikibot.Page): The page to be edited.
        """
        # The page to be edited
        self.talk_page = page
        self.options = (Options(self.talk_page)).option

    def archive_talk_page(self, ARCHIVE_THRESHOLD_DAYS=3):
        """
        Archives the talk page of the user.
        """
        last_comment_timestamps = self.get_last_comment_timestamps()
        text = self.talk_page.get()

        sections = self._split_sections(text)
        header = self._extract_header(text)
        current_time = datetime.utcnow()
        archive_text = ''
        remaining_text = ''

        for section_title, section_content in sections:
            section = Section(section_title, section_content)

            if section.id in last_comment_timestamps:
                last_comment_time = last_comment_timestamps[section.id]
                if (current_time - last_comment_time).days > ARCHIVE_THRESHOLD_DAYS:
                    archive_text += section_title + section_content
                else:
                    remaining_text += section_title + section_content
            else:
                remaining_text += section_title + section_content

        if archive_text:
            print("test")
            # archive_page = pywikibot.Page(self.site, f'{ARCHIVE_PAGE_PREFIX}{current_time.strftime("%Y-%m")}')
            # archive_page.text += archive_text
            # archive_page.save(summary='Archiving old discussions')
            #
            # self.talk_page.text = remaining_text
            # self.talk_page.save(summary='Archiving old discussions')
        else:
            print("No sections to archive.")

    def get_last_comment_timestamps(self):
        history = self.talk_page.revisions(reverse=True, total=500, content=True)  # Fetch last 500 revisions
        section_last_edit = {}
        seen_sections = set()

        for revision in history:
            timestamp = revision.timestamp
            content = revision.text

            sections = self._split_sections(content)
            current_sections = set()

            for section_title, section_content in sections:
                section = Section(section_title, section_content)
                current_sections.add(section.id)

                if section.id not in section_last_edit:
                    section_last_edit[section.id] = timestamp
                else:
                    section_last_edit[section.id] = max(section_last_edit[section.id], timestamp)

            removed_sections = seen_sections - current_sections
            for section_id in removed_sections:
                if section_id not in section_last_edit:
                    section_last_edit[section_id] = timestamp

            seen_sections = current_sections

        return section_last_edit

    def _split_sections(self, text):
        parsed = wtp.parse(text)
        sections = parsed.sections
        # show only sections with level 2
        return [(section.title, section.string) for section in sections if section.level == 2]

    def _extract_header(self, text):
        parsed = wtp.parse(text)
        templates = parsed.templates

        headers = []
        for template in templates:
            if template.name == 'رشف':
                headers.append(template.span[0])
                headers.append(template.span[1])
        if len(headers) <= 1:
            return ""
        if len(headers) >= 2:
            return text[headers[0]:headers[-1]]


site = pywikibot.Site('ar', 'wikipedia')
page_name = "نقاش_المستخدم:لوقا"
page = pywikibot.Page(site, page_name)
archive_obj = Archiver(page)
archive_obj.archive_talk_page()
"""
read options from template
create class to archive sections
skip sections that have no archive template
customez archive summary
"""
