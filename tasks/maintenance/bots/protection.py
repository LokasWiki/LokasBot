import wikitextparser as wtp

from core.utils.helpers import prepare_str


class Protection:
    def __init__(self, page, text, summary):
        self.page = page
        self.text = text
        self.templates = [
            "محمية",
            "Protected",
            "حماية خاصة",
            "حماية نزاع",
            "Pp-semi-template",
            "Pp-semi-vandalism",
            "Pp-dispute",
            "قفل",
            "Pp-semi-protected",
            "Pp-move-indef",
            "Pp-protected",
            "حماية كلية",
            "حماية حرب",
            "حماية جزئية",
            "Pp-semi",
            "حماية كاملة",
            "حماية",
            "صفحة محمية",
            "Semi-protection",
            "Pp-semi-indef",
            "محمية/تحويلة",
            "شبه محمي",
            "حماية تخريب"
        ]
        self.type_of_protection = None
        self.parsed = wtp.parse(self.text)
        self.summary = summary

    def __call__(self):

        if self.check():
            self.add_template()

        else:
            self.remove_template()
        return self.text, self.summary

    def add_template(self):
        """
        This method adds the {{محمية}} template to the page if it doesn't already exist.
        """
        # todo:add away to check old template attr
        found = False
        for needed_template in self.templates:
            for template in self.parsed.templates:
                if prepare_str(template.name) == prepare_str(needed_template):
                    found = True
                    break

        if not found:
            if self.page.isRedirectPage():
                new_text = self.text
                new_text += "\n"
                new_text += "{{محمية|تحويلة}}"
            else:
                if self.type_of_protection is not None:
                    new_text = "{{محمية|" + str(self.type_of_protection) + "}}"
                else:
                    new_text = "{{محمية}}"
                new_text += "\n"
                new_text += self.text

            self.text = new_text
            self.summary += "، بوت:إضافة قالب حماية"

    def remove_template(self):
        """
           This method removes the {{محمية}} template from the page if it exists.
           """
        new_text = self.text
        for needed_template in self.templates:
            for template in self.parsed.templates:
                if prepare_str(template.name) == prepare_str(needed_template):
                    new_text = str(new_text).replace(str(template) + "\n", "")
                    new_text = str(new_text).replace(str(template), "")

        if new_text != self.text:
            self.text = new_text
            self.summary += "، إزالة قالب الحماية"

    def check(self):
        protection = self.page.protection()
        has_protection = False

        # The dictionary is not empty that mean page have protection
        if bool(protection):
            has_protection = True
            if 'edit' in protection and protection['edit'] is not None:
                if 'autoconfirmed' in protection['edit']:
                    self.type_of_protection = 1
                elif 'editautoreviewprotected' in protection['edit']:
                    self.type_of_protection = 4
                elif 'editeditorprotected' in protection['edit']:
                    self.type_of_protection = 2
                elif 'sysop' in protection['edit']:
                    self.type_of_protection = 3
            elif 'move' in protection and protection['move'] is not None:
                self.type_of_protection = "نقل"

        return has_protection
