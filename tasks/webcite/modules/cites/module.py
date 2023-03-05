import copy

from tasks.webcite.modules.date_formatter import DateFormatter


class BaseCite:
    """Class representing a base for cite template"""

    def __init__(self, template):
        self.template = template
        self.o_template = copy.deepcopy(template)
        self.archive_url_args = [
            "مسار الأرشيف",
            "archiveurl",
            "archive-url",
            "مسار أرشيف"
        ]
        self.archive_date_args = [
            "archivedate",
            "تاريخ الأرشيف",
            "archive-date",
            "تاريخ أرشيف"
        ]
        self.url_args = [
            "url",
            "المسار",
            "مسار"
        ]
        self.title_args = [
            "title",
            "العنوان",
            "عنوان",
        ]

        self.accessdate_args = [
            "accessdate",
            "access-date",
            "تاريخ الوصول",
            "accessdate",
            "تاريخ الوصول للمسار"

        ]

        self.arguments_after_clean = []
        self.archive_url_args_found = []
        self._check_args_found()

    def url(self):
        for need_arg in self.url_args:
            for arg in self.template.arguments:
                if need_arg.lower().strip().replace(" ", "_") == arg.name.lower().strip().replace(" ", "_"):
                    if arg.value.strip().lower():
                        return self.template.get_arg(arg.name)
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
                if arg.name.lower().strip().replace(" ", "_") == need_arg.lower().strip().replace(" ", "_"):
                    self.archive_url_args_found.append(arg)

    def replace_to(self, searched_list, arg):
        my_arg = None
        for need_arg in searched_list:
            if self.template.has_arg(need_arg.strip().lower()):
                tem_arg = copy.deepcopy(self.template.get_arg(need_arg.strip().lower()))
                if len(tem_arg.value) >= 10:
                    self.template.del_arg(need_arg.strip().lower())
                    my_arg = tem_arg

        if my_arg is not None:
            self.template.set_arg(arg.strip().lower(), my_arg.value.strip())

    def update_template(self, url, timestamp):
        for need_arg in self.archive_url_args:
            if self.template.has_arg(need_arg):
                self.template.del_arg(need_arg)

        for need_arg in self.archive_date_args:
            if self.template.has_arg(need_arg):
                self.template.del_arg(need_arg)

        formatter_ar = DateFormatter(language='ar')
        formatted_date_ar = formatter_ar.format_timestamp(timestamp)

        self.replace_to(self.url_args, "مسار")
        self.replace_to(self.title_args, "عنوان")
        self.replace_to(self.accessdate_args, "تاريخ الوصول")
        o_url_value = self.template.get_arg("مسار").value.strip()
        self.template.set_arg("تاريخ أرشيف", formatted_date_ar)
        self.template.del_arg("مسار")
        self.template.set_arg("مسار", o_url_value)
        self.template.set_arg("مسار أرشيف", url)
