class WebCite:
    def __init__(self, template):
        self.template = template
        self.archive_url_args = [
            "مسار الأرشيف",
            "archiveurl",
            "مسار الأرشيف",
            "archive-url"
        ]
        self.arguments_after_clean = self.template.arguments
        self.archive_url_args_found = []

    def is_archived(self):
        res = False
        res = self._check_args_found() == 1
        return res

    def _check_args_found(self):
        self.arguments_after_clean = [arg for arg in self.template.arguments if len(arg.value.strip().lower()) >= 1]
        for need_arg in self.archive_url_args:
            for arg in self.arguments_after_clean:
                if arg.name.strip().lower() == need_arg.strip().lower():
                    self.archive_url_args_found.append(arg)

