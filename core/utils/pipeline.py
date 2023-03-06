class Pipeline:
    def __init__(self, page, text, summary, steps, extra_steps):
        self.page = page
        self.text = text
        self.summary = summary
        self.steps = steps
        self.extra_steps = extra_steps
        self.oldText = text

    def process(self):
        for step in self.steps:
            obj = step(self.page, self.text, self.summary)
            self.text, self.summary = obj()

        if self.hasChange():
            for step in self.extra_steps:
                obj = step(self.page, self.text, self.summary)
                self.text, self.summary = obj()

        return self.text, self.summary

    def hasChange(self):
        return self.text != self.oldText
