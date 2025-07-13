from tasks.tahdith_tashkila.src.data_translator.data_translation_handler import DataTranslationHandler
from tasks.tahdith_tashkila.src.models.player import Player


class NotHasArPostTranslationHandler(DataTranslationHandler):
    def translate(self, model: Player):
        if model.classification != "not_has_ar_post":
            return

        template_format = "{{template_name|الرقم=number|الاسم=page_title}}"
        template_format = template_format.replace("template_name", self.template_name(model))
        if model.is_manager:
            template_format = template_format.replace("|الرقم=number", "")
        else:
            template_format = template_format.replace("number", self.number(model))
        template_format = template_format.replace("page_title", self.name(model))

        # Translate the wiki link to Arabic (implement this logic)
        return template_format

    def template_name(self, model: Player):
        template = "لاعب تشكيلة فريق كرة قدم"
        if model.is_manager:
            template = "مدرب تشكيلة فريق كرة قدم"
        return template

    def number(self, model: Player):
        return str(model.number)

    def name(self, model: Player):
        temp_template = "{{وإو|ar_name|en_name}}"
        return temp_template.replace("ar_name", model.page_title).replace("en_name", model.page_title)
