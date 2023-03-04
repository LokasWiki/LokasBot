import time
import traceback

import wikitextparser as wtp

from tasks.webcite.data import list_of_template
from tasks.webcite.modules.cite import Cite
from tasks.webcite.modules.request_limiter import RequestLimiter


class Parsed:

    def __init__(self, text, summary, limiter):
        self.text = text
        self.old_text = text
        self.cite_templates = []
        self.list_of_templates = list_of_template
        self.summary = summary
        self.limiter = limiter
        self.max_number = 20
        self.number = 0

    def __call__(self):
        if self.check():
            self.start_replace()
        if self.text != self.old_text:
            self.summary += "بوت:الإبلاغ عن رابط معطوب أو مؤرشف V1.2.5*"
        return self.text, self.summary

    def check(self):
        parsed = wtp.parse(self.text)
        templates_found_number = 0
        for needed_templated in self.list_of_templates:
            for template in parsed.templates:
                if needed_templated[0].lower() == template.normal_name().lower():
                    self.cite_templates.append(template)
                    templates_found_number += 1
        return bool(templates_found_number)

    def start_replace(self):
        for template in self.cite_templates:
            # to make it only archive 10 links in one edit
            if self.number == self.max_number:
                break
            try:
                cite = Cite(template)
                # to check if url found
                if cite.check_available():
                    # to check if cite has archive link
                    if cite.is_archived() is False:
                        self.number += 1
                        time.sleep(2)
                        if self.limiter.can_make_request():
                            self.limiter.add_request()
                            # start archive cite
                            cite.archive_it()
                            cite.update_template()
                        else:
                            print("Rate limit exceeded, sleeping for 60 seconds")
                            time.sleep(60)
                        self.text = str(self.text).replace(str(cite.template.o_template), str(cite.template.template))
            except Exception as e:
                print(f"An error occurred while processing {template}: {e}")
                just_the_string = traceback.format_exc()
                print(just_the_string)
