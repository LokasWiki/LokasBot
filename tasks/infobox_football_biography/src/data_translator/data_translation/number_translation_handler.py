from tasks.infobox_football_biography.src.data_translator.data_translation_handler import DataTranslationHandler


class NumberTranslationHandler(DataTranslationHandler):
    def translate(self, value):
        # Translate the number to Arabic
        return str(value)
