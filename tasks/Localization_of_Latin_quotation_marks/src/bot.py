import pywikibot
import wikitextparser as wtp


class BotFactory:
    def __init__(self):
        self.site = pywikibot.Site()
        self.page = None
        self.page_text = str("")

    def load_page(self, page_title: str):
        self.page = pywikibot.Page(self.site, page_title)
        if not self.page.exists():
            raise Exception("Page " + page_title + " is not exists")
        self.page_text = self.page.text

    def run(self, page_title: str):
        self.load_page(page_title=page_title)
        self.remove()
        self.save()

    def remove(self):
        parse = wtp.parse(self.page_text)

        # Create a list to store the start and end indices of templates and HTML tags
        indices = []

        # templates
        for template in parse.templates:
            indices.append(template.span)

        # HTML tags
        for tag in parse.get_tags():
            indices.append(tag.span)
        # tables
        for table in parse.get_tables():
            indices.append(table.span)

        # Replace double quotes outside of templates and HTML tags
        modified_content = list(self.page_text)
        number_of_fount = 0
        for i in range(len(modified_content)):
            if modified_content[i] == '"' and not any(start <= i < end for start, end in indices):
                modified_content[i] = '«' if number_of_fount % 2 == 0 else '»'
                number_of_fount += 1

        # Join the modified characters back into a string
        modified_content = ''.join(modified_content)

        self.page_text = modified_content

    def save(self):
        self.page.text = self.page_text
        self.page.save("بوت:تعريب علامات التنصيص اللاتينية v0.0.1-beta")
