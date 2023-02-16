import wikitextparser as wtp


class Parsed:

    def __init__(self, text, summary):
        self.text = text
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

    def __call__(self):
        if self.check():
            pass
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
