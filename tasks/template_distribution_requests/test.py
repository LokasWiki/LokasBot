import re

import pywikibot


class WikiLinkExtractor:
    def __init__(self, text):
        self.text = text
        self.links = []

    def extract_links(self):
        pattern = re.compile(r'\[\[(.*?)\]\]', re.IGNORECASE)
        matches = re.findall(pattern, self.text)
        for match in matches:
            if "تصنيف:" not in match.lower() and "Category:" not in match.lower():
                if "|" in match:
                    link = match.split("|")[0]
                else:
                    link = match
                self.links.append(link)
        return self.links

site = pywikibot.Site()
title = "قالب:أقران ملوك حاليون"
page = pywikibot.Page(site,title)

extractor = WikiLinkExtractor(page.text)
links = extractor.extract_links()

# for link in page.linkedPages(namespaces=[0],follow_redirects=True):
for temlink in links:
# tempPage = pywikibot.Page(site,"مستخدم:لوقا/ملعب 10")
# for link in [tempPage]:
    link = pywikibot.Page(site,temlink)
    if link.exists() and link.namespace() == 0:
        template_found = False
        for tpl in link.templates(content=False):
            if tpl.title() == page.title():
                template_found = True
                break
        print(link.title())
        if not template_found:
            template_name = "{{" + title + "}}"
            text = link.text
            portal_template = '{{شريط بوابات'
            stub_template = '{{بذرة'
            category_template = '[[تصنيف:'
            if portal_template in text:
                text = text.replace(portal_template, template_name + '\n' + portal_template,1)
            elif stub_template in text:
                text = text.replace(stub_template, template_name + '\n' + stub_template,1)
            elif category_template in text:
                text = text.replace(category_template, template_name + '\n' + category_template,1)
            else:
                text = text + '\n' + template_name
            link.text = text
            link.save("بوت:توزيع قالب")

