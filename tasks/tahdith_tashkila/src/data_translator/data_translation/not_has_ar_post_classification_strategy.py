from tasks.tahdith_tashkila.src.data_translator.data_translation_handler import DataTranslationHandler


class NotHasArPostTranslationHandler(DataTranslationHandler):
    def translate(self, value):
        # Translate the wiki link to Arabic (implement this logic)
        return "{{لاعب تشكيلة فريق كرة قدم|الرقم=2|الاسم=[[ميتش آباو]]}}"
