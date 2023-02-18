import time
import traceback

import wikitextparser as wtp

from tasks.webcite.modules.cite import Cite
from tasks.webcite.modules.cites.webcite import WebCite


class Parsed:

    def __init__(self, text, summary):
        self.text = text
        self.old_text = text
        self.cite_templates = []
        self.list_of_templates = [
            "مرجع موقع",
            "استشهاد ويب/إنجليزي",
            "Cite web",
            "Citeweb",
            "مرجع وب",
            "مرجع وب/إنجليزي",
            "Cita web",
            "يستشهد ويب",
            "استشهاد بموقع",
            "Web cite",
            "مرجع ويب",
            "مرجع ويب/إنجليزي",
            "Cw",
            "استشهاد ويب"
        ]
        self.summary = summary
        self.max_number = 9
        self.number = 0

    def __call__(self):
        if self.check():
            self.start_replace()
        if self.text != self.old_text:
            self.summary += "بوت:الإبلاغ عن رابط معطوب أو مؤرشف V0.6*"
        return self.text, self.summary

    def check(self):
        parsed = wtp.parse(self.text)
        templates_found_number = 0
        for needed_templated in self.list_of_templates:
            for template in parsed.templates:
                if needed_templated.lower() == template.normal_name().lower():
                    self.cite_templates.append(template)
                    templates_found_number += 1
        return bool(templates_found_number)

    def start_replace(self):
        for template in self.cite_templates:
            # to make it only archive 10 links in one edit
            if self.number == self.max_number:
                break
            try:
                print(self.number)
                webcite = WebCite(template)
                cite = Cite(webcite)

                if cite.is_archived() is False:
                    self.number += 1
                    time.sleep(2)
                    cite.archive_it()
                    cite.update_template()
                    self.text = str(self.text).replace(str(cite.template.o_template), str(cite.template.template))
            except Exception as e:
                print(f"An error occurred while processing {template}: {e}")
                just_the_string = traceback.format_exc()
                print(just_the_string)
