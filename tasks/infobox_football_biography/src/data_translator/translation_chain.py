class TranslationChain:
    def __init__(self):
        self.handlers = []

    def add_handler(self, handler):
        self.handlers.append(handler)

    def translate(self, value):
        for handler in self.handlers:
            translated_value = handler.translate(value)
            if translated_value:
                return translated_value
        return value
