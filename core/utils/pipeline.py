import logging


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

            try:
                # to skip if some one bot not all
                obj = step(self.page, self.text, self.summary)
                self.text, self.summary = obj()
            except Exception as e:
                logging.exception(e)

        if self.hasChange():
            for step in self.extra_steps:
                try:
                    # to skip if some one bot not all
                    obj = step(self.page, self.text, self.summary)
                    self.text, self.summary = obj()
                except Exception as e:
                    logging.exception(e)

        return self.text, self.summary

    def hasChange(self):
        return self.text != self.oldText


class PipelineWithExtraSteps(Pipeline):
    def process(self):
        for step in self.steps:

            try:
                # to skip if some one bot not all
                obj = step(self.page, self.text, self.summary)
                self.text, self.summary = obj()
            except Exception as e:
                logging.exception(e)

        return self.text, self.summary
