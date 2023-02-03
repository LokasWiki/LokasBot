import re


class WikiLinkExtractor:
    def __init__(self, text):
        self.text = text
        self.links = []

    def extract_links(self):
        pattern = re.compile(r'\{\{.*?\}\}', re.IGNORECASE | re.DOTALL)
        templates = re.findall(pattern, self.text)

        for template in templates:
            self.text = self.text.replace(template, "")

        pattern = re.compile(r'\[\[(?!.*:)(.*?)\]\]', re.IGNORECASE)
        matches = re.findall(pattern, self.text)
        for match in matches:
            if "تصنيف:" not in match.lower() and "Category:" not in match.lower() and ":" not in match.split(":")[0]:
                if "|" in match:
                    link = match.split("|")[0]
                else:
                    link = match
                self.links.append(link)
        return self.links

