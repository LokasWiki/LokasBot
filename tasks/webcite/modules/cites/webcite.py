import re

import wikitextparser as wtp


class WebCite:
    def __init__(self, template):
        self.template = template
        self.o_template = template
        self.clear_template = template
        self.archive_url_args = [
            "مسار الأرشيف",
            "archiveurl",
            "archive-url",
            "مسار أرشيف"
        ]
        self.url_args = [
            "url",
            "المسار",
            "مسار"

        ]
        self.arguments_after_clean = []
        self.archive_url_args_found = []
        self._check_args_found()

    def url(self):
        for need_arg in self.url_args:
            if self.template.has_arg(need_arg):
                if self.template.get_arg(need_arg).value.strip().lower():
                    return self.template.get_arg(need_arg)
        return None

    def is_archived(self):
        res = len(self.archive_url_args_found) == 1
        return res

    def _check_args_found(self):

        for arg in self.template.arguments:
            if len(arg.value.strip().lower()) >= 1:
                self.arguments_after_clean.append(arg)

        for need_arg in self.archive_url_args:
            for arg in self.arguments_after_clean:
                if arg.name.strip().lower() == need_arg.strip().lower():
                    self.archive_url_args_found.append(arg)
